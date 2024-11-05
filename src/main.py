from HandDetector import HandDetectorCVRandomFreq, HandDetectorCVCentralFreq
from Synthesizer import SynthesizerRandomFreq, SynthesizerCentralFreq
from SharedResources import SharedResources
import threading
import sys

def main(strategy):
	shared_resources = SharedResources()

	if strategy == 'central':
		hand_detector = HandDetectorCVCentralFreq(shared_resources)
		synthesizer = SynthesizerCentralFreq(shared_resources)
	elif strategy == 'random':
		hand_detector = HandDetectorCVRandomFreq(shared_resources)
		synthesizer = SynthesizerRandomFreq(shared_resources)

	hand_detector_thread = threading.Thread(target=hand_detector.run)
	synthesizer_thread = threading.Thread(target=synthesizer.run)

	hand_detector_thread.start()
	synthesizer_thread.start()

	hand_detector_thread.join()
	synthesizer_thread.join()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python main.py <strategy>")
		sys.exit(1)
	strategy = sys.argv[1]
	main(strategy)