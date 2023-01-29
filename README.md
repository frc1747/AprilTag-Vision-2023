# Computer Vision 2023
 This repository contains all custom-built AprilTag Detection code, as well as other vision projects that are in the works for the 2023, Charged Up season.
 
## Apriltag Detection
 As the flagship project, we decided to create a simple, yet efficient AprilTag detection software. Located in `main.py`. It should be noted that this code is *not* used on the robot, but instead acts as a proof of concept and PR tool. AptilTag code integrated into the robot has been made possible through PhotonVision: (https://photonvision.org/)
### Usage:
 - Clone the repository and open `main.py`
 - At the bottom, uncomment the detection mode that accomplishes what you are trying to do.
 > - `calibrate_camera_webcam(webcam_port)`: Deprecated. Use (https://www.calibdb.net/) instead.
 > - `detect_AprilTags(webcam_port)`: Detects and draws AprilTags on a webcam feed using the respective webcam port.
 > - `calibrate_camera_picture(webcam_port)`: Deprecated. Use (https://www.calibdb.net/) instead.
 - Where `webcam_port` is an integer with a default of 0.

### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install cv2`
 - `pip install pupil_apriltags`

## Hand Detection
 This project utilizes libraries to create an interactable robot controller. Using an ai model made by `mediapipe`, an efficient detection algorithm outputs the x, y, and z coordinates of a hand, allowing for integration with other projects. In the case of the version found here, it was used to control a robot through a system of deadzones and invisible boundaries.
 
### Usage:
 - Clone the repository and open `hand.py`
 - Change the `webcam_port` on line 5, Where `webcam_port` is an integer with a default of 0.
 > cap = cv2.VideoCapture(webcam_port)
 - Set the desired resolution by changing `width` and `height`
 > **Note:** It is recommended to use the resolution that your webcam is outputting to avoid severe distortion

### NOTE: The correct dependencies must be installed for this project to work.
 - `pip install cv2`
 - `pip install mediapipe`

## Authors
Created by FRC Team 1747 and all respective contributors.
