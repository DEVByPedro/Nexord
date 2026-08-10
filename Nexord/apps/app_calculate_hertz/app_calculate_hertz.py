import sounddevice as sd
import numpy as np

RATE = 44100
CHUNK = 4096

def audio_callback(indata, frames, time, status):
    audio = indata[:, 0]

    # FFT
    fft = np.fft.rfft(audio)
    frequencies = np.fft.rfftfreq(len(audio), 1 / RATE)

    magnitude = np.abs(fft)

    # Ignore frequencies below 50 Hz
    magnitude[:int(50 * CHUNK / RATE)] = 0

    # Find strongest frequency
    peak = np.argmax(magnitude)
    frequency = frequencies[peak]

    print(f"{frequency:.2f} Hz")


# with sd.InputStream(
#     samplerate=RATE,
#     channels=1,
#     blocksize=CHUNK,
#     callback=audio_callback
# ):
#     print("Listening...")
#     input()