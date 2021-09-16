import tensorflow as tf
import tensorflow_hub as hub
import numpy as np


class Model:
    def __init__(self, model_dir, model_input_dims, image_dims):
        model = hub.load(model_dir)
        self._model_signatures = model.signatures['serving_default']
        self._height, self._width = model_input_dims
        self._image_height, self._image_width = image_dims

    # Resizes the frame to match the model's input dimension.
    def _resize_frame(self, frame):
        frame_array = tf.expand_dims(frame, axis=0)
        resized_frame = tf.image.resize_with_pad(frame_array, self._height, self._width)
        model_input = tf.cast(resized_frame, dtype=tf.int32)
        return model_input

    # Captures a new frame and detects the joints in the image.
    def detect_keypoints(self, frame):
        model_input = self._resize_frame(frame)
        outputs = self._model_signatures(model_input)
        keypoints = np.squeeze(outputs['output_0'])
        rescaled_keyponts = np.multiply(keypoints, [self._image_height, self._image_width, 1])
        return rescaled_keyponts
