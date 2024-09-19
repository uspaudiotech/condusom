import cv2
import mediapipe as mp
import time

class handdetector:
	def __init__(
		self,
		mode=False,
		maxHands=2,
		modelComplexity=1,
		detectionConf=0.5,
		trackingConf=0.5,
	):
		self.mode = mode
		self.maxHands = maxHands
		self.modelComplexity = modelComplexity
		self.detectionConf = detectionConf
		self.trackingConf = trackingConf

		# detecting landmarks and connections
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(
			self.mode, self.maxHands, modelComplexity, detectionConf, trackingConf
		)
		self.mpdraw = mp.solutions.drawing_utils

	def findhands(self, img, draw=True):
		self.RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.result = self.hands.process(self.RGBimg)

		if self.result.multi_hand_landmarks:
			for handlms in self.result.multi_hand_landmarks:
				if draw:
					self.mpdraw.draw_landmarks(
						img, handlms, self.mpHands.HAND_CONNECTIONS
					)

		return img

	def findPosition(self, img, handNo=0, draw=True):
		lmlist = []

		if self.result.multi_hand_landmarks:
			myHand = self.result.multi_hand_landmarks[handNo]

			for id, lm in enumerate(myHand.landmark):
				h, w, c = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				lmlist.append([id, cx, cy])
				if draw:
					dot_size = 5
					dot_color = (255, 255, 255)
					cv2.circle(img, (cx, cy), dot_size, dot_color, cv2.FILLED)

		return lmlist
	

def fps2ms(fps):
	return 1000 // fps

def main():
	cTime = 0
	pTime = 0
	cap = cv2.VideoCapture(0)
	refresh_rate = fps2ms(24)
 
	# Reduce frame size for better performance
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

	# Initialize the detector once
	detector = handdetector()

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
