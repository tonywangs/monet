import websocket

import json
import base64

import soundfile as sf
import numpy as np

example_wav, sr = sf.read("logo_top_left.wav")

ws = websocket.create_connection("ws://localhost:8765")

example_wav = example_wav[:, 0]

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


result = ws.recv()

print(result)

ws.close()
