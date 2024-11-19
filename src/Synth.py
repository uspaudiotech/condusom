from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ, NUM_LANDMARKS, FPS, SLEEP
import pyaudio
import numpy as np
from time import sleep
from abc import ABC, abstractmethod

class MapFreq(ABC):
  @abstractmethod
  def map_frequency(self, f):
    pass

class MapFreqLinear(MapFreq):
  def map_frequency(self, f):
    if f is not None: 
      return np.interp(f, [0, int(0.8*HEIGHT)], [MAX_FREQ, MIN_FREQ])

class MapFreqExponential(MapFreq):
  def map_frequency(self, f):
    return MIN_FREQ * (MAX_FREQ / MIN_FREQ) ** (f / HEIGHT)

class MapFreqLogarithmic(MapFreq):
  def map_frequency(self, f):
    return MIN_FREQ + (MAX_FREQ - MIN_FREQ) * np.log1p(f) / np.log1p(HEIGHT)

class MapFreqFactory:
  def create_map_freq(strategy: str) -> MapFreq:
    if strategy == 'linear':
      return MapFreqLinear()
    elif strategy == 'exponential':
      return MapFreqExponential()
    elif strategy == 'logarithmic':
      return MapFreqLogarithmic()
    else:
      raise ValueError(f"Unknown frequency mapping strategy: {strategy}")
    


class MapHand(ABC):
  @abstractmethod
  def get_hand_coords(self, hand_landmarks, hand_center):
    pass

class MapHandCenter(MapHand):
  def get_hand_coords(self, hand_landmarks, hand_center):
    return hand_center[0]

class MapHandRandom(MapHand):
  def get_hand_coords(self, hand_landmarks, hand_center):
    coords = hand_landmarks[np.random.randint(0, NUM_LANDMARKS)]
    if coords is not None:
      return coords
    return (0,0)

class HandCoordsFactory:
  def create_map_hand(strategy: str) -> MapHand:
    if strategy == 'center':
      return MapHandCenter()
    elif strategy == 'random':
      return MapHandRandom()
    else:
      raise ValueError(f"Unknown hand mapping strategy: {strategy}")



class Synth(ABC):
  def __init__(self, map_hand_strat: str, map_freq_strat: str, shared_resources):
    # Shared resources setup
    self.lock           = shared_resources.lock
    self.running        = shared_resources.running 
    self.hand_landmarks = shared_resources.hand_landmarks
    self.hand_center    = shared_resources.hand_center

    # Synth parameters 
    self.freq           = 0
    self.phase          = 0
    self.amplitude      = DEF_AMP
    self.map_freq       = MapFreqFactory.create_map_freq(map_freq_strat)
    self.map_hand       = HandCoordsFactory.create_map_hand(map_hand_strat)

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
  
  def update(self):
    with self.lock:
      x, y = self.map_hand.get_hand_coords(self.hand_landmarks, self.hand_center)
      self.freq = self.map_freq.map_frequency(y)

  def stop(self):
    print("Stopping Synth.")
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()
  
  def run(self):
    print("Starting Synth.")
    self.stream.start_stream()
    while self.running[0]:
      self.update()
      sleep(SLEEP)
    self.stop()