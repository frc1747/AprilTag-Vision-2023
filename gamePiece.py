# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()

args = vars(ap.parse_args())

# Camera Resolution: 640 x 480

vs = VideoStream(src=2).start()

while True:

	frame = vs.read()

	frame = frame[1] if args.get("video", False) else frame

	if frame is None:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# ----- Cube initialization -----

	purpleLower = (102, 0, 124)
	purpleUpper = (180, 179, 255)

	cubeMask = cv2.inRange(hsv, purpleLower, purpleUpper)
	cubeMask = cv2.erode(cubeMask, None, iterations=3)
	cubeMask = cv2.dilate(cubeMask, None, iterations=3)

	cubeCnts = cv2.findContours(cubeMask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cubeCnts = imutils.grab_contours(cubeCnts)
	center = None

	# ----- Cone initialization -----

	yellowLower = (0, 151, 73)
	yellowUpper = (180, 255, 255)

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
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.putText(frame, "Cube", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(255,0,255), 2)
			cv2.circle(frame, center, 5, (255, 255, 255), -1)

			print(int(x))

	if len(coneCnts) > 0:
		c = max(coneCnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.putText(frame, "Cone", (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(255,0,255), 2)
			cv2.circle(frame, center, 5, (255, 255, 255), -1)

			print(int(x))

	cv2.imshow("Game Piece Detection", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

vs.stop()
vs.release()
cv2.destroyAllWindows()