import os
# TODO: setup parameters in this file

PROJECT_NAME = "Template"
API_ADDRESS = "http://localhost:8001"
API_HOST = "localhost"
API_PORT = 8001

COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
}

USER_ROOT = os.path.expanduser('~')
PROJECT_DIR = os.path.join(USER_ROOT, 'project_dir')   
APP_DIR = os.path.join(PROJECT_DIR, 'app')
CORE_DIR = os.path.join(PROJECT_DIR, 'core')
DATA_DIR = os.path.join(CORE_DIR, 'data')
DATA_OUTPUT = os.path.join(DATA_DIR, 'output')

TEMP_LOG_OUT = os.path.join(DATA_DIR, 'log')
TEMP_IMAGE_OUT = os.path.join(DATA_OUTPUT, 'image')
TEMP_VIDEO_OUT = os.path.join(DATA_OUTPUT, 'video')
TEMP_STREAM_OUT = os.path.join(DATA_OUTPUT, 'stream')
