from game.settings.general_settings import FRAME_LENGTH, FPS

def simulate_time(seconds, update_object):
	"""Simulates time by calling the given update function every frame for the given amount of time."""
	map(lambda x: update_object.update(FRAME_LENGTH), xrange(int(FPS * seconds)))
