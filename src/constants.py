# Webcam settings 
HEIGHT = 720
WIDTH  = HEIGHT * 16 // 9 # 16:9 aspect ratio
FPS    = 30

# Hand detection settings
HAND_DETECTION_CONFIDENCE = 0.8
MAX_HANDS                 = 1
NUM_LANDMARKS             = 21

# Synth settings
MIN_FREQ = 100
MAX_FREQ = 2**2 * MIN_FREQ

# Audio settings
SR      = 48000
SLEEP   = 0.1
DEF_AMP = 0.4
DEF_BLOCK_SIZE = 64