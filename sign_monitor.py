import time
from collections import Counter
import simpleaudio as sa

class SignMonitor:
    def __init__(self):
        self.start_signal = "five" # the label that triggers 'hey google'
        self.initial_audio = "hey_google.wav"
        self.interval = 5 # the time between the 'hey google' and the command
        self.timestamp = None # marks when the 'hey google' was triggered
        self.is_listening = False # whether or not 'hey google was triggered
        self.labels = [] # labels recieved after 'hey google'
        self.threshold = 0.5 # how sensitive we want our action command trigger to be
        self.actions = {
            "peace": "weather.wav",
            "five": "skip",
            "thumbs_up": "timer.wav"
        }

    def has_expired(self):
        return self.timestamp is not None and \
            int(time.time()) >= self.timestamp + self.interval

    def start_listening(self):
        self.timestamp = int(time.time())
        self.is_listening = True
        print("recieved start signal, listening for action signal")

    def stop_listening(self):
        self.timestamp = None
        self.is_listening = False
        self.labels = []
        print("stopping listening until recieve start signal")

    def set_action(self):
        if len(self.labels) > 0:
            label, count = Counter(self.labels).most_common()[0]
            if count / len(self.labels) >= self.threshold:
                print("length of labels is " + str(len(self.labels)))
                print("most common was " + str(label) + " with count of " + str(count))
                audio_file = self.actions[label]
                if audio_file is not "skip":
                    print("playing " + str(audio_file))
                    sa.WaveObject.from_wave_file(audio_file).play()
                else:
                    print("no discernable signal received at this time")
        self.stop_listening()


    def update(self, label):
        if self.is_listening:
            if self.has_expired():
                self.set_action()
            elif label != self.start_signal:
                self.labels.append(label)
        elif label == self.start_signal:
            self.start_listening()
            print("playing initializer")
            sa.WaveObject.from_wave_file(self.initial_audio).play()
