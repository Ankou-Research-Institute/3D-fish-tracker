# 3D-fish-tracker
## 1. Overview
We are trying to build up an open experiment environment for tracking 3D-positions of a fish school in an aquarium.
Our goal is to identify each fish, track each one's 3D-position (X, Y, Z) by utilizing OpenCV with a Intel RealSense depth camera, and provide open data for researching the collective behavior. 
To our best of knowledge, this is the first open source-based 3D fish tracking project.

## 2. Experimental setup
- Ubuntu 16.04 with OpenCV 3.4.2 on VirtualBox 5.2.22 running on MacOSX (Majove) 
- Intel RealSense D435
- Cube-type aquarium (25cm × 25cm × 25cm)
- 5 Paracheirodon axelrodi
<img src="https://user-images.githubusercontent.com/13718037/69966934-bc61fe00-155a-11ea-96fb-886b53e130cd.jpg" width="450px">

## 3. Technical challenge
As of now, we suppose the camera can track the 2D possion (X, Y) of each fish by using image data.
However, it seems difficult to sense the depth (Z) information because the fish size is too small to be captured by the depth camera.
