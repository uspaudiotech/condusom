from SharedResources import SharedResources
from Synth import Synth
from HandTracker import HandTracker
from abc import ABC, abstractmethod
import threading

class Condusom():
  def __init__(self, map_hand_strat, map_freq_strat):
    self.shared_resources = SharedResources()
    self.hand_tracker     = HandTracker(self.shared_resources)
    self.synth            = Synth(map_hand_strat, map_freq_strat, self.shared_resources)
  
  def run(self):
    print("Starting Condusom.")
    hand_tracker_thread = threading.Thread(target=self.hand_tracker.run)
    synth_thread = threading.Thread(target=self.synth.run)

    hand_tracker_thread.start()
    synth_thread.start()

    hand_tracker_thread.join()
    synth_thread.join()