import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Defined here: https://google.github.io/mediapipe/solutions/pose.html#pose_landmarks
left_hip = 23
right_hip = 24

usableDistance = None

pose = mp_pose.Pose(
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

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
				usableDistance = results.pose_landmarks.landmark[left_hip].z
			
			# If the right hip is best to use
			elif results.pose_landmarks.landmark[right_hip].visibility > results.pose_landmarks.landmark[left_hip].visibility and results.pose_landmarks.landmark[right_hip].visibility > 0.7:
				usableDistance = results.pose_landmarks.landmark[right_hip].z

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
		print(usableDistance)

	if cv2.waitKey(1) == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()
