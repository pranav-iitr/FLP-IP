import cv2
import socketio
import base64
import requests


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
print(data)
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
url = 0
cap = cv2.VideoCapture(url)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        cap.release()
        cap = cv2.VideoCapture(url)

    else:
        # Process the frame (resize, crop, or other operations as needed)
        # For example, resizing the frame to a specific width and height
        if counter%3==0:
            frame = cv2.resize(frame, (640, 480))
    
            # Send the processed frame to the server
            send_image(frame)
            
            # Display the frame locally (optional)
        counter += 1 
        print("send",counter)
        cv2.imshow('Local Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Disconnect from the Socket.IO server when the program exits
client.disconnect()
