from SharedResources import SharedResources
from Condusom import CondusomCenter, CondusomRandom
import threading
import sys

def main(strategy):
	shared_resources = SharedResources()

	if strategy == 'center':
		# hand_detector = HandTrackerCenter(shared_resources)
		# synth = SynthCenter(shared_resources)
		condusom = CondusomCenter()
	elif strategy == 'random':
		# hand_detector = HandTrackerRandom(shared_resources)
		# synth = SynthRandom(shared_resources)
		condusom = CondusomRandom()

	# hand_detector_thread = threading.Thread(target=hand_detector.run)
	# synth_thread = threading.Thread(target=synth.run)

	# hand_detector_thread.start()
	# synth_thread.start()

	# hand_detector_thread.join()
	# synth_thread.join()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python main.py <strategy>")
		sys.exit(1)
	strategy = sys.argv[1]
	main(strategy)