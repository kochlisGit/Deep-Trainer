from urllib import request
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2

ip_cam_url = "http://192.168.1.29:8080/shot.jpg"

KEY_ESC = 27

INPUT_HEIGHT = 192
INPUT_WIDTH = 192
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

NOSE_ID = 0
RIGHT_EAR = 2
RIGHT_SHOULDER = 6
RIGHT_ELBOW = 8
RIGHT_WRIST = 10
RIGHT_HIP = 12
RIGHT_KNEE = 14
RIGHT_ANKLE = 16


# Draws the edges of the connected keypoints on the frame.
def draw_connections(webcam_frame, predicted_keypoints, predefined_edges, confidence_threshold):
    detected_joins = dict()

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

            if p1 not in detected_joins:
                detected_joins[p1] = np.array(center1)
                cv2.circle(webcam_frame, center1, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            if p2 not in detected_joins:
                detected_joins[p2] = np.array(center2)
                cv2.circle(webcam_frame, center2, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

            cv2.line(webcam_frame, center1, center2, EDGE_COLOR)

    return webcam_frame, detected_joins


# Computes the angle of 3 given joints. Points must be given in order.
def calculate_angle(p1, p2, p3):
    radians = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    joint_angle = np.abs(radians*180.0/np.pi)

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


# Loading the model after downloading it from tf-hub.
model = hub.load('models/movenet_lightning/')
movenet = model.signatures['serving_default']

while True:
    frame_array = np.array(bytearray(request.urlopen(ip_cam_url).read()), dtype=np.uint8)
    frame = cv2.imdecode(frame_array, -1)

    # Reshaping the frame. Movenet accepts 192x192x3 as input images.
    image = tf.expand_dims(frame, axis=0)
    reshaped_frame = tf.image.resize_with_pad(image, INPUT_HEIGHT, INPUT_WIDTH)
    input_image = tf.cast(reshaped_frame, dtype=tf.int32)

    # Predicting Key-Points with Movenet.
    outputs = movenet(input_image)

    # The y, x outputs of keypoints are normalized to [0.0, 1.0]. Rescaling is required.
    keypoints = np.squeeze(outputs['output_0'])
    frame, joints = draw_connections(frame, keypoints, BODY_EDGES, 0.3)

    if RIGHT_ELBOW in joints and RIGHT_SHOULDER in joints and RIGHT_HIP in joints:
        angle = calculate_angle(joints[RIGHT_ELBOW], joints[RIGHT_SHOULDER], joints[RIGHT_HIP])
        visualize_angle(frame, joints[RIGHT_SHOULDER], int(angle))

    cv2.imshow('Movenet Thunder', frame)

    if cv2.waitKey(1) == KEY_ESC:
        break
cv2.destroyAllWindows()
