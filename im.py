from PIL import Image
import cv2
import numpy as np
# Specify the file path of the image
image_path = r'download.jpeg'

# Load the image using Pillow
image = Image.open(image_path)
print(image)
image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Display the image using OpenCV
cv2.imshow('RTSP Stream', image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()