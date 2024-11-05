from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ, NUM_LANDMARKS, FPS, SLEEP
import pyaudio
import numpy as np
import time
from abc import ABC, abstractmethod

class Synthesizer(ABC):
  def __init__(self, shared_resources):
    self.lock = shared_resources.lock
    self.running = shared_resources.running 
    self.hand_positions = shared_resources.hand_positions
    self.pa = pyaudio.PyAudio()
    self.freq = 0
    self.amplitude = DEF_AMP
    self.phase = 0
    self.stream = self.pa.open(format=pyaudio.paFloat32,
                               channels=1,
                               rate=SR,
                               output=True,
                               stream_callback=self.callback
                              )

  def callback(self, in_data, frame_count, time_info, status):
    # Create an array of time values for the current frame
    t = np.arange(frame_count) / SR
    
    # Generate sine wave samples based on the current frequency and amplitude
    samples = (self.amplitude * np.sin(self.phase + (2 * np.pi * self.freq * t))).astype(np.float32)
    
    # Update the phase to ensure continuity of the sine wave in the next callback
    # self.phase = (self.phase + frame_count) % SR
    self.phase += 2 * np.pi * self.freq * (frame_count / SR)
    
    # Return the generated samples and indicate that the stream should continue
    return (samples.tobytes(), pyaudio.paContinue)
  
  @abstractmethod
  def get_hand_coords(self):
    pass

  def update(self):
    # with self.lock:
    # print(f"{self.hand_positions}")

    _, y = self.get_hand_coords()

    # Map the y-coordinate of the hand to a frequency value
    self.freq = np.interp(y, [int(-HEIGHT/2),HEIGHT-100], [MAX_FREQ,MIN_FREQ])
   
  @abstractmethod
  def run(self):
    pass

  def stop(self):
    print("Stopping Synthesizer.")
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()



class SynthesizerCentralFreq(Synthesizer):
  def get_hand_coords(self):
    return self.hand_positions[0]

  def run(self):
    print("Starting Synthesizer.")
    self.stream.start_stream()
    while self.running[0]:
      # print("Synthesizer running.")
      self.update()
    self.stop()



class SynthesizerRandomFreq(Synthesizer):
  def get_hand_coords(self):
    return self.hand_positions[np.random.randint(0,NUM_LANDMARKS)]

  def run(self):
    print("Starting Synthesizer.")
    self.stream.start_stream()
    while self.running[0]:
      # print("Synthesizer running.")
      self.update()
      time.sleep(SLEEP)
    self.stop()