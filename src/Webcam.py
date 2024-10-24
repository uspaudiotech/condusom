from constants import FPS, WIDTH, HEIGHT
import cv2

def fps2ms(fps):
  return 1000 // fps

class Webcam:
  def __init__(self):
    self.cap = cv2.VideoCapture(0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    self.refresh_rate = fps2ms(FPS)

  # def run(self):
  #   while self.shared_state.running:
  #     success, img = self.cap.read()
  #     if not success:
  #       break
  #     cv2.imshow("Webcam", img)

  #     # HandDetector behaviour should be implemented here

  #     if cv2.waitKey(self.refresh_rate) & 0xFF == ord("d"):
  #       self.shared_state.running = False
  
  def stop(self):
    self.cap.release()
    cv2.destroyAllWindows()
