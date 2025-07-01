# flake8: noqa: E501
from vmbpy import Frame
from click import echo, secho, getchar  # , launch
import time
import cv2
import threading
import queue
from camera import AlviumCamera


def record_video(camera: AlviumCamera, output: str):
    """Record a video with the camera."""

    # Countdown before recording starts
    for i in range(3, 0, -1):
        secho(f"\r ● {i}s ...", fg="bright_black", nl=False)
        time.sleep(1)

    # Indicate the start of the recording
    secho(
        "\r ● RECORDING",
        fg="red",
        bold=True,
        blink=True,
    )
    echo()
    secho(
        f"Press any key to stop recording. The video will be saved to '{output}'.",
        fg="yellow",
    )

    # Initialize the video writer
    count = 0  # Counter for the number of frames recorded
    codec = (
        "XVID" if output.endswith(".avi") else "mp4v"
    )  # Choose codec based on file extension
    out = cv2.VideoWriter(
        output,
        cv2.VideoWriter_fourcc(*codec),
        camera.current_fps,
        (camera.image_width, camera.image_height),
    )  # Initialize the video writer with the specified codec and resolution

    # Queue to save frames received from the camera until they are written to the video file
    frame_queue = queue.Queue()

    def record_frame(frame: Frame):
        """Callback function to handle each frame received from the camera."""
        frame_queue.put_nowait(
            frame
        )  # It just add the frame in the queue for it to be written later

    def write_frames():
        """Thread function to write frames to the video file."""
        nonlocal out, count
        video_not_ended = True

        while video_not_ended:  # Loop through the queue until the recording is stopped
            try:
                frame = frame_queue.get()
                if frame is None:  # Check for the end of the recording
                    video_not_ended = False
                else:
                    img = cv2.cvtColor(
                        frame.as_numpy_ndarray(), cv2.COLOR_GRAY2RGB
                    )  # Convert the frame to RGB format for OpenCV
                    out.write(img)  # Write the frame to the video file
                    count += 1
            except Exception as e:
                secho(f"Error writing frame: {e}", fg="red")

    # Start the video writer thread to write frames to the video file
    video_writer_thread = threading.Thread(target=write_frames)
    video_writer_thread.start()

    # Start the camera and register the callback function to handle frames
    camera.start_recording(record_frame)

    # Wait for any key to stop recording
    getchar()

    # Stop the recording when a key as been pressed
    camera.stop_recording()
    frame_queue.put(None)  # Signal the thread that this was the last frame to write

    # Prompt the user that the recording has stopped, but we need to wait faor the video writer thread to finish
    secho("\033[A\33[2K\033[A\33[2K\033[A\33[2K ● RECORDED", fg="bright_black")
    echo()
    secho(
        f"Saving video to '{output}'...",
        fg="yellow",
    )

    # Wait for the video writer thread to finish writing frames
    video_writer_thread.join()
    out.release()  # Close the video file

    # Indicate that the video has been saved successfully and show som infos
    secho(
        "\033[A\33[2KVideo saved successfully !",
        fg="yellow",
        bold=True,
    )
    echo()
    secho(
        "- Video details -",
        fg="green",
        bold=True,
    )
    secho(f"Output file path: {output}", fg="green")
    secho(f"Video codec: {codec}", fg="green")
    secho(
        f"Video resolution: {camera.image_width}x{camera.image_height} px",
        fg="green",
    )
    secho(f"Video framerate: {camera.current_fps:.2f} fps", fg="green")
    secho(f"Video duration: {count / camera.current_fps:.2f} s", fg="green")
    secho(f"Total frames recorded: {count}", fg="green")
    echo()
    # if confirm("Do you want to open the video file?", default=False):
    #     launch(output)
    #     secho("Video file opened !", fg="green")
    # echo()
