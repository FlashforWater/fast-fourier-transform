Our problem is removing an unwanted hum from audio. I generated a two-second recording containing:
    A 440Hz tone we want to keep.
    A 50Hz hum we want to remove.
    Some background niose.
The audio is synthetic, so we know exactly what a successful result should be.

How we slove it

    1. Record samples. Each number measures the sound's amplitude at one moment. Here, 8,000 samples per second for two seconds gives 16,000 numbers.
    2. Apply the FFT. It expresses those samples as frequency components. We find strong components at appoximately 50 Hz and 440 Hz.
    3. Remove unwanted component. We set the frequency coefficients between 49 and 51 Hz to zero. This is a narrow frequency filter, often called a notch filter.
    4. Apply the inverse FFT. It converts the edited frequency representation back into samples.

The measured result was:
Component	            Amplitude before	       Amplitude after
50 Hz hum	                  0.450	              Approximately zero
440 Hz useful tone	          0.250	                     0.250

# x contains the recorded samples; fs is the sampling rate.
X = np.fft.rfft(x)
frequencies = np.fft.rfftfreq(len(x), d=1/fs)

X[(frequencies >= 49) & (frequencies <= 51)] = 0

cleaned = np.fft.irfft(X, n=len(x))