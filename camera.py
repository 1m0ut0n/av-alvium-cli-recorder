# flake8: noqa: E501
from vmbpy import VmbSystem
from utils import cleanup_after_exception

# TODO: Add a Camera interface to use different type of cameras (maybe to support the PC webcam or the Basler cameras?).


class AlviumCamera:
    """Class to handle the Allied Vision Alvium Camera."""

    def __init__(self):
        """Initialize"""
        self.__camera = None
        self.__vmb_syst = None

    def __enter__(self):
        """
        Initialize the first Allied Vision Alvium Camera found by the VmbSystem.
        We also configure the camera to use the maximum framerate that she can support and do not use auto exposure.
        """
        # Initialize the VmbSystem instance
        self.__vmb_syst = VmbSystem.get_instance()
        self.__vmb_syst.__enter__()  # <-- Ajout pour entrer dans le contexte VmbSystem
        try:
            # Get a list of all the connected cameras
            cameras = self.__vmb_syst.get_all_cameras()
            if not cameras:
                raise RuntimeError(
                    "No Alvium camera found. Please check that the camera is correctly connected."
                )
            # Choose the first that is found and configure it
            self.__camera = cameras[0]
            try:
                self.__camera.__enter__()  # <-- Enter the camera context
                self.__camera.AcquisitionFrameRateEnable.set(
                    False
                )  # So that it always use the maximum available value
                self.__camera.ExposureAuto.set("Off")
                self.__camera.BinningSelector.set("Sensor")
                self.__camera.BinningHorizontal.set(
                    1
                )  # Needed to change to average binning
                self.__camera.BinningVertical.set(
                    1
                )  # Needed to change to average binning
                self.__camera.BinningHorizontalMode.set(
                    "Average"
                )  # TODO: Make sure that average mode don't make us lose some exposure
            except Exception as e:
                self.__camera.__exit__(None, None, None)
                self.__camera = None
                raise e
        except Exception as e:
            self.__vmb_syst.__exit__(None, None, None)
            self.__vmb_syst = None
            self.__camera = None
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Release the camera and VmbSystem instance."""
        if self.__camera:
            self.__vmb_syst.__exit__(None, None, None)
            self.__camera = None
        if self.__vmb_syst:
            self.__vmb_syst.__exit__(exc_type, exc_value, traceback)
            self.__vmb_syst = None

    @property
    @cleanup_after_exception
    def current_fps(self) -> float:
        """Get the current FPS of the camera."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.AcquisitionFrameRate.get()

    @property
    @cleanup_after_exception
    def fps_range(self) -> tuple[float, float]:
        """Get the range of FPS supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.AcquisitionFrameRate.get_range()

    @property
    @cleanup_after_exception
    def shutter_speed(self) -> float:
        """Get the current shutter speed in microseconds."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.ExposureTime.get()

    @shutter_speed.setter
    @cleanup_after_exception
    def shutter_speed(self, value: float):
        """Set the shutter speed in microseconds."""
        self.__check_camera_and_vmbsyst()
        exposure_range = self.__camera.ExposureTime.get_range()
        if value < exposure_range[0] or value > exposure_range[1]:
            raise ValueError(
                f"Shutter speed must be within the range {exposure_range}."
            )
        self.__camera.ExposureTime.set(value)

    @property
    @cleanup_after_exception
    def shutter_speed_range(self) -> tuple[float, float]:
        """Get the range of shutter speeds supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.ExposureTime.get_range()

    @property
    @cleanup_after_exception
    def image_height(self) -> int:
        """Get the current image height in pixels."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Height.get()

    @property
    @cleanup_after_exception
    def image_height_increment(self) -> int:
        """Get the increment for image height in pixels in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Height.get_increment()

    @property
    @cleanup_after_exception
    def image_height_range(self) -> tuple[int, int]:
        """Get the range of image heights supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Height.get_range()

    @image_height.setter
    @cleanup_after_exception
    def image_height(self, value: int):
        """Set the image height in pixels."""
        self.__check_camera_and_vmbsyst()
        height_increment = self.__camera.Height.get_increment()
        if value % height_increment != 0:
            raise ValueError(f"Image height must be a multiple of {height_increment}.")
        height_range = self.__camera.Height.get_range()
        if value < height_range[0] or value > height_range[1]:
            raise ValueError(f"Image height must be within the range {height_range}.")
        self.__camera.Height.set(value)

    @property
    @cleanup_after_exception
    def image_height_range(self) -> tuple[int, int]:
        """Get the range of image heights supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Height.get_range()

    @property
    @cleanup_after_exception
    def image_width(self) -> int:
        """Get the current image width in pixels."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Width.get()

    @property
    @cleanup_after_exception
    def image_width_increment(self) -> int:
        """Get the increment for image width in pixels in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Width.get_increment()

    @property
    @cleanup_after_exception
    def image_width_range(self) -> tuple[int, int]:
        """Get the range of image widths supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Width.get_range()

    @image_width.setter
    @cleanup_after_exception
    def image_width(self, value: int):
        """Set the image width in pixels."""
        self.__check_camera_and_vmbsyst()
        width_increment = self.__camera.Width.get_increment()
        if value % width_increment != 0:
            raise ValueError(f"Image width must be a multiple of {width_increment}.")
        width_range = self.__camera.Width.get_range()
        if value < width_range[0] or value > width_range[1]:
            raise ValueError(f"Image width must be within the range {width_range}.")
        self.__camera.Width.set(value)

    @property
    @cleanup_after_exception
    def image_width_range(self) -> tuple[int, int]:
        """Get the range of image widths supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.Width.get_range()

    @property
    @cleanup_after_exception
    def offset_x(self) -> int:
        """Get the current X offset in pixels."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetX.get()

    @property
    @cleanup_after_exception
    def offset_x_increment(self) -> int:
        """Get the increment for X offset in pixels in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetX.get_increment()

    @property
    @cleanup_after_exception
    def offset_x_range(self) -> tuple[int, int]:
        """Get the range of X offsets supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetX.get_range()

    @offset_x.setter
    @cleanup_after_exception
    def offset_x(self, value: int):
        """Set the X offset in pixels."""
        self.__check_camera_and_vmbsyst()
        offset_x_increment = self.__camera.OffsetX.get_increment()
        if value % offset_x_increment != 0:
            raise ValueError(f"Offset X must be a multiple of {offset_x_increment}.")
        offset_x_range = self.__camera.OffsetX.get_range()
        if value < offset_x_range[0] or value > offset_x_range[1]:
            raise ValueError(f"Offset X must be within the range {offset_x_range}.")
        self.__camera.OffsetX.set(value)

    @property
    @cleanup_after_exception
    def offset_y(self) -> int:
        """Get the current Y offset in pixels."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetY.get()

    @property
    @cleanup_after_exception
    def offset_y_increment(self) -> int:
        """Get the increment for Y offset in pixels in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetY.get_increment()

    @property
    @cleanup_after_exception
    def offset_y_range(self) -> tuple[int, int]:
        """Get the range of Y offsets supported by the camera in the current configuration."""
        self.__check_camera_and_vmbsyst()
        return self.__camera.OffsetY.get_range()

    @offset_y.setter
    @cleanup_after_exception
    def offset_y(self, value: int):
        """Set the Y offset in pixels."""
        self.__check_camera_and_vmbsyst()
        offset_y_increment = self.__camera.OffsetY.get_increment()
        if value % offset_y_increment != 0:
            raise ValueError(f"Offset Y must be a multiple of {offset_y_increment}.")
        offset_y_range = self.__camera.OffsetY.get_range()
        if value < offset_y_range[0] or value > offset_y_range[1]:
            raise ValueError(f"Offset Y must be within the range {offset_y_range}.")
        self.__camera.OffsetY.set(value)

    @property
    @cleanup_after_exception
    def binning(self) -> bool:
        """Get the current binning mode."""
        self.__check_camera_and_vmbsyst()
        return (
            self.__camera.BinningHorizontal.get() > 1
            or self.__camera.BinningVertical.get() > 1
        )

    @binning.setter
    @cleanup_after_exception
    def binning(self, value: bool):
        """Set the binning mode."""
        self.__check_camera_and_vmbsyst()
        if value:
            self.__camera.BinningHorizontal.set(2)
            self.__camera.BinningVertical.set(2)
        else:
            self.__camera.BinningHorizontal.set(1)
            self.__camera.BinningVertical.set(1)

    @cleanup_after_exception
    def start_recording(self, handler):
        """Start streaming frames from the camera. For each frame received, the handler function will be called."""
        self.__check_camera_and_vmbsyst()
        if not callable(handler):
            raise ValueError("Handler must be a callable function.")

        def streaming_handler(cam, stream, frame):
            """Internal handler to process frames from the camera."""
            try:
                handler(frame)
                self.__camera.queue_frame(frame)
            except Exception as e:
                print(f"Error in frame handler: {e}")

        self.__camera.start_streaming(streaming_handler)

    @cleanup_after_exception
    def stop_recording(self):
        """Stop the stream of frames from the camera."""
        self.__check_camera_and_vmbsyst()
        self.__camera.stop_streaming()

    def __check_vmbsyst_instance(self):
        """Check if the VmbSystem instance is initialized."""
        if not self.__vmb_syst:
            raise RuntimeError(
                "VmbSystem instance not initialized (or not with a `with` context). Use `with AlviumCamera() as camera:` to initialize all what is needed."
            )

    def __check_camera(self):
        """Check if the camera is initialized."""
        if not self.__camera:
            raise RuntimeError(
                "Camera not initialized (or not with a `with` context). Use `with AlviumCamera() as camera:` to initialize the camera."
            )

    def __check_camera_and_vmbsyst(self):
        """Check if both the camera and VmbSystem instance are initialized."""

        def inner():
            self.__check_vmbsyst_instance()
            self.__check_camera()

        return inner
