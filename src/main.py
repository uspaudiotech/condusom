from Condusom import CondusomCenter, CondusomRandom
import sys

def main(strategy):
	if strategy == 'center':
		condusom = CondusomCenter()
	elif strategy == 'random':
		condusom = CondusomRandom()

	condusom.run()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python main.py <strategy>")
		sys.exit(1)
	strategy = sys.argv[1]
	main(strategy)