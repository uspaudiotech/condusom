import pyaudio
import numpy as np

class Theremin:
  def __init__(self):
    self.pa = pyaudio.PyAudio()
    self.stream = self.pa.open(format=pyaudio.paFloat32,
                                channels=1,
                                rate=44100,
                                output=True)
  def play(self, freq):
    samples = []
    for i in range(44100):
      samples.append(0.5 * np.sin(2 * np.pi * freq * i / 44100))
    self.stream.write(np.array(samples, dtype=np.float32).tostring())