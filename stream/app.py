import os
import gi
gi.require_version('Gst', '1.0') 
from gi.repository import Gst
from base_camera import BaseCamera

Gst.init(None)

class Camera(BaseCamera):
	video_device = "/dev/video0"

	@staticmethod
	def set_video_device(device):
		Camera.video_device = device

	def __init__(self):
		if os.environ.get('GST_CAMERA_VIDEO_DEVICE'):
			Camera.set_video_device(int(os.environ['GST_CAMERA_VIDEO_DEVICE']))
		super(Camera, self).__init__()

	@staticmethod
	def frames():
		MJPEG_PIPELINE = f"v4l2src device={Camera.video_device} ! jpegenc ! appsink name=sink"
		pipeline = Gst.parse_launch(MJPEG_PIPELINE)
		sink = pipeline.get_by_name("sink")

		# Start playing
		ret = pipeline.set_state(Gst.State.PLAYING)
		if ret == Gst.StateChangeReturn.FAILURE:
			print("Unable to set the pipeline to the playing state.")
			exit(-1)

		try:
			while True:
				sample = sink.emit("pull-sample")
				buf = sample.get_buffer()
				#print("Timestamp: ", buf.pts)
				yield buf.extract_dup(0, buf.get_size())
		finally:
			pipeline.set_state(Gst.State.NULL)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'