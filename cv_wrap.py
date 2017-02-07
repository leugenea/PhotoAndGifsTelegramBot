from __future__ import print_function

import cv2
from datetime import datetime
from os import path
import os

import settings


def open_camera(camera_size):
    camera = cv2.VideoCapture(settings.camera_port)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_size[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_size[1])
    return camera


def close_camera(camera):
    camera.release()


def get_image_instant(camera):
    retval, im = camera.read()
    return im


def skip_frames(camera, frames_to_skip):
    for i in range(frames_to_skip):
        get_image_instant(camera)


def get_fps(camera):
    return camera.get(cv2.CAP_PROP_FPS)


def get_picture(camera=None, ddir=settings.IMAGES_CACHE_DIR, filename=None, ramp_frames=settings.ramp_frames,
                camera_size=settings.camera_photo_size):
    if not path.exists(ddir) or not path.isdir(ddir):
        os.makedirs(ddir)
    image_path = path.join(ddir, (str(datetime.now()) + ".png") if filename is None else filename)

    had_camera = camera is not None

    if not had_camera:
        camera = open_camera(camera_size)

    skip_frames(camera, ramp_frames)

    image = get_image_instant(camera)

    if not had_camera:
        close_camera(camera)

    cv2.imwrite(image_path, image)

    return image_path
