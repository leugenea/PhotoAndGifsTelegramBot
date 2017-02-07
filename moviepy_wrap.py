from __future__ import print_function

import os
import shutil
from datetime import datetime
from os import path

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

import cv_wrap
import settings


def get_gif():
    print("Capturing GIF...", end=' ')
    filename_wo_ext = path.join(settings.IMAGES_CACHE_DIR, str(datetime.now()))
    if not path.exists(filename_wo_ext) or not path.isdir(filename_wo_ext):
        os.makedirs(filename_wo_ext)

    result_filename = filename_wo_ext + '.mp4'

    camera = cv_wrap.open_camera(settings.camera_gif_size)

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

    clip = ImageSequenceClip(frames, fps)
    if settings.gif_format == '.mp4':
        clip.write_videofile(result_filename, fps=fps, audio=False)
    else:
        clip.write_gif(result_filename, fps=fps, program='ffmpeg')

    print('Cleaning up...', end=' ')

    shutil.rmtree(filename_wo_ext)

    print('Got ' + settings.gif_format.upper() + ' ' + result_filename)

    return result_filename
