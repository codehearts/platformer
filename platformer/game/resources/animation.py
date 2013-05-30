# TODO This file should probably be deleted
import pyglet
from .. import util

def make_from(sheet, frames, times):
    # Ensure that our times list is the same length as our frames list
    if len(times) < len(frames):
        times = util.equalize_list_sizes(frames, times)

    animation_frames = []
    for i in xrange(len(frames)):
        animation_frames.append(pyglet.image.AnimationFrame(sheet[frames[i]], times[i]))

    return pyglet.image.Animation(animation_frames)
