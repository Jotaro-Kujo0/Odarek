import config
import os
import json


class Commander:
    def __init__(self):
        self.recognizer = None
        self.audio_stream = None

        if os.path.exists(config):
            print("bumbum")
