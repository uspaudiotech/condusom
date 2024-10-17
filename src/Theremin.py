from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ
import pyaudio
import numpy as np


class Theremin:
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
    # if len(hand_positions) == 1:
    y1 = hand_positions[0][1]  # Y-coordinate of the first hand
    # y1 = np.mean([pos[1] for pos in hand_positions[:5]])  # Mean of the Y-coordinates of the first 5 hands
    self.freq = np.interp(y1, [0,HEIGHT], [MAX_FREQ,MIN_FREQ])  # Map y1 to frequency range
    self.amplitude = DEF_AMP
    # print(f"Updated frequency: {self.freq}")

    # elif len(hand_positions) == 2:
    #   y1 = hand_positions[0][1]  # Y-coordinate of the first hand
    #   y2 = hand_positions[1][1]  # Y-coordinate of the second hand
    #   freq = np.interp(y1, [0, 480], [100, 1000])  # Map y1 to frequency range
    #   amplitude = np.interp(y2, [0, 480], [0, 1])  # Map y2 to amplitude range

  def close(self):
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()