import pyaudio

audio = pyaudio.PyAudio()

print("Audio devices:\n")

for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)

    print(
        f"{i}: {info['name']} | "
        f"inputs={info['maxInputChannels']} | "
        f"outputs={info['maxOutputChannels']} | "
        f"rate={info['defaultSampleRate']}"
    )

audio.terminate()