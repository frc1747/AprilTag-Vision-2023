import cv2
import mediapipe as mp
import time
from networktables import NetworkTables
import threading

cap = cv2.VideoCapture(1)

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

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 640
height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.8,
                      min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    windowWidth=img.shape[1]
    windowHeight=img.shape[0]

    #Stop
    cv2.circle(img, (int(windowWidth/2),int(windowHeight/2)), 15, (0,0,255), cv2.FILLED)

    #Turn Left
    cv2.circle(img, (int(windowWidth/5),int(windowHeight/2)), 15, (0,0,255), cv2.FILLED)

    #Turn Right
    cv2.circle(img, (int(windowWidth/1.2),int(windowHeight/2)), 15, (0,0,255), cv2.FILLED)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks != None:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):


                # Data exportation code
                # lm.x/y/z gives the resprcitve x, y, or z coordinate

                # print(lm.x)
                nTable.putNumber("Hand X", lm.x)
                # if (lm.x > 0.35 and lm.x < 0.4):
                #     print("Center")

                # Drawing Code (Visual Purposes Only)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 2, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


	
    flipHorizontal = cv2.flip(img, 1)
    cv2.putText(flipHorizontal,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow("Output", flipHorizontal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

img.release()
cv2.destroyAllWindows()