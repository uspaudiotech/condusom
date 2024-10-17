from constants import FPS
import cv2

def fps2ms(fps):
  return 1000 // fps

class Webcam:
  def __init__(self) -> None:
    self.cap = cv2.VideoCapture(0)
    self.refresh_rate = fps2ms(FPS)

    # Reduce frame size for better performance
    width = 1280; height = 640
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

