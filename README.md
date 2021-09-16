# Deep-Trainer
Monitor Your Workout through a Webcam/IP Camera. No equipment is required, other than a camera and a laptop. This application could potentially replace a personal trainer, making it the idea app for workout.

# Features
* GUI (Graphical User Interface) in which You can select the video stream and an exercise.
* Notification Sound when you complete a repetition correctly.
* Realtime detection and demonstration of the pose of your body.
* Warnings when You are doing the exercise too fast.
* Text messages on the screen, when your pose is incorrect.

# Licensing
You can check the license here:
https://github.com/kochlisGit/Deep-Trainer/blob/main/LICENSE.md

# Screenshots
![](https://github.com/kochlisGit/Deep-Trainer/blob/main/screenshots/Screenshot%20from%202021-09-16%2016-22-01.png)
![](https://github.com/kochlisGit/Deep-Trainer/blob/main/screenshots/Screenshot%20from%202021-09-16%2016-22-03.png)
![](https://github.com/kochlisGit/Deep-Trainer/blob/main/screenshots/bicep_corrent.png)
![](https://github.com/kochlisGit/Deep-Trainer/blob/main/screenshots/not_vertical_arm.png)

# Frameworks
The program is writen in python. The pose-estimation model is "Movenet Thunder/Lightning provided by Tensorflow". The GUI is built with Tkinter and the visualization of the pose is made using Opencv.

# Demo
We have uploaded videos on Youtube, on which we demonstrate how the application works. You can view those videos here:
https://www.youtube.com/watch?v=fAHbx8wz7ko&ab_channel=NikolasGaripis
https://youtu.be/l3II62ebGZ4
https://youtu.be/kUw_1Pwyo-Q
https://youtu.be/NjcsrHjAWa0

# Performance
According to Tensorflow's Movenet Thunder model, it achieves states of the art results, while maintaining very fast execution speed. More specifically, It can estimate a pose at about 72% accurately at 30 fps. Movenet lightning, while it can operate in 60 fps, It has lower accuracy. The model is tested of both GPU GTX 970 and with an Intel i5 CPU.

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

# Contributors
* Vasileios Kochliaridis
* Nikolaos Gkaripis
* Antonios Koutsouras
* Stathis Moustakas
