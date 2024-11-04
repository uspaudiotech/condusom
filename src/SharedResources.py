import threading
from constants import WIDTH, HEIGHT, NUM_LANDMARKS

class SharedResources:
  def __init__(self):
    self.running = [True]
    self.lock = threading.Lock() # Lock for the hand_positions list shared resource
    self.hand_positions = [(0,10*HEIGHT)] * NUM_LANDMARKS # (x,y) coordinates of each landmark
    # self.hand_positions = [(0,10*HEIGHT)]