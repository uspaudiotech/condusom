from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ, NUM_LANDMARKS, FPS, SLEEP
import pyaudio
import numpy as np
from time import sleep
from abc import ABC, abstractmethod

class Synth(ABC):
  def __init__(self, shared_resources):
    # Shared resources setup
    self.lock           = shared_resources.lock
    self.running        = shared_resources.running 
    self.hand_landmarks = shared_resources.hand_landmarks
    self.hand_center    = shared_resources.hand_center

    # Synth parameters 
    self.freq           = 0
    self.phase          = 0
    self.amplitude      = DEF_AMP

    # PyAudio setup
    self.pa             = pyaudio.PyAudio()
    self.stream         = self.pa.open(format=pyaudio.paFloat32,
                                       channels=1,
                                       rate=SR,
                                       output=True,
                                       stream_callback=self.callback
                                       )

  def callback(self, in_data, frame_count, time_info, status):
    # with self.lock:
      # Create an array of time values for the current frame
      t = np.arange(frame_count) / SR
      
      # Generate sine wave samples based on the current frequency and amplitude
      samples = (self.amplitude * np.sin(self.phase + (2 * np.pi * self.freq * t))).astype(np.float32)
      
      # Update the phase to ensure continuity of the sine wave in the next callback
      self.phase += 2 * np.pi * self.freq * (frame_count / SR)
      
      # Return the generated samples and indicate that the stream should continue
      return (samples.tobytes(), pyaudio.paContinue)
  
  @abstractmethod
  def get_hand_coords(self):
    pass

  def update(self):
    with self.lock:
      _, y = self.get_hand_coords()

      # Map the y-coordinate of the hand to a frequency value
      self.freq = np.interp(y, [0, int(0.8*HEIGHT)], [MAX_FREQ, MIN_FREQ])
   
  @abstractmethod
  def run(self):
    pass

  def stop(self):
    print("Stopping Synth.")
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()



class SynthCenter(Synth):
  def get_hand_coords(self):
    # with self.lock:
      return self.hand_center[0]

  def run(self):
    print("Starting Synth.")
    self.stream.start_stream()
    while self.running[0]:
      self.update()
      sleep(1/FPS)
    self.stop()



class SynthRandom(Synth):
  def get_hand_coords(self):
    return self.hand_landmarks[np.random.randint(0,NUM_LANDMARKS)]

  def run(self):
    print("Starting Synth.")
    self.stream.start_stream()
    while self.running[0]:
      self.update()
      sleep(SLEEP)
    self.stop()