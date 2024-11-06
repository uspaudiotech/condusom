from constants import HEIGHT, NUM_LANDMARKS
from Synth import Synth, SynthCenter, SynthRandom
from HandTracker import HandTracker, HandTrackerCenter, HandTrackerRandom
from abc import ABC, abstractmethod
import threading

class Condusom(ABC):
  def __init__(self):
    self.synth = None
    self.hand_detector = None
    self.running = [True]
    self.lock = threading.Lock() # Lock for the hand_positions list
    self.hand_positions = [(0,HEIGHT)] * NUM_LANDMARKS # (x,y) coordinates of each landmark
    self.center = [(0,HEIGHT)]
  
  def run(self):
    hand_detector_thread = threading.Thread(target=self.hand_detector.run)
    synth_thread = threading.Thread(target=self.synth.run)

    hand_detector_thread.start()
    synth_thread.start()

    hand_detector_thread.join()
    synth_thread.join()
  

  @abstractmethod
  def create_synth(self) -> Synth:
    pass

  @abstractmethod
  def create_hand_tracker(self) -> HandTracker:
    pass

class CondusomCenter(Condusom):
  def create_synth(self) -> SynthCenter:
    self.synth = SynthCenter()

  def create_hand_detector(self) -> HandTrackerCenter:
    self.hand_tracker = HandTrackerCenter()
  
class CondusomRandom(Condusom):
  def create_synth(self) -> SynthRandom:
    self.synth = SynthRandom()

  def create_hand_detector(self) -> HandTrackerRandom:
    self.hand_tracker = HandTrackerRandom()