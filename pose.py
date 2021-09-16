import cv2
import numpy as np
from enum import Enum

_default_config = {
    'joint_size': 4,
    'joint_color': (255, 255, 255),
    'joint_thickness': 2,
    'edge_color': (255, 0, 0),
    'text_color': (0, 255, 0),
    'text_scale': 4.0
}


class Pose(Enum):
    INITIAL = 1
    FINAL = 2
    INVALID = 3


class PoseDetector:
    def __init__(self, config, confidence, exercise):
        self._config = _default_config
        self._confidence = confidence
        self._exercise = exercise
        self._exercise_joints = exercise.required_joints
        self._current_pose = Pose.INVALID

        for configuration in config:
            self._config[configuration] = config[configuration]

        self._body_edges = {
            (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6),
            (5, 7), (7, 9), (6, 8), (8, 10), (5, 6), (5, 11),
            (6, 12), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)
        }

    # Returns a dictionary with all the detected joints in the frame.
    def get_detected_joints(self, keypoints):
        joints = dict()

        for i, (y, x, c) in enumerate(keypoints):
            if c >= self._confidence:
                joints[i] = (int(x), int(y))
        return joints

    # Draws the human joints and their connections on the frame.
    def draw_keypoints(self, frame, joints):
        for p1, p2 in self._body_edges:
            p1_in_joints = p1 in joints
            p2_in_joints = p2 in joints
            center1 = None
            center2 = None

            if p1_in_joints:
                center1 = joints[p1]
                cv2.circle(
                    frame,
                    center1,
                    self._config['joint_size'],
                    self._config['joint_color'],
                    self._config['joint_thickness']
                )
            if p2_in_joints:
                center2 = joints[p2]
                cv2.circle(
                    frame,
                    center2,
                    self._config['joint_size'],
                    self._config['joint_color'],
                    self._config['joint_thickness']
                )
            if p1_in_joints and p2_in_joints:
                cv2.line(frame, center1, center2, self._config['edge_color'], self._config['joint_thickness'])

    # Computes the pose similarity of 2 different poses, using the Mean Absolute Error Method.
    def compute_pose_similarity(self, joints1, joints2):
        if len(joints2) == len(self._exercise_joints):
            mae = 0
            for j in self._exercise_joints:
                mae += abs(np.linalg.norm(np.array(joints1[j]) - np.array(joints2[j])))
            return mae
        else:
            return 10000

    # Detects the current pose.
    def detect_pose(self, joints):
        if self._exercise_joints.issubset(joints.keys()):

            is_initial, initial_warning = self._exercise.initial_pose(joints)
            if is_initial:
                self._exercise.set_initial_pose(joints)
                return Pose.INITIAL, None

            is_final, final_warning = self._exercise.final_pose(joints)
            if is_final:
                self._exercise.set_final_pose(joints)
                return Pose.FINAL, None

            if initial_warning is not None or final_warning is not None:
                initial_sim_score = self.compute_pose_similarity(joints, self._exercise.initial_joints_pos)
                final_sim_score = self.compute_pose_similarity(joints, self._exercise.final_joints_pos)

                if initial_sim_score < final_sim_score:
                    if initial_sim_score < 250:
                        return Pose.INVALID, initial_warning
                else:
                    if final_sim_score < 250:
                        return Pose.INVALID, final_warning

        return Pose.INVALID, None

    # Updates the current pose of the body.
    def update_pose(self, detected_pose):
        if detected_pose != Pose.INVALID and detected_pose != self._current_pose:
            self._current_pose = detected_pose
            print('POSE SET TO', detected_pose)

    # Detects whether there has been a repetition of the exercise.
    def detect_repetition(self, detected_pose):
        return self._current_pose == Pose.INITIAL and detected_pose == Pose.FINAL

    # Gets the current progress of the pose.
    def get_progress(self, joints, detected_pose):
        if self._current_pose != Pose.INVALID:
            if detected_pose == Pose.INITIAL:
                return 0
            elif detected_pose == Pose.FINAL or self._current_pose == Pose.FINAL:
                return 100
            else:
                if self._exercise_joints.issubset(joints.keys()):
                    progress = self._exercise.get_progress(joints)
                    return progress
        return None
