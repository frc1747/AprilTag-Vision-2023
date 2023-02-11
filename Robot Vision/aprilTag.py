import cv2
import pupil_apriltags
import numpy as np
import os
import glob

        # [
        #     1166.6965407123562,
        #     0,
        #     660.5645539190895
        # ],
        # [
        #     0,
        #     1166.4199167741485,
        #     356.1837856150839
        # ],
        # [
        #     0,
        #     0,
        #     1
        # ]

def detect_AprilTags(camera_port):
	vid = cv2.VideoCapture(camera_port)
	detector = pupil_apriltags.Detector(families="tag36h11")

	while(True):
	
		ret, frame = vid.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		results = detector.detect(gray, estimate_tag_pose=True, camera_params=[1166.6965407123562, 1166.4199167741485, 660.5645539190895, 356.1837856150839], tag_size=17.145)

		gray = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
	
		for r in results:
			(ptA, ptB, ptC, ptD) = r.corners
			ptB = (int(ptB[0]), int(ptB[1]))
			ptC = (int(ptC[0]), int(ptC[1]))
			ptD = (int(ptD[0]), int(ptD[1]))
			ptA = (int(ptA[0]), int(ptA[1]))
	
			cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
			cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
			cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
			cv2.line(frame, ptD, ptA, (0, 255, 0), 2)


			(cX, cY) = (int(r.center[0]), int(r.center[1]))
			cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

			tagFamily = r.tag_family.decode("utf-8")
			tagInt = str(r.tag_id)
			print(r.pose_t)
			cv2.putText(frame, "Tag ID: " + tagInt, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 2)
		
		cv2.imshow('AprilTag Display', frame)
		# cv2.imshow('AprilTag Grayscale', gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	vid.release()
	cv2.destroyAllWindows()

def calibrate_camera_webcam(camera_port):
	vid = cv2.VideoCapture(camera_port)

	# Define the dimensions of checkerboard
	CHECKERBOARD = (7, 9)


	# stop the iteration when specified
	# accuracy, epsilon, is reached or
	# specified number of iterations are completed.
	criteria = (cv2.TERM_CRITERIA_EPS +
				cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


	# Vector for 3D points
	threedpoints = []

	# Vector for 2D points
	twodpoints = []


	# 3D points real world coordinates
	objectp3d = np.zeros((1, CHECKERBOARD[0]
						* CHECKERBOARD[1],
						3), np.float32)
	objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
								0:CHECKERBOARD[1]].T.reshape(-1, 2)
	prev_img_shape = None


	count = 0
	fxList, fyList = [], []
	cxList, cyList = [], []

	while(True):
		ret, frame = vid.read()
		# Import required modules

		grayColor = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Find the chess board corners
		# If desired number of corners are
		# found in the image then ret = true
		ret, corners = cv2.findChessboardCorners(
						grayColor, CHECKERBOARD,
						cv2.CALIB_CB_ADAPTIVE_THRESH
						+ cv2.CALIB_CB_FAST_CHECK +
						cv2.CALIB_CB_NORMALIZE_IMAGE)

		# If desired number of corners can be detected then,
		# refine the pixel coordinates and display
		# them on the images of checker board
		if ret == True:
			threedpoints.append(objectp3d)

			# Refining pixel coordinates
			# for given 2d points.
			corners2 = cv2.cornerSubPix(
				grayColor, corners, (11, 11), (-1, -1), criteria)

			twodpoints.append(corners2)

			# Draw and display the corners
			frame = cv2.drawChessboardCorners(frame,
											CHECKERBOARD,
											corners2, ret)

			# MATH STUFF

			# h, w = frame.shape[:2]

			# ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
			# 	threedpoints, twodpoints, grayColor.shape[::-1], None, None)

			# fx = matrix[0][0]
			# fy = matrix[1][1]
			# cx = matrix[0][2]
			# cy = matrix[1][2]
			# fxList.append(fx)
			# fyList.append(fy)
			# cxList.append(cx)
			# cyList.append(cy)
			# count += 1
			# # print("fx: " + str(fx))
			# # print("fy: " + str(fy))

		cv2.imshow('Camera Calibration', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			# total = 0
			# for num in fxList:
			# 	total += num
			# avgfx = total / count
			# total = 0
			# for num in fyList:
			# 	total += num
			# avgfy = total / count
			# total = 0
			# for num in cxList:
			# 	total += num
			# avgcx = total / count
			# total = 0
			# for num in cyList:
			# 	total += num
			# avgcy = total / count
			# print("Average fx: " + str(avgfx))
			# print("Average fy: " + str(avgfy))
			# print("Average cx: " + str(avgcx))
			# print("Average cy: " + str(avgcy))
			break

	vid.release()
	cv2.destroyAllWindows()

def calibrate_camera_picture():
	# Define the dimensions of checkerboard
	CHECKERBOARD = (7, 9)


	# stop the iteration when specified
	# accuracy, epsilon, is reached or
	# specified number of iterations are completed.
	criteria = (cv2.TERM_CRITERIA_EPS +
				cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


	# Vector for 3D points
	threedpoints = []

	# Vector for 2D points
	twodpoints = []


	# 3D points real world coordinates
	objectp3d = np.zeros((1, CHECKERBOARD[0]
						* CHECKERBOARD[1],
						3), np.float32)
	objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
								0:CHECKERBOARD[1]].T.reshape(-1, 2)
	prev_img_shape = None


	# Extracting path of individual image stored
	# in a given directory. Since no path is
	# specified, it will take current directory
	# jpg files alone
	images = ["1.jpg"]

	for filename in images:
		image = cv2.imread(filename)
		grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Find the chess board corners
		# If desired number of corners are
		# found in the image then ret = true
		ret, corners = cv2.findChessboardCorners(
						grayColor, CHECKERBOARD,
						cv2.CALIB_CB_ADAPTIVE_THRESH
						+ cv2.CALIB_CB_FAST_CHECK +
						cv2.CALIB_CB_NORMALIZE_IMAGE)

		# If desired number of corners can be detected then,
		# refine the pixel coordinates and display
		# them on the images of checker board
		if ret == True:
			threedpoints.append(objectp3d)

			# Refining pixel coordinates
			# for given 2d points.
			corners2 = cv2.cornerSubPix(
				grayColor, corners, (11, 11), (-1, -1), criteria)

			twodpoints.append(corners2)

			# Draw and display the corners
			image = cv2.drawChessboardCorners(image,
											CHECKERBOARD,
											corners2, ret)

		cv2.imshow('img', image)
		cv2.waitKey(0)

	cv2.destroyAllWindows()

	h, w = image.shape[:2]


	# Perform camera calibration by
	# passing the value of above found out 3D points (threedpoints)
	# and its corresponding pixel coordinates of the
	# detected corners (twodpoints)
	ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
		threedpoints, twodpoints, grayColor.shape[::-1], None, None)


	# Displaying required output
	print(" Camera matrix:")
	print(matrix)

# calibrate_camera_webcam(1)
detect_AprilTags(2)
# calibrate_camera_picture()