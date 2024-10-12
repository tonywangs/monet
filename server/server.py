import os
import base64
import json
import sys
import websockets
import asyncio

import websocket

import numpy as np

oai_ws = websocket.create_connection("wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01", header=[
    "Authorization: Bearer " + os.environ["OPENAI_API_KEY"],
    "OpenAI-Beta: realtime=v1"
    ])

print("Sending on oai websocket")
oai_ws.send(json.dumps({
    "type": "response.create",
    "response": {
        "modalities": ["text"],
        "instructions": "Please assist the user.",
        }
    }));

async def receive_oai():
    while True:
        response = oai_ws.recv()
        print(response)

async def handle_audio(audio):
    print(audio.shape)

def parse_audio(payload):
    audio_base64 = payload.encode("utf-8")
    audio = np.frombuffer(base64.b64decode(audio_base64), dtype=np.float32)
    return audio

async def handle_event(websocket):
    async for message in websocket:
        
        message = json.loads(message)
        
        print(message["event"])

        if message["event"] == "audio":
            audio = parse_audio(message["payload"])
            await handle_audio(audio)

        await websocket.send("received")

async def serve():
    async with websockets.serve(
            handle_event, "localhost", 8765, max_size=sys.maxsize):

        await asyncio.Future()

async def main():
    await asyncio.gather(
            serve()
            # receive_oai()
            )

if __name__ == "__main__":
    asyncio.run(main())
