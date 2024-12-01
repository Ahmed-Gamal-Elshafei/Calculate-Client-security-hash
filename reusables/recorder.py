import threading
import time
import mss
import os  # For folder management
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio
from datetime import datetime, timezone

# Global variables for recording state and resolution reduction factor
recording = False
record_thread = None
RESOLUTION_REDUCTION_FACTOR = 1


def start_recording(
    output_file_prefix="output",
    watermark_text="Watermark",
    font_size=20,
    text_color=(255, 255, 255, 128),
    stroke_color=(0, 0, 0, 255),
    fps=15
):
    """
    Start screen recording with a watermark overlay.

    Parameters:
        output_file_prefix (str): Prefix for the recorded video file name.
        watermark_text (str): Text to display as a watermark.
        font_size (int): Font size of the watermark.
        text_color (tuple): RGBA color for watermark text.
        stroke_color (tuple): RGBA stroke color for the watermark text.
        fps (int): Frames per second for the recording.
    """
    global recording, record_thread
    if not recording:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file_prefix)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Append current GMT date and time to the file name
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{output_file_prefix}_{current_time}.mp4"

        recording = True
        record_thread = threading.Thread(
            target=_record_screen,
            args=(output_file, watermark_text, font_size, text_color, stroke_color, fps)
        )
        record_thread.start()


def stop_recording():
    """
    Stop the ongoing screen recording.
    """
    global recording, record_thread
    if recording:
        recording = False
        record_thread.join()


def _record_screen(output_file, watermark_text, font_size, text_color, stroke_color, fps):
    """
    Internal function to handle screen recording logic.

    Parameters:
        output_file (str): Path to save the recorded video.
        watermark_text (str): Text to display as a watermark.
        font_size (int): Font size of the watermark.
        text_color (tuple): RGBA color for watermark text.
        stroke_color (tuple): RGBA stroke color for the watermark text.
        fps (int): Frames per second for the recording.
    """
    global RESOLUTION_REDUCTION_FACTOR

    # Capture the screen using mss
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Adjust index for multiple monitors
        width, height = monitor["width"], monitor["height"]

        # Calculate adjusted resolution (must be divisible by 16 for video encoding)
        width_adjusted = int((width / RESOLUTION_REDUCTION_FACTOR + 15) // 16 * 16)
        height_adjusted = int((height / RESOLUTION_REDUCTION_FACTOR + 15) // 16 * 16)

        # Initialize the video writer with proper settings
        writer = imageio.get_writer(
            output_file, fps=fps, codec="libx264", format="FFMPEG", quality=5, pixelformat='yuv420p'
        )

        # Load font for the watermark; fallback to default if unavailable
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Calculate position for watermark (centered horizontally, near the bottom)
        text_position = (width_adjusted // 2 - font_size * len(watermark_text) // 4, height_adjusted - 50)

        while recording:
            # Capture the current screen
            img = sct.grab(monitor)
            frame = Image.frombytes("RGB", img.size, img.rgb)

            # Resize the frame based on the resolution reduction factor
            frame = frame.resize((width_adjusted, height_adjusted), Image.BICUBIC)

            # Create an overlay for the watermark
            overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            draw.text(
                text_position,
                watermark_text,
                font=font,
                fill=text_color,
                stroke_width=2,
                stroke_fill=stroke_color,
            )

            # Combine the overlay with the frame
            frame = Image.alpha_composite(frame.convert("RGBA"), overlay)

            # Convert frame to numpy array for video writer
            frame_np = np.array(frame.convert("RGB"))

            # Write the frame to the video
            writer.append_data(frame_np)

            # Sleep to maintain the desired frame rate
            time.sleep(1 / fps)

        # Finalize the video writer
        writer.close()


if __name__ == "__main__":
    # Start recording with specified parameters
    start_recording(
        output_file_prefix=r"Records/output",
        watermark_text="Infinity Chat",
        font_size=30,
        text_color=(255, 255, 255, 128),
        stroke_color=(0, 0, 0, 255),
        fps=30
    )
    time.sleep(1 * 60)
    stop_recording()
