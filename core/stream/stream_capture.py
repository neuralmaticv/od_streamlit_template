from datetime import datetime
from vidgear.gears import CamGear


class StreamCapture:
    """A class to capture and read frames from a video stream.

    Attributes:
        rtsp_url : URL of the RTSP stream
        reset_attempts : number of re-connection attempts before giving up
        reset_delay : delay in seconds between re-connection attempts
        source : CamGear object to capture frames from the stream
        running : flag to indicate if the stream is running or not

    Methods:
        read() : Read a frame from the stream. Returns None if the stream is not available or if the maximum number of re-connection attempts has been reached.
        stop() : Stop the stream capture.
    """
    def __init__(self, rtsp_url, reset_attempts=20, reset_delay=5):
        """Initialize a class instance.

        Args:
            rtsp_url: The RTSP URL of the camera feed.
            reset_attempts: The number of attempts to reset the camera feed if it fails.
            reset_delay: The delay in seconds between each reset attempt.

        Attributes:
            rtsp_url: The RTSP URL of the camera feed.
            reset_attempts: The number of attempts to reset the camera feed if it fails.
            reset_delay: The delay in seconds between each reset attempt.
            source: The camera feed source.
            running: A boolean indicating if the camera feed is running.
        """
        self.rtsp_url = rtsp_url
        self.reset_attempts = reset_attempts
        self.reset_delay = reset_delay
        options = {"THREADED_QUEUE_MODE": False}
        self.source = CamGear(source=self.rtsp_url, colorspace="COLOR_BGR2RGB",
                              **options).start()
        self.running = True

    def read(self):
        """Start reading frames from the stream.

        Returns:
            A frame from the stream if the stream is available and the maximum number of re-connection attempts has not been reached. Otherwise, returns None.
        """
        if self.source is None:
            return None
        
        if self.running and self.reset_attempts > 0:
            frame = self.source.read()

            if frame is None:
                self.source.stop()
                self.reset_attempts -= 1
                print(
                    "re-connection attempt-{} at time:{}".format(
                        str(self.reset_attempts),
                        datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"),
                    )
                )

                options = {"THREADED_QUEUE_MODE": False}
                self.source = CamGear(source=self.rtsp_url, colorspace="COLOR_BGR2RGB",
                                      **options).start()

                return frame
            else:
                return frame
        
        return None

    def stop(self):
        """Stop the stream capture.

        Returns:
            None
        """
        self.running = False
        self.reset_attempts = 0
        if self.source is not None:
            self.source.stop()
