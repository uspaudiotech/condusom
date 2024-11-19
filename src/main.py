from Condusom import Condusom
import sys

def main(map_hand_strat, map_freq_strat):
	print(f"Hand mapping strategy: {map_hand_strat}")
	print(f"Frequency mapping strategy: {map_freq_strat}")

	condusom = Condusom(map_hand_strat, map_freq_strat)

	condusom.run()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python main.py <map_hand_strat> <map_freq_strat>")
		sys.exit(1)
	map_hand_strat = sys.argv[1]
	map_freq_strat = sys.argv[2]

	main(map_hand_strat, map_freq_strat)