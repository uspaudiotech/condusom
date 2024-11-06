import threading
from constants import WIDTH, HEIGHT, NUM_LANDMARKS

class SharedResources:
  def __init__(self):
    # Flag to stop the threads
    self.running        = [True]
    # Lock for hand_landmarks and hand_center
    self.lock           = threading.Lock()
    # (x,y) coordinates of each landmark
    self.hand_landmarks = [(0, HEIGHT)] * NUM_LANDMARKS
    # (x,y) coordinates of the center of the hand
    self.hand_center    = [(0, HEIGHT)]