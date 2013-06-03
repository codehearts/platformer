from pyglet.image import SolidColorImagePattern

def dummy_image(width, height, color=(0,0,0,0)):
	"""Creates a dummy image of the specified dimensions."""
	return SolidColorImagePattern(color).create_image(width, height)
