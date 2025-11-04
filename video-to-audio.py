# Video Frame Brightness to Audio Waveform
#
# By Jeff Geerling, with code from Google AI, in October 2025.
#
# The bugs are probably my own doing. The egregious ones, AI.
#
# ```
# # Create and activate venv with uv
# uv venv
# source .venv/bin/activate
#
# # Install dependencies
# uv pip install opencv-python numpy scipy tqdm
#
# # Run the script
# (if needed, activate the virtual environment:) source .venv/bin/activate
# python3 video-to-audio.py your_video.mp4 [--output your_audio.wav]
# ```
#
# Note: cv2 import takes a while, that is normal.

import cv2
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import resample
import argparse
import sys
from tqdm import tqdm

def gamma_correction(image, gamma=2.2):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def get_video_brightness(video_path):
    """
    Analyzes a video file to extract the average brightness level for each frame,
    with a live progress bar.

    Args:
        video_path (str): The path to the video file.

    Returns:
        tuple: A tuple containing a list of floats for average brightness and the video's frame rate.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return [], 0

    brightness_levels = []
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with tqdm(total=total_frames, desc="Processing video frames") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale frame for easier luminance processing.
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply gamma correction (this didn't help as much as I thought).
            # gamma_corrected_frame = gamma_correction(gray_frame, gamma=3.0)
            # avg_brightness = np.mean(gamma_corrected_frame)

            avg_brightness = np.mean(gray_frame)
            brightness_levels.append(avg_brightness)

            pbar.update(1)

    cap.release()
    return brightness_levels, frame_rate

def create_and_save_wav(brightness_levels, frame_rate, output_path='brightness_audio.wav'):
    """
    Converts a list of brightness levels into a WAV audio file,
    removing the DC offset to make it audible.

    Args:
        brightness_levels (list): A list of average brightness values for each frame.
        frame_rate (float): The frame rate of the original video.
        output_path (str): The path to save the output WAV file.
    """
    if not brightness_levels:
        print("No brightness data to process.")
        return

    audio_sample_rate = 44100
    num_frames = len(brightness_levels)
    duration_sec = num_frames / frame_rate
    num_audio_samples = int(duration_sec * audio_sample_rate)

    brightness_np = np.array(brightness_levels)

    # === Key change for DC offset removal ===
    # Subtract the mean to center the signal around zero
    # This removes the "DC bias" and makes the audio audible
    centered_data = brightness_np - np.mean(brightness_np)

    upsampled_data = resample(centered_data, num_audio_samples)

    # Scale and normalize the centered data to the audio range
    # abs(upsampled_data) is used to find the new maximum positive or negative amplitude
    max_amplitude = np.max(np.abs(upsampled_data))
    if max_amplitude > 0:
        scaled_data = (upsampled_data / max_amplitude) * 32767
    else:
        scaled_data = upsampled_data # Avoid division by zero if max_amplitude is 0

    audio_data = scaled_data.astype(np.int16)

    write(output_path, audio_sample_rate, audio_data)
    print(f"\nAudio waveform successfully saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts video frame brightness levels and converts them into a WAV audio file.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'video_file',
        type=str,
        help="Path to the video file to be processed."
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='brightness_audio.wav',
        help=(
            "Optional: Path and filename for the output WAV file.\n"
            "If not specified, saves to 'brightness_audio.wav' in the current directory."
        )
    )

    args = parser.parse_args()

    video_file = args.video_file
    output_file = args.output

    try:
        brightness, fps = get_video_brightness(video_file)
        if brightness:
            create_and_save_wav(brightness, fps, output_file)
        else:
            print("Processing stopped. Could not get brightness data.")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
