import streamlit as st
import asyncio
import websockets
import json
import base64
import numpy as np
import io
import streamlit_mic_recorder
from streamlit_mic_recorder import mic_recorder


# Streamlit UI for file uploads
st.title("AI Canvas Logo Generator")


# Upload other files
uploaded_file = st.file_uploader("Upload files", type=["jpg", "png", "pdf", "docx"])


# Audio recording
st.write("Record your audio description:")
audio = mic_recorder(
   start_prompt="Start recording",
   stop_prompt="Stop recording",
   just_once=False,
   use_container_width=False
)


# Async function to connect to the backend and send the data
async def send_data_to_backend(audio_data, file_data):
   uri = "wss://826a-4-39-199-2.ngrok-free.app"  # Changed to "wss://" instead of "ws://"
  
   async with websockets.connect(uri) as websocket:
       # Encode audio and file data to base64
       audio_base64 = base64.b64encode(audio_data).decode('utf-8')
       file_base64 = base64.b64encode(file_data).decode('utf-8')
      
       # Prepare JSON payload
       payload1 = {
           "event": "audio",
           "payload": audio_base64
       }


       payload2 = {
           "event": "file",
           "payload": file_base64
       }
      
       # Send data to backend
       await websocket.send(json.dumps(payload1))
       await websocket.send(json.dumps(payload2))
      
       # Wait for response
       response = await websocket.recv()
       return response


# Button to start processing
if st.button("Generate Logo"):
   if audio and uploaded_file:
       print(audio["sample_rate"])
       # Read file contents
       other_file_bytes = uploaded_file.read()
      
       # Run async function to send data via websockets
       response = asyncio.run(send_data_to_backend(audio['bytes'], other_file_bytes))
       st.write(f"Backend response: {response}")
   else:
       st.warning("Please provide both audio input and upload a file.")


# Display the generated logo (assuming the backend returns an image URL)
if 'response' in locals():
   try:
       response_data = json.loads(response)
       if 'logo_url' in response_data:
           st.image(response_data['logo_url'], caption="Generated Logo")
   except json.JSONDecodeError:
       st.error("Invalid response from backend")
