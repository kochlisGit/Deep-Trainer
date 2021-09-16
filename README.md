# Deep-Trainer
Monitor Your Workout through a Webcam/IP Camera. No equipment is required, other than a camera and a laptop. This application could potentially replace a personal trainer, making it the idea app for workout.

# Licensing
You can check the license here:
https://github.com/kochlisGit/Deep-Trainer/blob/main/LICENSE

# Snapshots


# Instructions
1. Download all the files.
2. Install Python 3
3. Install the following libraries:
* Numpy
* Opencv
* Tensorflow
* Pygame
* Tkinter
4. Run gui.py

Make sure your webcam is enabled. If You'd like to use an IP Camera, make sure to **set the correct IP_CAMERA_URL at the gui.py file.**

# Camera Position
Make sure You put the camera in the correct position for each exercise. Each exercise requires the camera to be put in the specified position.

* Pushups: Put the camera diagonal-front, so that it can see the both the front and the right side of your body.
* Biceps: Put the camera in front of you.

Your pose is displayed on the screen. You should adjust the distance of the camera, before proceeding to the exercise. Make sure You are not far away from the camera or the camera isn't too close to your body. If the camera is placed in the correct position, the model should be able to recognise all your body's joints during the workout.

If You'd like to change an exercise, You must restart the application.
