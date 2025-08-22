# flake8: noqa: E501
from camera import AlviumCamera
from click import secho


def configure_camera(camera: AlviumCamera, shutter_speed, binning, height, width):
    """Configure the camera settings and display the changes that are made if the setting can't be put to the given value."""

    # Set the binning mode
    if camera.binning_available:
        camera.binning = binning
    elif binning == True:
        secho(
            "Binning is not available on this camera. Setting binning to False.",
            fg="bright_black",
        )
        binning = False

    # Check if the shutter speed is within the camera's shutter speed range
    # If not it is automatically set to the minimum value allowed by the camera
    shutter_speed_range = camera.shutter_speed_range
    if shutter_speed < shutter_speed_range[0] or shutter_speed > shutter_speed_range[1]:
        camera.shutter_speed = shutter_speed_range[0]
        secho(
            f"Shutter speed {shutter_speed} µs is out of range. "
            f"Setting to minimum {camera.shutter_speed} µs.",
            fg="bright_black",
        )
    else:
        camera.shutter_speed = shutter_speed

    # Check if the height and width are within the camera's image size range
    # If not, set them to the maximum values allowed by the camera
    height_range = camera.image_height_range
    width_range = camera.image_width_range
    if height < height_range[0] or height > height_range[1]:
        camera.image_height = height_range[1]
        secho(
            f"Height {height} pixels is out of range. "
            f"Setting to maximum {camera.image_height} pixels.",
            fg="bright_black",
        )
    else:
        camera.image_height = height
    if width < width_range[0] or width > width_range[1]:
        camera.image_width = width_range[1]
        secho(
            f"Width {width} pixels is out of range. "
            f"Setting to maximum {camera.image_width} pixels.",
            fg="bright_black",
        )
    else:
        camera.image_width = width

    # Check if the height and width are multiples of the increments required by the camera
    # If not, set them to the nearest multiple of the increment
    height_increment = camera.image_height_increment
    if height % height_increment != 0:
        camera.image_height = (height // height_increment) * height_increment
        secho(
            f"Height {height} pixels is not a multiple of {height_increment}. "
            f"Setting to {height} pixels.",
            fg="bright_black",
        )
    width_increment = camera.image_width_increment
    if width % width_increment != 0:
        camera.image_width = (width // width_increment) * width_increment
        secho(
            f"Width {width} pixels is not a multiple of {width_increment}. "
            f"Setting to {width} pixels.",
            fg="bright_black",
        )

    # Calculate offsets values for centering the image on the sensor
    offset_x = (width_range[1] - camera.image_width) // 2
    offset_y = (height_range[1] - camera.image_height) // 2
    offset_x_increment = camera.offset_x_increment
    offset_y_increment = camera.offset_y_increment
    if offset_x % offset_x_increment != 0:
        offset_x = (offset_x // offset_x_increment) * offset_x_increment
    if offset_y % offset_y_increment != 0:
        offset_y = (offset_y // offset_y_increment) * offset_y_increment
    camera.offset_x = offset_x
    camera.offset_y = offset_y


def print_infos(camera: AlviumCamera):
    """Print the current camera configuration."""
    secho("- Current camera configuration -", fg="blue", bold=True)
    secho(
        f"Pixels : {'Colored (Bayer)' if camera.color_available else 'Gray (Mono)'}",
        fg="blue",
    )
    secho(f"Framerate: {camera.current_fps:.2f} fps", fg="blue")
    secho(f"Shutter speed: {camera.shutter_speed} µs", fg="blue")
    secho(
        f"Binning: {'Enabled (2x2) (Average)' if camera.binning else 'Disabled'}",
        fg="blue",
    )
    secho(f"Image size: {camera.image_width}x{camera.image_height} px", fg="blue")
    secho(f"Offsets: {camera.offset_x}x{camera.offset_y} px", fg="blue")
