import time
import numpy as np
import pyaudio
import openwakeword
from openwakeword.model import Model

openwakeword.utils.download_models()

model = Model(
    wakeword_models = ["hey_jarvis"]
)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280
MICROPHONE_INDEX = 15

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=MICROPHONE_INDEX,
    frames_per_buffer=CHUNK
)

print("Listening...")
print("Say Hey Jarvis")

last_detection = 0

try:
    while True:
        audio_data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )
        
        frame = np.frombuffer(
            audio_data,
            dtype=np.int16
        )
        
        prediction = model.predict(frame)
        
        for wakeword,score in prediction.items():
            if score > 0.5 and time.time() - last_detection > 2:
                print("Hello world")
                last_detection = time.time()
except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(e)
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()