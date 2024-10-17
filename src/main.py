from Webcam import Webcam
from HandDetector import HandDetectorMP, HandDetectorCV
from Theremin import Theremin

def main():
	webcam = Webcam()

	# hand_detector = HandDetectorMP()
	hand_detector = HandDetectorCV()

	hand_detector.run(webcam,)

if __name__ == "__main__":
	main()