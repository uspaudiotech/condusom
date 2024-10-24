from constants import MAX_HANDS, HEIGHT, NUM_LANDMARKS
from Webcam import Webcam
import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp

class HandDetectorCV:
	def __init__(self, shared_resources):
		self.lock = shared_resources.lock
		self.running = shared_resources.running 
		self.hand_positions = shared_resources.hand_positions
		self.detector = HandDetector(staticMode=False,
															 maxHands=MAX_HANDS,
															 modelComplexity=1,
															 detectionCon=0.8
															 )
		self.webcam = Webcam()

	def run(self):
		print("Starting HandDetectorCV.")
		while self.running[0]:
			success, img = self.webcam.cap.read()
			img = cv2.flip(img,1) # mirror the image
			if not success:
				break
			hands, img = self.detector.findHands(img, draw=True, flipType=False)

			# with self.lock:
			if hands:
				for hand in hands:
					self.hand_positions[:] = [lm[1] for lm in hand['lmList']]
			else:
				self.hand_positions[:] = [-HEIGHT] * NUM_LANDMARKS 
			# print(f"{self.hand_positions}")

			cv2.imshow("img", img)

			# Press 'd' to exit the application
			if cv2.waitKey(self.webcam.refresh_rate) & 0xFF == ord("d"):
				self.running[0] = False
				print("Stopping HandDetectorCV.")
				self.webcam.stop()

class HandDetectorMP:
	def __init__(
		self,
		mode=False,
		maxHands=1,
		modelComplexity=1,
		detectionConf=0.5,
		trackingConf=0.5,
	):
		self.mode = mode
		self.maxHands = maxHands
		self.modelComplexity = modelComplexity
		self.detectionConf = detectionConf
		self.trackingConf = trackingConf

		# Detecting landmarks and connections
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(
			self.mode, self.maxHands, modelComplexity, detectionConf, trackingConf
		)
		self.mpdraw = mp.solutions.drawing_utils

	def find_hands(self, img, draw=True):
		"""
		Detects hands in the given image and optionally draws landmarks on them.

		Args:
			img (numpy.ndarray): The input image in which hands are to be detected.
			draw (bool, optional): If True, draws landmarks on the detected hands. Defaults to True.

		Returns:
			numpy.ndarray: The image with landmarks drawn if `draw` is True, otherwise the original image.
		"""
		self.RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.result = self.hands.process(self.RGBimg)

		if self.result.multi_hand_landmarks:
			for handlms in self.result.multi_hand_landmarks:
				if draw:
					self.mpdraw.draw_landmarks(
						img, handlms, self.mpHands.HAND_CONNECTIONS
					)

		return img

	def find_position(self, img, handNo=0, draw=True):
		"""
		Finds the position of hand landmarks in the given image.

		Args:
			img (numpy.ndarray): The input image in which hand landmarks are to be detected.
			handNo (int, optional): The index of the hand to be processed. Defaults to 0.
			draw (bool, optional): If True, draws circles on the detected landmarks. Defaults to True.

		Returns:
			list: A list of lists, where each sublist contains the id and (x, y) coordinates of a landmark.
		"""
		lmlist = []

		if self.result.multi_hand_landmarks:
			myHand = self.result.multi_hand_landmarks[handNo]

			for id, lm in enumerate(myHand.landmark):
				h, w = img.shape[:2]
				cx, cy = int(lm.x * w), int(lm.y * h)
				lmlist.append([id, cx, cy])
				if draw:
					dot_size = 5
					dot_color = (255, 255, 255)
					cv2.circle(img, (cx, cy), dot_size, dot_color, cv2.FILLED)

				return lmlist

	def run(self, webcam):
		while True:
			success, img = webcam.cap.read()
			if not success:
				break

			img = cv2.flip(img,1) # mirror the image

			img = self.find_hands(img)

			# position = hand_detector.find_position(img)
			# if len(position) != 0:
			# 	print(position)

			# Display the frame rate
			# cv2.putText(
			# 	img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1
			# )

			cv2.imshow("img", img)

			# Press 'd' to exit the application
			if cv2.waitKey(webcam.refresh_rate) & 0xFF == ord("d"):
				break	
