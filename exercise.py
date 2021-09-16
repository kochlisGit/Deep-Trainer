import utils

_NOSE = 0
_RIGHT_EAR = 2
_RIGHT_SHOULDER = 6
_RIGHT_ELBOW = 8
_RIGHT_WRIST = 10
_RIGHT_HIP = 12
_RIGHT_KNEE = 14
_RIGHT_ANKLE = 16


class Exercise:
    def __init__(self, name, required_joints):
        self.name = name
        self.required_joints = required_joints
        self.initial_joints_pos = dict()
        self.final_joints_pos = dict()

    def set_initial_pose(self, joints):
        for joint_id in self.required_joints:
            x, y = joints[joint_id]
            self.initial_joints_pos[joint_id] = [x, y]

    def set_final_pose(self, joints):
        for joint_id in self.required_joints:
            x, y = joints[joint_id]
            self.final_joints_pos[joint_id] = [x, y]

    # Detects if the initial pose is captured.
    def initial_pose(self, joints):
        pass

    # Detects if the final pose is captured.
    def final_pose(self, joints):
        pass

    # Gets the current progress of the pose, according to the initial pose.
    def get_progress(self, joints):
        pass


class PushUps(Exercise):
    def __init__(self):
        required_joints = {
            _NOSE, _RIGHT_EAR, _RIGHT_SHOULDER, _RIGHT_ELBOW, _RIGHT_WRIST, _RIGHT_HIP, _RIGHT_KNEE, _RIGHT_ANKLE
        }
        super().__init__('Push Ups', required_joints)

    def initial_pose(self, joints):
        ankle_x, ankle_y = joints[_RIGHT_ANKLE]
        knee_x, knee_y = joints[_RIGHT_KNEE]
        hip_x, hip_y = joints[_RIGHT_HIP]
        shoulder_x, shoulder_y = joints[_RIGHT_SHOULDER]
        elbow_x, elbow_y = joints[_RIGHT_ELBOW]
        wrist_x, wrist_y = joints[_RIGHT_WRIST]
        ear_y = joints[_RIGHT_EAR][1]

        shoulder_angle = utils.calculate_angle(joints[_RIGHT_ELBOW], joints[_RIGHT_SHOULDER], joints[_RIGHT_HIP])

        if not (ankle_y >= knee_y >= hip_y > shoulder_y):
            return False, '-- Non Diagonal Side --'
        if utils.horizontal_joints([hip_y, shoulder_y], hip_y, 5):
            return False, '-- Misplaced Back --'
        if not (ankle_x < knee_x < hip_x < shoulder_x):
            return False, '-- Vertical Core --'
        if not (shoulder_y < elbow_y < wrist_y):
            return False, '-- Non Vertical Arms --'
        if not utils.vertical_joints([shoulder_x, elbow_x, wrist_x], elbow_x, 50):
            return False, '-- Non Vertical Arms'
        if not utils.angle_in_region(shoulder_angle, 60, 15):
            return False, '-- Misplaced Arms --'
        if not utils.horizontal_joints([shoulder_y, ear_y], shoulder_y, 10):
            return False, '-- Misplaced head --'

        return True, None

    def final_pose(self, joints):
        ankle_x, ankle_y = joints[_RIGHT_ANKLE]
        knee_x, knee_y = joints[_RIGHT_KNEE]
        hip_x, hip_y = joints[_RIGHT_HIP]
        shoulder_x, shoulder_y = joints[_RIGHT_SHOULDER]
        nose_y = joints[_NOSE][1]

        shoulder_angle = utils.calculate_angle(joints[_RIGHT_ELBOW], joints[_RIGHT_SHOULDER], joints[_RIGHT_HIP])
        elbow_angle = utils.calculate_angle(joints[_RIGHT_WRIST], joints[_RIGHT_ELBOW], joints[_RIGHT_SHOULDER])

        if not(ankle_x < knee_x < hip_x < shoulder_x):
            return False, '-- Vertical Core --'
        if not utils.horizontal_joints([ankle_y, knee_y, hip_y, shoulder_y], shoulder_y, 25):
            return False, '-- Chest too High --'
        if not (nose_y >= shoulder_y):
            return False, '-- Head too High --'
        if not utils.angle_in_region(shoulder_angle, 15, 15):
            return False, '-- Core too High --'
        if not utils.angle_in_region(elbow_angle, 70, 20):
            return False, '-- Elbow not Bending Enough --'

        return True, None

    def get_progress(self, joints):
        init_ankle_x, init_ankle_y = self.initial_joints_pos[_RIGHT_ANKLE]
        init_knee_x, init_knee_y = self.initial_joints_pos[_RIGHT_KNEE]
        init_hip_x, init_hip_y = self.initial_joints_pos[_RIGHT_HIP]

        ankle_x, ankle_y = joints[_RIGHT_ANKLE]
        knee_x, knee_y = joints[_RIGHT_KNEE]
        hip_x, hip_y = joints[_RIGHT_HIP]

        if utils.joint_in_region(ankle_x, ankle_y, init_ankle_x, init_ankle_y, 20, 20) and \
                utils.joint_in_region(knee_x, knee_y, init_knee_x, init_knee_y, 20, 20) and \
                utils.joint_in_region(hip_x, hip_y, init_hip_x, init_hip_y, 20, 40):

            init_shoulder_angle = utils.calculate_angle(
                self.initial_joints_pos[_RIGHT_ELBOW],
                self.initial_joints_pos[_RIGHT_SHOULDER],
                self.initial_joints_pos[_RIGHT_HIP],
            )
            current_shoulder_angle = utils.calculate_angle(
                joints[_RIGHT_ELBOW],
                joints[_RIGHT_SHOULDER],
                joints[_RIGHT_HIP]
            )
            expected_shoulder_angle = 10

            progress = (init_shoulder_angle - current_shoulder_angle) / (init_shoulder_angle - expected_shoulder_angle)
            return int(progress * 100)
        return None


