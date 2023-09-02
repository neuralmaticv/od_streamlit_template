import time
from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from util.helper import *
from stream.stream_capture import StreamCapture

import logging
logger = logging.getLogger("core")


class ModelConfig(BaseModel):
    """A class to represent the configuration of a model.

    Attributes:
        model_path : path to the model
        device : device to use for running the model
        classes : list of classes for the model
        confidence_threshold : threshold for confidence score
        iou_threshold : threshold for intersection over union score
    """
    model_path: str
    device: str
    classes: list
    confidence_threshold: float
    iou_threshold: float

class Processing(BaseModel):
    """A class to represent processing information.

    Attributes:
        detection : float value representing detection information
        recognition : float value representing recognition information
    """
    detection: float
    recognition: float

class Box(BaseModel):
    """A class to represent a box.

    Attributes:
        xmin : minimum x-coordinate of the box
        ymin : minimum y-coordinate of the box
        xmax : maximum x-coordinate of the box
        ymax : maximum y-coordinate of the box
    """
    xmin: int
    ymin: int
    xmax: int
    ymax: int

class Result(BaseModel):
    """A class to represent a result.

    Attributes:
        box : an instance of the Box class
        d_score : a float representing the score for detection
    """
    box: Box
    d_score: float

class Response(BaseModel):
    """A class representing the response from frame processing.

    Attributes:
        processing_time : processing time of the frame
        results : list of results from the frame
        filename : name of the file
        camera_id : optional camera ID
        timestamp : timestamp of the processing
    """
    processing_time: Processing
    results: List[Result]
    filename: str
    camera_id: Optional[str] = None
    timestamp: str

class StreamConfig(BaseModel):
    """A class to represent a stream configuration.

    Attributes:
        stream_url : URL of the stream
    """
    stream_url: str

class Frame(BaseModel):
    """A class to represent a frame.

    Attributes:
        frame : the frame string
    """
    frame: str

class Camera(str, Enum):
    """A class to represent camera locations.
    """
    test = "test"
    # TODO: add camera locations

def create_response(np_img, results, start_det_time, end_det_time, source, source_name):
    # TODO: create Response object from results
    pass
    

cv_router = APIRouter(
    prefix="/cv",
    tags=["main"]
)

@cv_router.get("/")
async def index():
    """Index route."""
    return {"message": "Template API"}

@cv_router.post("/set_config/")
async def set_config(model_config: ModelConfig):
    logger.info("Setting config...")
    # TODO: implement your code here
    pass

@cv_router.post("/infer_image", response_model=Response)
async def infer_image(file: UploadFile = File(...)):
    # TODO: implement your code here
    pass

def infer_stream(rtsp_url, camera):
    prev = 0
    FPS = 60 # how often to read from the stream

    stream = StreamCapture(rtsp_url, reset_attempts=2, reset_delay=5)

    while True:
        time_elapsed = time.time() - prev 

        rframe = stream.read()

        if time_elapsed > 1./FPS:
            prev = time.time()
            # TODO: implement your code here, use the infer_image function to process the frame
            # TODO: use the create_response function to create a Response object and return it
            pass

@cv_router.get("/{camera}/infer_stream")
def infer_camera_stream(camera: Camera):
    # TODO: implement your code here
    pass