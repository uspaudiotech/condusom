from hand_detector import HandDetector, fps2ms
from theremin import Theremin
import cv2
import time

def main():
	cTime = 0
	pTime = 0
	cap = cv2.VideoCapture(0)
	refresh_rate = fps2ms(24)
 
	# Reduce frame size for better performance
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

	# Initialize the detector once
	detector = HandDetector()

	while True:
		success, img = cap.read()
		if not success:
			break

		img = cv2.flip(img,1) # mirror the image
		img = detector.findhands(img)
		position = detector.findPosition(img)

		if len(position) != 0:
			print(position)

		# calculating time
		cTime = time.time()
		fps = 1 / (cTime - pTime)
		pTime = cTime

		cv2.putText(
			img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1
		)

		cv2.imshow("img", img)
		if cv2.waitKey(refresh_rate) & 0xFF == ord("d"):
			break


if __name__ == "__main__":
	main()