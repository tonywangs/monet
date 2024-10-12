import streamlit as st
import asyncio
import websockets
import json
import base64
from audio_recorder_streamlit import audio_recorder

# Streamlit UI for file uploads
st.title("AI Canvas Logo Generator")

# Upload other files
uploaded_file = st.file_uploader("Upload files", type=["jpg", "png", "pdf", "docx"])

# Audio recording
st.write("Record your audio description:")
audio_bytes = audio_recorder()

# Button to start processing
if st.button("Generate Logo"):
    if audio_bytes and uploaded_file:
        # Read file contents
        other_file_bytes = uploaded_file.read()
        
        # Run async function to send data via websockets
        asyncio.run(send_data_to_backend(audio_bytes, other_file_bytes))
    else:
        st.warning("Please provide both audio input and upload a file.")

# Async function to connect to the backend and send the data
async def send_data_to_backend(audio_data, file_data):
    uri = "ws://localhost:8000"  # Replace with your backend WebSocket URI

    async with websockets.connect(uri) as websocket:
        data_to_send = {
            "audio_data": base64.b64encode(audio_data).decode('utf-8'),
            "file_data": base64.b64encode(file_data).decode('utf-8'),
        }
        await websocket.send(json.dumps(data_to_send))
        response = await websocket.recv()
        st.write("Response from backend:", response)

# Display the generated logo (assuming the backend returns an image URL)
if 'response' in locals():
    try:
        response_data = json.loads(response)
        if 'logo_url' in response_data:
            st.image(response_data['logo_url'], caption="Generated Logo")
    except json.JSONDecodeError:
        st.error("Invalid response from backend")
