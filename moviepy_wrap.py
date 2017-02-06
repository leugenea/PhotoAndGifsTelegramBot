from __future__ import print_function

import os
import shutil
from datetime import datetime
from os import path

from moviepy.video.fx import resize
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

import cv_wrap
import settings


def get_gif():
    print("Capturing GIF...", end=' ')
    filename_wo_ext = path.join(settings.IMAGES_CACHE_DIR, str(datetime.now()))
    if not path.exists(filename_wo_ext) or not path.isdir(filename_wo_ext):
        os.makedirs(filename_wo_ext)

    mp4_filename = filename_wo_ext + '.mp4'

    camera = cv_wrap.open_camera()

    fps = cv_wrap.get_fps(camera)

    cv_wrap.skip_frames(camera, settings.ramp_frames)

    frames = []

    print("Got frames:", end=' ')
    for i in range(settings.images_in_gif):
        im = cv_wrap.get_picture(camera=camera,
                                 ddir=filename_wo_ext,
                                 filename=str(i) + '.png',
                                 ramp_frames=0)

        print(str(i + 1) + ',', end=' ')
        frames.append(im)

    cv_wrap.close_camera(camera)

    print("... Merging ...", end=' ')

    # clip = resize.resize(ImageSequenceClip(frames, fps), newsize=0.5)
    clip = ImageSequenceClip(frames, fps)
    clip.write_videofile(mp4_filename, fps=fps, audio=False)

    print('Cleaning up...', end=' ')

    shutil.rmtree(filename_wo_ext)

    print('Got MP4 ' + mp4_filename)

    return mp4_filename
