from HandDetector import HandDetectorCV
from Synthesizer import Synthesizer
from SharedResources import SharedResources
import threading

def main():
	shared_resources = SharedResources()

	hand_detector = HandDetectorCV(shared_resources.lock,
																shared_resources.running,
																shared_resources.hand_positions)
	synthesizer = Synthesizer(shared_resources.lock,
													 shared_resources.running,
													 shared_resources.hand_positions)

	hand_detector_thread = threading.Thread(target=hand_detector.run)
	synthesizer_thread = threading.Thread(target=synthesizer.run)

	hand_detector_thread.start()
	synthesizer_thread.start()

	hand_detector_thread.join()
	synthesizer_thread.join()

if __name__ == "__main__":
	main()