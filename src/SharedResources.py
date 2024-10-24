import threading
from constants import HEIGHT, NUM_LANDMARKS

class SharedResources:
  def __init__(self):
    self.running = [True]
    self.lock = threading.Lock() # Lock for the hand_positions list shared resource
    self.hand_positions = [-HEIGHT] * NUM_LANDMARKS