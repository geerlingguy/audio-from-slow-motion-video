# Audio from SloMo Video

Attempts at reproducing sound using video frames of hot dog plasma arcing.

This project stems from a collaboration between Geerling Engineering and Slow Mo Guys:

  - Geerling Engineering: [TODO](TODO)
  - Slow Mo Guys: [TODO](TODO)

The repository includes a Arduino Sketch meant for testing the theory of audio-from-video, using an LED that blinks more brightly in response to the amplitude of an audio waveform.

It also includes a Python script which attempts to turn a video into audio waveforms, by converting frame brightness to sound amplitude.

Some pre- and post-processing steps are required. See the Geerling Engineering video [TODO](TODO) for an overview of the process with some real-world footage of a hot dog, grounded to an AM radio tower, generating bright plasma arcs in response to the amplitude-modulated carrier wave.

## 1 - drive LED brightness based on sound level

TODO: Photo of setup here.

Using an Arduino Uno connected to your computer's USB port, and an audio device capable of headphone-level sound output, along with an audio cable broken out into individual pins (or clipping onto the TRS, where the Sleeve is ground):

  1. Connect the analog audio output positive/signal into Analog Pin `A0`
  2. Connect the analog audio output negative/ground into one of the Power `GND` pins
  3. Connect the LED negative leg to one of the Power `GND` pins
  4. Connect the LED positive leg to a 220-ohm resistor
  5. Connect the 220-ohm resistor to Digital PWM pin `~9`
  6. Plug the Uno into your computer, open `Analog-Voltage-to-LED-Brightness.ino` inside [Arudino IDE](https://www.arduino.cc/en/software/)
  7. Upload the compiled .ino to the Uno, and play some audio.

When you're ready to play the sound file in, you should slow it down so you can get more temporal resolution (unless you have a camera able to record at 11kHz or higher...):

```
sox input.aiff output.aiff speed 0.025
```

Note: `0.025` means it will be 97.5% slower than the original sound file.

## 2 - Capture slow-motion video and convert the brightness levels to audio waveforms

TODO: Image of audio waveforms.

Record the LED using a high speed camera (e.g. iPhone at 240 fps 'Slo-mo', or a nicer slow-motion camera if you have it!). If desired, isolate the LED so it's brightness more directly affects the video brightness levels. Consider using a black felt or construction paper background around the LED to further isolate it, and turn off other lights!

I also put the video file into Final Cut Pro and further processed it to isolate the red LED light. Then I scaled it to fill up most of the frame (with black around it).

> Note: For real-world footage, especially from a high-speed camera, I found the easiest way to isolate bright spots (like plasma) from the rest of the footage was to add a [luma keyer](https://support.apple.com/guide/final-cut-pro/use-the-luma-keyer-effect-ver40b0028e/mac), and filter out almost everything but the brightest spots. YMMV if you try this technique with closeup footage of an incredibly bright object like the sun.

Then take the processed video file, and extract brightness values as a waveform:

```
python3 video-to-audio.py your_video_file.mp4
```

The resulting WAV file will need some cleanup.

## 3 - Cleaning up and adjusting the WAV file

TODO: Before DC offset filter.

There is likely going to be some 'DC bias' or 'offset' that needs cleaning up. I used Sound Studio's [DC Offset](https://www.felttip.com/ss/reference.html) filter to automatically fix the bias, so I'd have a true audio waveform and not something that just pushes out the speaker cone a lot (see above for what it looked like before applying the filter).

If you slowed down the original audio file, you need to speed it back up by the same amount (e.g. 125x):

```
sox input.aiff output.aiff speed 125.0
```
