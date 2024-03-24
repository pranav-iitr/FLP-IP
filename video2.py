import socketio
import base64
import requests
import rtsp
import io


response = requests.get(f"https://backend.gammarotors.com/api/retrive/?id={1}&secret=Jl3bDV9y_ko929DqY1kTRw")
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
    try:
        client.emit('stream', {'image': jpg_str, 'room': room_id})
        print("image sent")
    except Exception as e:
        print(e)


# Open the video capture device (camera)

rtsp_server_uri = 'rtsp://127.0.0.1:8554/live'
print("connecting to rtsp")
client_RT = rtsp.Client(rtsp_server_uri=rtsp_server_uri, verbose=True)
print("connected to rtsp")
while True:

    image = client_RT.read()
        
        # Check if the image is not None before showing it
    if image is not None:
        print("image is not none")


        if counter%4==0:
            send_image(image)

        counter += 1 
        # cv2.imshow('Local Stream', frame)

    if  0xFF == ord('q'):
            break




# Disconnect from the Socket.IO server when the program exits
client.disconnect()