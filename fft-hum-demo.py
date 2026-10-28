import wave
from pathlib import Path

import numpy as np


def main():
    input_path = Path("/Users/sfffpanda/Documents/Algorithm-materials/fast-fourier-transform/materials/fft-before.wav")
    out_path = input_path.with_name("fff_cleaned.wav")

    # Read the WAV file.
    with wave.open(str(input_path), "rb") as wav:
        params = wav.getparams()

        if params.sampwidth != 2:
            raise ValueError("Expected a 16-bit PCM WAV file.")

        samples = np.frombuffer(wav.readframes(params.nframes), dtype="<i2")
        samples = samples.reshape(-1, params.nchannels).astype(float)

        #convert each audio channel to the frequency domain.

        spectrum = np.fft.rfft(samples, axis = 0)
        frequencies = np.fft.rfftfreq(len(samples), d = 1 / params.framerate)

        #Remove the 50 Hz hum.
        spectrum[(frequencies >= 49) & (frequencies <= 51)] = 0

        # Convert back to audio samples.
        cleaned = np.fft.irfft(spectrum, n = len(samples), axis = 0)
        cleaned = np.clip(np.rint(cleaned), -32768, 32767).astype("<i2")

        # save the filtered recording.
        with wave.open(str(out_path), "wb") as wav:
            wav.setparams(params)
            wav.writeframes(cleaned.tobytes())

        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()

    