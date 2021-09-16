'''
MISTAKE 1. HALF REPS
MISTAKE 2. LOWER BACK UP/DOWN
MISTAKE 3: HEAD UP/DOWN
MISTAKE 4: ELBOWS OUT
MISTAKE 5: WIDE HANDS
MISTAKE 6: HANDS FORWARD-BACKWARD
MISTAKE 7: SPEED
'''

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
from enum import Enum


class Poses(Enum):
    INITIAL = 1
    FINAL = 2
    INVALID = 3


KEY_ESC = 27

INPUT_HEIGHT = 256
INPUT_WIDTH = 256
MODEL_CONFIDENCE = 0.3

CIRCLE_RADIUS = 4
CIRCLE_COLOR = (0, 255, 0)
CIRCLE_THICKNESS = -1
EDGE_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

BODY_EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

NOSE = 0
RIGHT_EAR = 2
RIGHT_SHOULDER = 6
RIGHT_ELBOW = 8
RIGHT_WRIST = 10
RIGHT_HIP = 12
RIGHT_KNEE = 14
RIGHT_ANKLE = 16


# Draws the edges of the connected keypoints on the frame.
def draw_connections(webcam_frame, predicted_keypoints, predefined_edges, confidence_threshold):
    detected_joints = dict()

    # Inverse Scaling of the keypoints.
    height, width, channels = webcam_frame.shape
    rescaled_keypoints = np.multiply(predicted_keypoints, [height, width, 1])

    for (p1, p2) in predefined_edges:
        y1, x1, c1 = rescaled_keypoints[p1]
        y2, x2, c2 = rescaled_keypoints[p2]

        # Drawing the edges if the prediction exceeds the confidence threshold.
        if c1 > confidence_threshold and c2 > confidence_threshold:
            center1 = [int(x1), int(y1)]
            center2 = [int(x2), int(y2)]

            if p1 not in detected_joints:
                detected_joints[p1] = np.array(center1)
                cv2.circle(webcam_frame, center1, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            if p2 not in detected_joints:
                detected_joints[p2] = np.array(center2)
                cv2.circle(webcam_frame, center2, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            cv2.line(webcam_frame, center1, center2, EDGE_COLOR)

    return webcam_frame, detected_joints


# Computes the angle of 3 given joints. Points must be given in order.
def calculate_angle(p1, p2, p3):
    radians = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    joint_angle = np.abs(radians * 180.0 / np.pi)

    if joint_angle > 180.0:
        joint_angle = 360 - joint_angle

    return joint_angle


# Prints the angle on the screen.
def visualize_angle(input_frame, position, joint_angle):
    cv2.putText(
        img=input_frame,
        text=str(joint_angle),
        org=position,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=TEXT_COLOR,
        thickness=2,
        lineType=cv2.LINE_AA
    )


# Detects if the predicted angle is near the expected angle.
def is_boundary_angle(predicted_angle, expected_angle, max_error_radius):
    return expected_angle - max_error_radius <= predicted_angle <= expected_angle + max_error_radius


# Detects if the given joints are in vertical position.
def is_vertical(predicted_joints_x_pos, x_axis_pos, max_error_distance):
    for x in predicted_joints_x_pos:
        if not (x_axis_pos - max_error_distance <= x <= x_axis_pos + max_error_distance):
            return False
    return True


# Detects if the given joints are in horizontal position.
def is_horizontal(predicted_joints_y_pos, y_axis_pos, max_error_distance):
    for y in predicted_joints_y_pos:
        if not (y_axis_pos - max_error_distance <= y <= y_axis_pos + max_error_distance):
            return False
    return True


# Detects the initial pose of the exercise.
def is_initial_pose(
        ear_y, shoulder_x, shoulder_y, elbow_x, elbow_y, wrist_x, wrist_y, hip_y, knee_y, ankle_y,
        shoulder_angle
):
    return ankle_y >= knee_y >= hip_y >= shoulder_y and \
           shoulder_y < elbow_y < wrist_y and \
           is_vertical([shoulder_x, elbow_x, wrist_x], elbow_x, 50) and \
           is_boundary_angle(shoulder_angle, 60, 15) and \
           is_horizontal([shoulder_y, ear_y], shoulder_y, 10)


# Detects the final pose of the exercise.
def is_final_pose(
        nose_y, shoulder_y, hip_y, knee_y, ankle_y, shoulder_angle, elbow_angle
):
    return is_horizontal([ankle_y, knee_y, hip_y, shoulder_y], shoulder_y, 10) and \
            nose_y >= shoulder_y and \
            is_boundary_angle(shoulder_angle, 5, 5) and \
            is_boundary_angle(elbow_angle, 90, 15)


# Detects the current phase of the exercise.
def detect_pose(detected_joints, shoulder_angle, elbow_angle):
    if not (RIGHT_EAR in detected_joints and
            NOSE in detected_joints and
            RIGHT_SHOULDER in detected_joints and
            RIGHT_ELBOW in detected_joints and
            RIGHT_WRIST in detected_joints and
            RIGHT_HIP in detected_joints and
            RIGHT_KNEE in detected_joints and
            RIGHT_ANKLE in detected_joints):
        return Poses.INVALID
    else:
        nose_x, nose_y = detected_joints[NOSE]
        ear_x, ear_y = detected_joints[RIGHT_EAR]
        shoulder_x, shoulder_y = detected_joints[RIGHT_SHOULDER]
        elbow_x, elbow_y = detected_joints[RIGHT_ELBOW]
        wrist_x, wrist_y = detected_joints[RIGHT_WRIST]
        hip_x, hip_y = detected_joints[RIGHT_HIP]
        knee_x, knee_y = detected_joints[RIGHT_KNEE]
        ankle_x, ankle_y = detected_joints[RIGHT_ANKLE]

        if is_initial_pose(
            ear_y, shoulder_x, shoulder_y, elbow_x, elbow_y, wrist_x, wrist_y, hip_y, knee_y, ankle_y,
            shoulder_angle
        ):
            return Poses.INITIAL
        elif is_final_pose(
            nose_y, shoulder_y, hip_y, knee_y, ankle_y, shoulder_angle, elbow_angle
        ):
            return Poses.FINAL


# Loading the model after downloading it from tf-hub.
model = hub.load('../models/movenet_thunder/')
movenet = model.signatures['serving_default']

# Loading video-stream from webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Reading the current frame.
    ret, frame = cap.read()

    # Validating that webcam captured a frame. If True:
    if ret:

        # Reshaping the frame. Movenet Thunder accepts 256x256x3 as input images.
        image = tf.expand_dims(frame, axis=0)
        reshaped_frame = tf.image.resize_with_pad(image, INPUT_HEIGHT, INPUT_WIDTH)
        input_image = tf.cast(reshaped_frame, dtype=tf.int32)

        # Predicting Key-Points with Movenet.
        outputs = movenet(input_image)

        # The y, x outputs of keypoints are normalized to [0.0, 1.0]. Rescaling is required.
        keypoints = np.squeeze(outputs['output_0'])
        frame, joints = draw_connections(frame, keypoints, BODY_EDGES, 0.3)

        if RIGHT_ELBOW in joints and RIGHT_SHOULDER in joints and RIGHT_HIP in joints:
            shoulder_angle = calculate_angle(joints[RIGHT_ELBOW], joints[RIGHT_SHOULDER], joints[RIGHT_HIP])
            visualize_angle(frame, joints[RIGHT_SHOULDER], int(shoulder_angle))

            if RIGHT_WRIST in joints:
                elbow_angle = calculate_angle(joints[RIGHT_WRIST], joints[RIGHT_ELBOW], joints[RIGHT_SHOULDER])
                visualize_angle(frame, joints[RIGHT_ELBOW], int(elbow_angle))

                current_pose = detect_pose(joints, shoulder_angle, elbow_angle)
                if current_pose == Poses.INITIAL:
                    print('Found Initial Pose!!')
                elif current_pose == Poses.FINAL:
                    print('Found Final Pose!!')

        cv2.imshow('Movenet Thunder', frame)

    key = cv2.waitKey(1)
    if key == KEY_ESC:
        break

cap.release()
cv2.destroyAllWindows()
