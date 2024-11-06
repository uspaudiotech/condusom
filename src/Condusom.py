from SharedResources import SharedResources
from Synth import Synth, SynthCenter, SynthRandom
from HandTracker import HandTracker
from abc import ABC, abstractmethod
import threading

class Condusom(ABC):
  def __init__(self):
    self.shared_resources = SharedResources()
    self.hand_tracker     = HandTracker(self.shared_resources)
    self.synth            = self.create_synth(self.shared_resources)
  
  def run(self):
    print("Starting Condusom.")
    hand_tracker_thread = threading.Thread(target=self.hand_tracker.run)
    synth_thread = threading.Thread(target=self.synth.run)

    hand_tracker_thread.start()
    synth_thread.start()

    hand_tracker_thread.join()
    synth_thread.join()
  

  @abstractmethod
  def create_synth(self) -> Synth:
    pass



class CondusomCenter(Condusom):
  def create_synth(self, shared_resources) -> SynthCenter:
    return SynthCenter(shared_resources)
  


class CondusomRandom(Condusom):
  def create_synth(self, shared_resources) -> SynthRandom:
    return SynthRandom(shared_resources)