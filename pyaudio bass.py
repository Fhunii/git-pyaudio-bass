import tkinter as tk
import numpy as np
import sounddevice as sd

class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Faders")

        # Initialize variables
        self.volume = 0.0
        self.freq = 30

        # Volume Fader
        tk.Label(root, text="Volume").pack()
        self.volume_fader = tk.Scale(root, from_=0, to_=1, orient=tk.VERTICAL, resolution=0.01, command=self.update_volume, length=300)
        self.volume_fader.set(self.volume)
        self.volume_fader.pack(side=tk.LEFT)

        # Frequency Fader
        tk.Label(root, text="Frequency (Hz)").pack()
        self.freq_fader = tk.Scale(root, from_=30, to_=80, orient=tk.HORIZONTAL, resolution=1, command=self.update_freq, length=300)
        self.freq_fader.set(self.freq)
        self.freq_fader.pack(side=tk.BOTTOM)

        # Start audio stream
        self.stream = sd.OutputStream(samplerate=44100, channels=1, callback=self.audio_callback)
        self.stream.start()

        # Update the audio stream
        self.update_audio()

    def update_volume(self, value):
        self.volume = float(value)

    def update_freq(self, value):
        self.freq = float(value)
        self.update_audio()

    def audio_callback(self, outdata, frames, time, status):
        t = np.linspace(0, frames / 44100, frames, endpoint=False)
        signal = self.volume * np.sin(2 * np.pi * self.freq * t)
        outdata[:] = signal.reshape(-1, 1)

    def update_audio(self):
        self.stream.stop()
        self.stream.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioApp(root)
    root.mainloop()