class Biceps(Exercise):
    def __init__(self):
        required_joints = {
            _RIGHT_SHOULDER, _RIGHT_ELBOW, _RIGHT_WRIST
        }
        super().__init__('Biceps', required_joints)

    def initial_pose(self, joints):
        shoulder_x, shoulder_y = joints[_RIGHT_SHOULDER]
        elbow_x, elbow_y = joints[_RIGHT_ELBOW]
        wrist_x, wrist_y = joints[_RIGHT_WRIST]

        elbow_angle = utils.calculate_angle(joints[_RIGHT_WRIST], joints[_RIGHT_ELBOW], joints[_RIGHT_SHOULDER])

        if not (wrist_y > elbow_y > shoulder_y):
            return False, '-- Arm not Vertical --'
        if not utils.vertical_joints([shoulder_x, elbow_x, wrist_x], shoulder_x, 20):
            return False, '-- Arm not Vertical --'
        if not utils.angle_in_region(elbow_angle, 180, 10):
            return False, '-- Elbow Bends too Much --'

        return True, None

    def final_pose(self, joints):
        shoulder_x, shoulder_y = joints[_RIGHT_SHOULDER]
        elbow_x, elbow_y = joints[_RIGHT_ELBOW]
        wrist_x, wrist_y = joints[_RIGHT_WRIST]

        if not utils.vertical_joints([shoulder_x, elbow_x, wrist_x], elbow_x, 20):
            return False, '-- Arm not Vertical --'
        if not utils.joint_in_region(wrist_x, wrist_y, shoulder_x, shoulder_y, 15, 15):
            return False, '-- Wrist away from Shoulder --'

        return True, None

    def get_progress(self, joints):
        initial_elbow_angle = utils.calculate_angle(
            self.initial_joints_pos[_RIGHT_WRIST],
            self.initial_joints_pos[_RIGHT_ELBOW],
            self.initial_joints_pos[_RIGHT_SHOULDER]
        )
        current_elbow_angle = utils.calculate_angle(
            joints[_RIGHT_WRIST],
            joints[_RIGHT_ELBOW],
            joints[_RIGHT_SHOULDER]
        )
        expected_elbow_angle = 50
        progress = (initial_elbow_angle - current_elbow_angle) / (initial_elbow_angle - expected_elbow_angle)
        return int(progress * 100)


class Squats(Exercise):
    def __init__(self):
        required_joints = {
            _NOSE, _RIGHT_EAR, _RIGHT_SHOULDER, _RIGHT_ELBOW, _RIGHT_WRIST, _RIGHT_HIP, _RIGHT_KNEE, _RIGHT_ANKLE
        }
        super().__init__('Squats', required_joints)

    def initial_pose(self, joints):
        pass

    def final_pose(self, joints):
        pass

    def get_progress(self, joints):
        pass


class KneeCrunches(Exercise):
    def __init__(self):
        required_joints = {
            _NOSE, _RIGHT_EAR, _RIGHT_SHOULDER, _RIGHT_ELBOW, _RIGHT_WRIST, _RIGHT_HIP, _RIGHT_KNEE, _RIGHT_ANKLE
        }
        super().__init__('Knee Crunches', required_joints)

    def initial_pose(self, joints):
        pass

    def final_pose(self, joints):
        pass

    def get_progress(self, joints):
        pass
