# Webcam constants
HEIGHT = 720 
# WIDTH = 1280 
WIDTH = HEIGHT * 16 // 9 # 16:9 aspect ratio

# Frequency range for the Synthesizer
MIN_FREQ = 60
MAX_FREQ = 1500 

# Audio settings
SR = MAX_FREQ * 2 + 100
CHUNK = 64
SLEEP = 0.07

# Amplitude settings
DEF_AMP = 0.1 

# Hand detection settings
HAND_DETECTION_CONFIDENCE = 0.8
MAX_HANDS = 1
NUM_LANDMARKS = 21

# Webcam settings
FPS = 24