from constants import SR, DEF_AMP, HEIGHT, MIN_FREQ, MAX_FREQ, NUM_LANDMARKS, FPS, SLEEP
import pyaudio
import numpy as np
import time

class Synthesizer():
  def __init__(self, lock, running, hand_positions):
    super().__init__()
    self.lock = lock
    self.running = running 
    self.hand_positions = hand_positions
    self.pa = pyaudio.PyAudio()
    self.freq = 0
    self.amplitude = 0
    self.phase = 0
    self.stream = self.pa.open(format=pyaudio.paFloat32,
                               channels=1,
                               rate=SR,
                               output=True,
                               stream_callback=self.callback
                              )

  # Generates samples of a sine wave
  def callback(self, in_data, frame_count, time_info, status):
    # Create an array of time values for the current frame
    t = (np.arange(frame_count) + self.phase) / SR
    
    # Generate sine wave samples based on the current frequency and amplitude
    samples = (self.amplitude * np.sin(2 * np.pi * self.freq * t)).astype(np.float32)
    
    # Update the phase to ensure continuity of the sine wave in the next callback
    self.phase = (self.phase + frame_count) % SR
    
    # Return the generated samples and indicate that the stream should continue
    return (samples.tobytes(), pyaudio.paContinue)

  def update(self):
    # with self.lock:
    # print(f"{self.hand_positions}")

    # Chooses randomly one of the 21 landmarks to set the frequency
    y1 = self.hand_positions[np.random.randint(0,NUM_LANDMARKS)]

    self.freq = np.interp(y1, [int(-HEIGHT/2),HEIGHT-100], [MAX_FREQ,MIN_FREQ]) # linear
    self.amplitude = DEF_AMP

  def run(self):
    print("Starting Synthesizer.")
    self.stream.start_stream()
    while self.running[0]:
      # print("Synthesizer running.")
      self.update()
      # time.sleep(1/FPS)
      time.sleep(SLEEP)
    self.stop()

  def stop(self):
    print("Stopping Synthesizer.")
    self.stream.stop_stream()
    self.stream.close()
    self.pa.terminate()