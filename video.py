import cv2
import numpy as np
import rtsp

rtsp_server_uri = 'rtsp://127.0.0.1:8554/live'
client = rtsp.Client(rtsp_server_uri=rtsp_server_uri, verbose=True)

try:
    print(f"Connected to video source {rtsp_server_uri}.")
    
    while True:
        image = client.read()
        print(image)
        # Check if the image is not None before showing it
        if image is not None:
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imshow('RTSP Stream', image_np)

        # Break the loop when the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    client.close()
    cv2.destroyAllWindows()  # Close any open OpenCV windows
    print(f"Disconnected from {rtsp_server_uri}.")


