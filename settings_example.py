from os import path

TOKEN = 'YOUR:TOKEN'
IMAGES_CACHE_DIR = path.join(path.dirname(path.realpath(__file__)), 'images_cache')
camera_port = 0
camera_photo_size = (1280, 960)
camera_gif_size = (320, 240)
ramp_frames = 10
images_in_gif = 120
gif_format = '.mp4'  # or '.gif'
