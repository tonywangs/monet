import websocket

import json
import base64

import librosa
import soundfile as sf
import numpy as np

example_wav, sr = sf.read("logo_top_left.wav")
print(sr)

ws = websocket.create_connection("ws://localhost:8765")

# example_wav = example_wav[:, 0]

print("created websocket")

print(example_wav.shape)

example_wav_base64 = base64.b64encode(example_wav.tobytes()).decode("utf-8")

# ws.send(example_wav_base64)

example_json = {
        "event": "audio",
        "payload": example_wav_base64
        }

example_json_str = json.dumps(example_json)

ws.send(example_json_str)

logo_file = open("logo.jpg", "rb")

logo_file_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

ws.send(json.dumps({
    "event": "file",
    "payload": logo_file_base64
    }))

ws.recv()
ws.recv()

# print(result)

ws.close()
