import io
import picamera
import PIL.Image

RESOLUTION = (640, 480)

_camera = picamera.PiCamera();
#_camera.color_effects = (128, 128)
_camera.resolution = RESOLUTION
#_camera.start_preview()

def _image_path(name):
    return '/home/pi/kasse/images/' + name + '.jpg'

def take_picture():
    stream = io.BytesIO()
    _camera.capture(stream, format='jpeg', resize=RESOLUTION)
    stream.seek(0)
    return PIL.Image.open(stream)

def save_picture(name):
    _camera.capture(_image_path(name))

def load_picture(name):
    return PIL.Image.open(_image_path(name))
