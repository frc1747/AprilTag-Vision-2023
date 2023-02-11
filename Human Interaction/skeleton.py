import cv2
import mediapipe as mp
import threading
import time
from networktables import NetworkTables

# Network Tables Initiation

TEAM_IP = 'roborio-1747-frc.local'
TIMEOUT_TIME = 20
TABLE_NAME = 'SmartDashboard'

def initNetworkTables():
    def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        with cond:
            notified[0] = True
            cond.notify()

    print('Attempting to connect to RoboRio. Timing out in',TIMEOUT_TIME,'seconds.')
    # Start timeout timer
    startTime = time.time()

    cond = threading.Condition()
    notified = [False]

    # As a client to connect to a robot
    serverIP = TEAM_IP
    NetworkTables.initialize(server=serverIP)
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
    
    with cond:
        # Check if we connected
        print("Waiting")
        if not notified[0]:
            # Keep waiting until we connect or time out
            # Returns true if sucess, false if timed out.
            connectionState = cond.wait(TIMEOUT_TIME)
    
    # Check if we timed out.
    if connectionState == False:
        print("Connection Timed out after",TIMEOUT_TIME,"seconds.")
        quit()

    print("Connection Established!")
    
    global nTable
    nTable = NetworkTables.getTable(TABLE_NAME)
    nTable.putBoolean('connected', True)
    if nTable.getBoolean('connected',defaultValue=False):
        print('Connected to RoboRio at', serverIP)
    else:
        print('Connection Failed')

initNetworkTables()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Defined here: https://google.github.io/mediapipe/solutions/pose.html#pose_landmarks
left_hip = 23
right_hip = 24

usableDistance = None

pose = mp_pose.Pose(
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5)

cap = cv2.VideoCapture(2)

while cap.isOpened():
	# read frame from capture object
	_, frame = cap.read()

	try:
		# convert the frame to RGB format
		RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	
		# process the RGB frame to get the result
		results = pose.process(RGB)

		if results.pose_landmarks != None:
			# If the left hip is best to use
			if results.pose_landmarks.landmark[left_hip].visibility > results.pose_landmarks.landmark[right_hip].visibility and results.pose_landmarks.landmark[left_hip].visibility > 0.7:
				usableDistance = results.pose_landmarks.landmark[left_hip]
			
			# If the right hip is best to use
			elif results.pose_landmarks.landmark[right_hip].visibility > results.pose_landmarks.landmark[left_hip].visibility and results.pose_landmarks.landmark[right_hip].visibility > 0.7:
				usableDistance = results.pose_landmarks.landmark[right_hip]

			else:
				usableDistance = None
		if results.pose_landmarks == None:
			usableDistance = None

		mp_drawing.draw_landmarks(
		frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

	except:
			pass

	cv2.imshow("Output", frame)

	if usableDistance != None:
		nTable.putNumber("Skeleton X", usableDistance.x)
		nTable.putNumber("Skeleton Y", usableDistance.y)
		nTable.putNumber("Skeleton Z", usableDistance.z)

	if cv2.waitKey(1) == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()
