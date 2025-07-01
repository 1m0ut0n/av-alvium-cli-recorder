# flake8: noqa: E501
import click
from camera import AlviumCamera
from configure import configure_camera, print_infos
from capture import record_video


@click.group()
def cli():
    """Command line tool to configure and take videos with an Alvium camera."""
    pass


@cli.command(short_help="Get infos about current camera configuration")
@click.option(
    "--shutter-speed", "-ss", type=click.FLOAT, default=5000, help="Shutter speed in µs"
)
@click.option(
    "--binning",
    "-b",
    type=click.BOOL,
    default=False,
    help="To activate 2x2 sensor binning (the max resolution will be cut in half)",
)
@click.option(
    "--height", "-h", type=click.INT, default=1248, help="Image height in pixels"
)
@click.option(
    "--width", "-w", type=click.INT, default=1632, help="Image width in pixels"
)
# @click.option("--output", "-o", default="video.mp4", help="Output video file name")
def infos(shutter_speed, binning, height, width):
    """
    Configure the camera with the given options and then display the current config.
    """
    with AlviumCamera() as camera:
        configure_camera(camera, shutter_speed, binning, height, width)
        click.echo()
        print_infos(camera)
        click.echo()


@cli.command(short_help="Record a video with the camera")
@click.option(
    "--shutter-speed", "-ss", type=click.FLOAT, default=5000, help="Shutter speed in µs"
)
@click.option(
    "--binning",
    "-b",
    type=click.BOOL,
    default=False,
    help="To activate 2x2 sensor binning (the max resolution will be cut in half)",
)
@click.option(
    "--height", "-h", type=click.INT, default=1248, help="Image height in pixels"
)
@click.option(
    "--width", "-w", type=click.INT, default=1632, help="Image width in pixels"
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="video.avi",
    help="Output video file name",
)
def record(shutter_speed, binning, height, width, output):
    """
    Configure the camera with the given options and then start the recording of a video.
    """
    with AlviumCamera() as camera:
        configure_camera(camera, shutter_speed, binning, height, width)
        click.echo()
        print_infos(camera)
        click.echo()
        record_video(camera, output)


if __name__ == "__main__":
    cli()
