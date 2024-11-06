from constants import FPS, WIDTH, HEIGHT
import cv2

class Webcam:
  def __init__(self):
    self.cap = cv2.VideoCapture(0)

    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    self.refresh_rate = self.fps2ms(FPS)

  
  def fps2ms(self, fps):
    return 1000 // fps

  def stop(self):
    self.cap.release()
    cv2.destroyAllWindows()
