# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
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



ap = argparse.ArgumentParser()

args = vars(ap.parse_args())

# Camera Resolution: 640 x 480

vs = VideoStream(src=1).start()

while True:

	frame = vs.read()

	frame = frame[1] if args.get("video", False) else frame

	if frame is None:
		break

	frame = imutils.resize(frame, width=640, height=480)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# ----- Cube initialization -----

	purpleLower = (113, 34, 71)
	purpleUpper = (168, 255, 255)

	cubeMask = cv2.inRange(hsv, purpleLower, purpleUpper)
	cubeMask = cv2.erode(cubeMask, None, iterations=3)
	cubeMask = cv2.dilate(cubeMask, None, iterations=3)

	cubeCnts = cv2.findContours(cubeMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cubeCnts = imutils.grab_contours(cubeCnts)
	center = None

	# ----- Cone initialization -----

	yellowLower = (0, 89, 117)
	yellowUpper = (88, 255, 255)

	coneMask = cv2.inRange(hsv, yellowLower, yellowUpper)
	# coneMask = cv2.erode(coneMask, None, iterations=3)
	# coneMask = cv2.dilate(coneMask, None, iterations=3)

	coneCnts = cv2.findContours(coneMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	coneCnts = imutils.grab_contours(coneCnts)
	center = None

	# Place center screen frame

	cv2.circle(frame, (320, 240), 3, (0, 0, 255), 5)

	if len(cubeCnts) > 0:
		c = max(cubeCnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		if M["m00"] != 0:
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.putText(frame, "Cube", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
			cv2.putText(frame, "Cube X: " + str(int(x)), (0, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(255,0,255), 2)
			if M["m00"] != 0:
				cv2.circle(frame, center, 5, (255, 255, 255), -1)
				nTable.putNumber("Cube X", x)
			else:
				nTable.putNumber("Cube X", 0)

	if len(coneCnts) > 0:
		c = max(coneCnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		if M["m00"] != 0:
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.putText(frame, "Cone", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255))
			cv2.putText(frame, "Cone X: " + str(int(x)), (0, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(255,0,255), 2)
			if M["m00"] != 0:
				cv2.circle(frame, center, 5, (255, 255, 255), -1)
				nTable.putNumber("Cone X", x)
			else:
				nTable.putNumber("Cone X", 0)

	else:
		nTable.putNumber("Cone X", 0)
		nTable.putNumber("Cube X", 0)

	cv2.imshow("Game Piece Detection", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

vs.stop()
vs.release()
cv2.destroyAllWindows()