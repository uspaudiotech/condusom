from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ, NUM_LANDMARKS
import pyaudio
import numpy as np


class Synthesizer:
  def __init__(self):
    self.pa = pyaudio.PyAudio()
    self.freq = 0
    self.amplitude = 0
    self.phase = 0
    self.stream = self.pa.open(format=pyaudio.paFloat32,
                               channels=1,
                               rate=SR,
                               output=True,
                               stream_callback=self.callback
                              )

  # Generates samples of a sine wave
  def callback(self, in_data, frame_count, time_info, status):
    t = (np.arange(frame_count) + self.phase) / SR
    samples = (self.amplitude * np.sin(2 * np.pi * self.freq * t)).astype(np.float32)
    self.phase = (self.phase + frame_count) % SR
    return (samples.tobytes(), pyaudio.paContinue)

  def update(self, hand_positions):
    print(f"{hand_positions}")
    # Chooses randomly one of the 21 landmarks to set the frequency
    y1 = hand_positions[np.random.randint(0,NUM_LANDMARKS)]

    # Map y1 to frequency range
    self.freq = np.interp(y1, [int(-HEIGHT/2),HEIGHT-100], [MAX_FREQ,MIN_FREQ])  # linear
    self.amplitude = DEF_AMP
    # print(f"Updated frequency: {self.freq}")

  def close(self):
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()