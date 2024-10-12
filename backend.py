import websockets
import asyncio
import json

async def process_request(websocket, path):
    data = await websocket.recv()
    received_data = json.loads(data)
    
    # Extract and decode the files
    audio_data = bytes.fromhex(received_data["audio_data"])
    file_data = bytes.fromhex(received_data["file_data"])

    # Now handle the files (e.g., pass to AI model or process)
    print("Received audio and file data")
    
    # Send a response back to the frontend
    await websocket.send("Files received and processed!")

start_server = websockets.serve(process_request, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
