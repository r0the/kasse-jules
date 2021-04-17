import io
import picamera
import PIL.Image

RESOLUTION = (640, 480)

_camera = picamera.PiCamera();
#_camera.color_effects = (128, 128)
_camera.resolution = RESOLUTION
#_camera.start_preview()

def take_picture():
    stream = io.BytesIO()
    _camera.capture(stream, format='jpeg', resize=RESOLUTION)
    stream.seek(0)
    return PIL.Image.open(stream)
