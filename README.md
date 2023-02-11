# Computer Vision 2023
 This repository contains all custom-built AprilTag Detection code, as well as other vision projects that are in the works for the 2023, Charged Up season.
 
## Apriltag Detection
 As the flagship project, we decided to create a simple, yet efficient AprilTag detection software. Located in `aprilTag.py`. It should be noted that this code is *not* used on the robot, but instead acts as a proof of concept and PR tool. AprilTag code integrated into the robot has been made possible through PhotonVision: (https://photonvision.org/)
### Usage:
 - Clone the repository and open `aprilTag.py`
 - At the bottom, uncomment the detection mode that accomplishes what you are trying to do.
 > - `calibrate_camera_webcam(webcam_port)`: Deprecated. Use (https://www.calibdb.net/) instead.
 > - `detect_AprilTags(webcam_port)`: Detects and draws AprilTags on a webcam feed using the respective webcam port.
 > - `calibrate_camera_picture(webcam_port)`: Deprecated. Use (https://www.calibdb.net/) instead.
 - Where `webcam_port` is an integer with a default of 0.

### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install opencv-python`
 - `pip install pupil_apriltags`

## Hand Detection
 This project utilizes libraries to create an interactable robot controller. Using an ai model made by `mediapipe`, an efficient detection algorithm outputs the x, y, and z coordinates of a hand, allowing for integration with other projects. In the case of the version found here, it was used to control a robot through a system of deadzones and invisible boundaries.
 
### Usage:
 - Clone the repository and open `hand.py`
 - Change the `webcam_port` on line 5, where `webcam_port` is an integer with a default of 0.
 > cap = cv2.VideoCapture(webcam_port)
 - Set the desired resolution by changing `width` and `height`
 > **Note:** It is recommended to use the resolution that your webcam is outputting to avoid severe distortion

### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install opencv-python`
 - `pip install mediapipe`
 
## Body Skeleton Detection
 The project is solely created to act as a PR version of the AprilTag onboard robot detection system.  Rather than finding an AprilTag and tracking it, the skeleton program looks for the most visible part of the body, specified by the user, and outputs the coordinates.
 
### Usage:
 - Clone the repository and open `skeleton.py`
 - Change the `webcam_port` on line 18, where `webcam_port` is an integer with a default of 0.
  > cap = cv2.VideoCapture(webcam_port)
 - On lines 34 and 37, change `body_part` to the desired body part, where `body_part` is an integer with a default of 0.
  > `results.pose_landmarks.landmark[body_part]` <br>
  > **NOTE:** The specific body part *must* be the respective integer.  Use the image below as a guide. `left_hip` and `right_hip` have been specifically put into the code and are *NOT* exceptions to the integer requirement. See lines 9 and 10.
  
### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install opencv-python`
 - `pip install mediapipe`

## Game Piece Detection
 This project focuses on detecting the cones and cubes for the 2023 Charged Up FRC game.  Utilizing OpenCV's contour detection library, the program looks for the nearest cone or cube and outlines the position through bounding circles.  The X values of the cube and cone locations are sent to networktables, which can be retrieved through the robot code.
 
 ### Usage:
 - Clone the repository and open `gamePiece.py`
 - Change the `webcam_port` on line 72, where `webcam_port` is an integer with a default of 0.
  > vs = VideoStream(src=webcam_port).start()
 - Set the desired resolution by changing `width` and `height` on line 83
  > **NOTE:** The `width` and `height` are automatically set to 640 and 480, respectively.  These *must* be determined for your specific webcam prior to use.
 - Change the upper and lower bounds for the `cubeLower`, `cubeUpper`, `coneLower`, and `coneUpper` tuples on lines 89-90 and 103-104
  > **NOTE:** These *must* be configured manually as they are different for every webcam and dependent on the lighting of the environment.
  > Utilize `GRIP Pipelines` found in the repository to calibrate the webcam

### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install opencv-python`
 - `pip install imutils`
 - `pip install argparse`
 - `pip install collections`
 - `pip install pynetworktables`
 - `pip install threading`


## GRIP Pipelines
 These are the configurations for essentially optimal cone and cube configurations for the 2023 Charged Up FRC game.
 
### Usage:
 - Download GRIP found here: https://github.com/WPIRoboticsProjects/GRIP
 - Configure as shown by the tutorial on the GRIP `readme`
  > The goal is to get a `mask` that shows only the cone or the cube by editing the `HSV threshold` value
 - Open GRIP and select `file`, then `open`
 - Open the desired pipeline found in the `GRIP Pipelines` folder in this repository
  > **NOTE:** On the left side, the webcam object may need to be removed to change the port.  
  > If this is the case, remove the webcam, click on `add source`, then add the webcam with the correct port. Then drag the `image` dot from the webcam to the `src` dot of the HSV Threshold
 - Under the HSV Threshold tab, edit the `hue`, `saturation`, and `value` sliders until the mask shows the object to the best of its abilities.
  > **NOTE:** You may need to click on the eye icons under the `mask` tab in order to see it.
 - When the mask is succesfully created, use the values on the left of the sliders to set the lower bounds, and the values to the right of the slider to set the upper bounds
  > For example, `hue`: 113 - 168, `saturation`: 34 - 255, `value`: 71 - 255
  > The lower bound will be `(113, 34, 71)` and the upper bound will be `(168, 255, 255)`
 - Change the bounds on lines 89 - 90 and 134 - 135 to the ones calibrated earlier

## Authors
Created by FRC Team 1747 and all respective contributors.
