from Webcam import Webcam
from HandDetector import HandDetectorMP, HandDetectorCV
from Theremin import Theremin
# import threading
# import queue

def main():
	webcam = Webcam()

	# hand_detector = HandDetectorMP()
	hand_detector = HandDetectorCV()

	theremin = Theremin()

	hand_detector.run(webcam, theremin)

if __name__ == "__main__":
	main()