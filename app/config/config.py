import os
# TODO: setup parameters in this file

PROJECT_NAME = "Template"
API_ADDRESS = "http://localhost:8001"

COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
}

USER_ROOT = os.path.expanduser('~')
PROJECT_DIR = os.path.join(USER_ROOT, 'project_dir')   
APP_DIR = os.path.join(PROJECT_DIR, 'app')
CORE_DIR = os.path.join(PROJECT_DIR, 'core')

TEMP_IMG = os.path.join(CORE_DIR, 'data', 'uploads', 'image')
TEMP_IMG_OUT = os.path.join(TEMP_IMG, 'out')

TEMP_VIDEO = os.path.join(CORE_DIR, 'data', 'uploads', 'video')
TEMP_VIDEO_OUT = os.path.join(TEMP_VIDEO, 'out')

TEMP_STREAM = os.path.join(CORE_DIR, 'data', 'uploads', 'stream')
TEMP_STREAM_OUT = os.path.join(TEMP_STREAM , 'out')

MODEL_PATH = os.path.join(CORE_DIR, 'models', 'model_pth')

DEFAULT_DEVICE = "cpu"
CLASS_NAME0 = {"id": 0, "name": "class0"}
CLASS_NAME1 = {"id": 1, "name": "class1"}
CLASSES = [CLASS_NAME0, CLASS_NAME1]

MIN_CONFIDENCE_THRESHOLD = 0.0
MAX_CONFIDENCE_THRESHOLD = 1.0
DEFAULT_CONFIDENCE_THRESHOLD = 0.85

MIN_IOU_THRESHOLD = 0.0
MAX_IOU_THRESHOLD = 1.0
DEFAULT_IOU_THRESHOLD = 0.5

MODELS = {
    "model_id": {
        "model_path": "",
        "device": DEFAULT_DEVICE,
        "classes": CLASSES,
        "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD,
        "iou_threshold": DEFAULT_IOU_THRESHOLD
    }
}

DEFAULT_CONFIG = MODELS["model_id"]

RTSP_PORT = 554
ENDPOINT = "live"

STREAMS = {
    "": "none",
    "stream0": {
        "username": "",
        "password": "",
        "address": "",
        "port": RTSP_PORT,
        "endpoint": ENDPOINT
    },
}

SOURCES = {
    "": "none",
    "Image": "image",
    "Video": "video",
    "Stream": STREAMS
}
