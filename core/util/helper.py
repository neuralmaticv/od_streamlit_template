import base64
import os

import cv2
import numpy as np


def encode_frame(frame: np.ndarray) -> tuple:
    """Encode a frame.

    Args:
        frame: A numpy array representing a frame.

    Returns:
        A tuple containing the shape of the frame and the encoded frame as a string.

    Note:
        The frame is encoded using base64 encoding.
    """
    shape = frame.shape
    arr = base64.b64encode(frame.tobytes()).decode('utf-8')
    return shape, arr

def decode_frame(arr: str, shape: tuple) -> np.ndarray:
    """Decodes a base64 encoded string and reshapes it into a numpy array.

    Args:
        arr: A base64 encoded string.
        shape: A tuple specifying the shape of the resulting numpy array.

    Returns:
        A numpy array with the specified shape.

    Raises:
        ValueError: If the shape does not match the dimensions of the decoded array.
    """
    vec = np.frombuffer(base64.b64decode(arr), dtype=np.uint8).reshape(
        shape[0], shape[1], shape[2])
    return vec

def save_image(np_img: np.ndarray, output: str, source_name: str) -> None:
    """Saves an image to a specified location.

    Args:
        np_img: NumPy array representing the image
        output: Path to the output directory
        source_name: Name of the image source

    Returns:
        None
    """

    output_path = os.path.join(output, f"{source_name}.jpg")

    cv2.imwrite(output_path, cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR))

