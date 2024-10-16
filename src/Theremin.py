import pyaudio
import numpy as np

class Theremin:
  def __init__(self):
    self.pa = pyaudio.PyAudio()
    self.stream = self.pa.open(format=pyaudio.paFloat32,
                                channels=1,
                                rate=44100,
                                output=True
                              )

  def play(self, freq, amplitude):
    samples = (amplitude * np.sin(2 * np.pi * np.arange(44100) * freq / 44100)).astype(np.float32)
    self.stream.write(samples.tobytes())

  def update(self, hand_positions):
    freq = 0
    amplitude = 0
    if len(hand_positions) == 1:
      y1 = hand_positions[0][1]  # Y-coordinate of the first hand
      freq = np.interp(y1, [0, 480], [100, 1000])  # Map y1 to frequency range
      amplitude = 0.5  # Default amplitude
    elif len(hand_positions) == 2:
      y1 = hand_positions[0][1]  # Y-coordinate of the first hand
      y2 = hand_positions[1][1]  # Y-coordinate of the second hand
      freq = np.interp(y1, [0, 480], [100, 1000])  # Map y1 to frequency range
      amplitude = np.interp(y2, [0, 480], [0, 1])  # Map y2 to amplitude range

    self.play(freq, amplitude)

  def close(self):
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()