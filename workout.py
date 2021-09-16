from model import Model
from pose import PoseDetector, Pose
from urllib import request
import numpy as np
import cv2
import utils
import time

_KEY_ESC = 27

_MODEL_DIMS = (256, 256)

_MODEL_DIR = 'models/movenet_thunder'
_MODEL_CONFIDENCE = 0.3
_SOUND_FILEPATH = 'sounds/reward.ogg'


class WorkoutPlan:
    def __init__(self, image_dims, config, exercise):
        self._model = Model('models/movenet_thunder', _MODEL_DIMS, image_dims)
        self._pose_detector = PoseDetector(config, _MODEL_CONFIDENCE, exercise)
        self._exercise_name = exercise.name
        self._reps_counter = 0
        self._rep_time_counter = 0

    def _display_workout(self, frame):
        keypoints = self._model.detect_keypoints(frame)
        joints = self._pose_detector.get_detected_joints(keypoints)

        self._pose_detector.draw_keypoints(frame, joints)
        detected_pose, warning = self._pose_detector.detect_pose(joints)

        if detected_pose == Pose.INITIAL:
            self._rep_time_counter = time.time()

        if self._pose_detector.detect_repetition(detected_pose):
            current_time = time.time()

            if current_time - self._rep_time_counter >= 1.2:
                self._reps_counter += 1
                utils.play_reward(_SOUND_FILEPATH)
            else:
                print('FAST MOVEMENT')
                utils.display_message(frame, '-- Fast Movement --', (550, 380))
        else:
            progress = self._pose_detector.get_progress(joints, detected_pose)

            if progress is not None:
                progress_str = str(progress) + '%'
                utils.display_message(frame, progress_str, (520, 380))

        self._pose_detector.update_pose(detected_pose)

        if warning is not None:
            utils.display_message(frame, warning, (10, 400), color=(0, 0, 255))

        utils.display_message(frame, str(self._reps_counter), (560, 100))
        cv2.imshow(self._exercise_name, frame)

    def play_from_webcam(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                self._display_workout(frame)

            key = cv2.waitKey(1)
            if key == _KEY_ESC:
                break

        cap.release()
        cv2.destroyAllWindows()

    def play_from_ip_cam(self, ip_camera_url):
        while True:
            frame_array = np.array(bytearray(request.urlopen(ip_camera_url).read()), dtype=np.uint8)
            frame = cv2.imdecode(frame_array, -1)

            self._display_workout(frame)

            if cv2.waitKey(1) == _KEY_ESC:
                break
        cv2.destroyAllWindows()