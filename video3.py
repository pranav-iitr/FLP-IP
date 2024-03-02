import cv2
import socketio
import base64
import requests
import numpy as np
import rtsp
import io
from PIL import Image

response = requests.get(f"http://b.esummit.in/api/retrive/?id={1}&secret=km4rR4LKV44eu0sqbi4YDg")
data = response.json()
print(data)
# Initialize Socket.IO server
sio = socketio.Server()

# Create a Socket.IO client
client = socketio.Client()

# Connect to the server
client.connect(data['url'])

# Room ID to join
room_id = data['room_id']
counter = 0

cap = cv2.VideoCapture(0)

# Function to send the image to the server
def send_image(pil_image):
    # Convert the PIL Image to bytes in JPEG format
    jpg_buffer = io.BytesIO()
    pil_image.save(jpg_buffer, format='JPEG')

    # Convert the JPEG bytes to Base64
    jpg_bytes = base64.b64encode(jpg_buffer.getvalue())

    # Convert bytes to string for Socket.IO
    jpg_str = jpg_bytes.decode('utf-8')

    # Emit the 'stream' event with the Base64-encoded image and room ID
    client.emit('stream', {'image': jpg_str, 'room': room_id})


# Open the video capture device (camera)
    
# url = "rtsp://127.0.0.1:8554/live"
# rtsp_server_uri = 'rtsp://127.0.0.1:8554/live'
# client_RT = rtsp.Client(rtsp_server_uri=rtsp_server_uri, verbose=True)

print("started")
while True:
    ret,frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the numpy array to a Pillow Image
    image = Image.fromarray(rgb_frame)

    # image = client_RT.read()
        
        # Check if the image is not None before showing it
    if image is not None:


        if counter%3==0:
            send_image(image)

        counter += 1 
        print("working")
    cv2.imshow('Local Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cv2.destroyAllWindows()

# Disconnect from the Socket.IO server when the program exits
client.disconnect()