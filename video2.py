import cv2
import socketio
import base64
import requests
import argparse

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument('--id', type=str)
parser.add_argument('--secrete', type=str)
args = parser.parse_args()

print(args)

response = requests.get(f"http://localhost:8000/api/retrive/?id={args.id}&secret={args.secrete}")
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

# Function to send the image to the server
def send_image(image):
    # Encode the image as JPEG and then as Base64
    _, buffer = cv2.imencode('.jpg', image)
    jpg_bytes = base64.b64encode(buffer)

    # Convert bytes to string for Socket.IO
    jpg_str = jpg_bytes.decode('utf-8')

    # Emit the 'stream' event with the Base64-encoded image and room ID
    client.emit('stream', {'image': jpg_str, 'room': room_id})

# Open the video capture device (camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Process the frame (resize, crop, or other operations as needed)
    # For example, resizing the frame to a specific width and height
    frame = cv2.resize(frame, (640, 480))

    # Send the processed frame to the server
    send_image(frame)

    # Display the frame locally (optional)
    cv2.imshow('Local Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Disconnect from the Socket.IO server when the program exits
client.disconnect()
