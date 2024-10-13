import io
import openai
import os
import base64
import json
import sys
import websockets
import asyncio
import soundfile as sf

from function_calls import call_openai_function

import websocket

import torch
import torchaudio

import numpy as np

client = openai.OpenAI()

oai_ws = websocket.create_connection("wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01", header=[
    "Authorization: Bearer " + os.environ["OPENAI_API_KEY"],
    "OpenAI-Beta: realtime=v1"
    ])

oai_ws.send(json.dumps({
    "type": "session.update",
    "session": {
        "modalities": ["text", "audio"],
        "instructions": "Your knowledge cutoff is 2023-10. You are a helpful assistant.",
        "voice": "alloy",
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16",
        "input_audio_transcription": {
            "model": "whisper-1"
        },
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 200
        },
        "tool_choice": "auto",
        "temperature": 0.8
    }
}))

print("Sending on oai websocket")

def send_oai_audio(audio):
    oai_ws.send(json.dumps({
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "audio": audio
                    }
                ]
            }
        }));
    oai_ws.send(json.dumps({
        "type": "response.create"
        }))

async def receive_oai():
    await asyncio.to_thread(recv_oai_blocking)

def recv_oai_blocking():
    while True:
        response = oai_ws.recv()
        response_json = json.loads(response)
        print("response:", response_json["type"])

        if response_json["type"] == "response.audio_transcript.delta":
            print(response_json)

def transcribe_audio(audio):
    transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="text"
            )

    try:
        call_openai_function(transcription)
    except Exception as e:
        print(e)


async def handle_audio(audio):
    print(audio.shape)

def parse_audio(payload):
    audio_base64 = payload.encode("utf-8")
    audio = np.frombuffer(base64.b64decode(audio_base64), dtype=np.float32)
    return audio

def buffer_audio(audio):
    sf.write("temp.wav", audio, 16000)
    return open("temp.wav", "rb")

def parse_file(payload):
    file = payload.encode("utf-8")
    file = base64.b64decode(file)

    return file

async def handle_event(websocket):
    async for message in websocket:
        
        message = json.loads(message)
        
        print(message["event"])

        if message["event"] == "audio":
            # audio_44khz = parse_audio(message["payload"])
            # sf.write("temp.wav", audio_44khz, 48000)
            # break
            # audio_44khz = torch.tensor(audio_44khz)
            # print(audio_44khz.shape)
            # audio = torchaudio.functional.resample(audio_44khz, 41000, 16000)
            # print(audio.shape)
            # audio = audio.numpy()
            # print(audio.shape)
            # audio_base64 = base64.b64encode(audio.numpy()).decode("utf-8")


            # send_oai_audio(audio_base64)

            audio = parse_file(message["payload"])
            with open("audio.wav", "wb") as audio_file:
                audio_file.write(audio)

            with open("audio.wav", "rb") as audio_file:
                transcribe_audio(audio_file)

        elif message["event"] == "file":
            file = parse_file(message["payload"])
            logo = open("logo.jpg", "wb")
            logo.write(file)

        # await websocket.send("received")

async def serve():
    async with websockets.serve(
            handle_event, "localhost", 8765, max_size=sys.maxsize):

        await asyncio.Future()

async def main():
    print("Starting server")
    await asyncio.gather(
            serve()
            # receive_oai()
            )

if __name__ == "__main__":
    asyncio.run(main())
