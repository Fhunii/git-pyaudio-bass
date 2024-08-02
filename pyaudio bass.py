import tkinter as tk
import numpy as np
import sounddevice as sd

class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Faders")

        # Initialize variables
        self.volume = 0.0
        self.freq = 30.0

        # Volume Fader
        tk.Label(root, text="Volume").pack()
        self.volume_fader = tk.Scale(root, from_=0, to_=0.5, orient=tk.VERTICAL, resolution=0.0001, command=self.update_volume, length=300)
        self.volume_fader.set(self.volume)
        self.volume_fader.pack(side=tk.LEFT)

        # Frequency Fader
        tk.Label(root, text="Frequency (Hz)").pack()
        self.freq_fader = tk.Scale(root, from_=30, to_=80, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_freq, length=300)
        self.freq_fader.set(self.freq)
        self.freq_fader.pack(side=tk.BOTTOM)

        # Audio stream setup
        self.stream = sd.OutputStream(samplerate=44100, channels=1, callback=self.audio_callback)
        self.stream.start()

        # Store current settings
        self.current_volume = self.volume
        self.current_freq = self.freq

    def update_volume(self, value):
        self.current_volume = float(value)

    def update_freq(self, value):
        self.current_freq = float(value)

    def audio_callback(self, outdata, frames, time, status):
        t = np.linspace(0, frames / 44100, frames, endpoint=False)
        signal = self.current_volume * np.sin(2 * np.pi * self.current_freq * t)
        outdata[:] = signal.reshape(-1, 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioApp(root)
    root.mainloop()
