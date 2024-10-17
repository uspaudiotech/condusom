from constants import FPS, WIDTH, HEIGHT
import cv2

def fps2ms(fps):
  return 1000 // fps

class Webcam:
  def __init__(self) -> None:
    self.cap = cv2.VideoCapture(0)
    self.refresh_rate = fps2ms(FPS)

    # Reduce frame size for better performance
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

