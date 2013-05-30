from animation_frame import AnimationFrame
from pyglet.clock import schedule_once, unschedule
from pyglet.event import EventDispatcher
from pyglet.image import ImageGrid

# TODO Tests for this class
class BasicAnimation(EventDispatcher):
	"""A basic animation.

	Attributes:
		frames (list of :class:`game.animation.animation_frame.AnimationFrame`): The frames that make up the animation.
		frame_count (number): The number of frames in the animation.
		current_frame_index (number): The index of the currently drawn frame in the animation's frame list.
		current_frame (:class:`game.animation.animation_frame.AnimationFrame`): The currently drawn animation frame.
		delay (number): The amount of time (in seconds) to wait on the first frame before animating.
		elapsed_time (number): The amount of time (in seconds) that the animation has been animated.
		is_infinite (bool): Whether this animation loops infinitely or not.
		total_loops: A number if this animation loops finitely, or ``None`` if this animation loops infinitely.
		total_duration: The number of seconds this animation runs for in total, or ``None`` if the animation loops infinitely.
		current_loop (number): The current loop in the animation.
		is_finished (bool): Whether this animation has finished animating.
	"""

	def __init__(self, frames, loops=1, delay=0):
		"""Creates a new animation.

		Args:
			frames (list of :class:`game.animation.animation_frame.AnimationFrame`): The frames that make up the animation.

		Kwargs:
			loops: The number of times to loop the animation, or ``True`` to loop infinitely.
			delay (number): The amount of time (in seconds) to wait on the first frame before animating.
		"""
		self.frames = frames

		self.frame_count = len(frames)
		self.current_frame = frames[0]
		self.current_frame_index = 0

		self.delay = delay

		self.is_infinite = (loops is True)
		if self.is_infinite:
			self.total_loops = None
			self.total_duration = None
		else:
			self.total_loops = loops
			self.total_duration = delay + loops * sum([frame.duration for frame in frames])
		self.current_loop = 1
		self.elapsed_time = 0

		self.is_finished = False
		schedule_once(self._schedule_frame_change, frames[0].duration + delay, self._get_next_frame_index())


	def update(self, dt):
		"""Updates the animation."""
		self.elapsed_time += dt

	def draw(self, x=0, y=0):
		"""Draws the animation with its anchor point (usually the bottom left corner) at the given coordinates.

		Kwargs:
			x (number): The x coordinate to draw the animation's anchor point at.
			y (number): The y coordinate to draw the animation's anchor point at.
		"""
		self.current_frame.image.blit(x, y, 0)

	def _change_frame(self, frame_index):
		"""Changes the currently drawn frame in the animation.

		Args:
			frame_index (number): The index of the new frame to draw in the ``frames`` list.
		"""
		# Increment the loop counter if we've moved to a new loop
		if frame_index < self.current_frame_index and not self.is_infinite:
			self.current_loop += 1

		self.current_frame_index = frame_index
		self.current_frame = self.frames[frame_index]

	# TODO There is quite a bit of timing error when drawing frames. The duration of each frame should be tweaked to work with the intended frame rate. Look at how pyglet.sprite.Sprite handle this.
	# TODO It'd be easier to sort out the timing issues with tests
	def _schedule_frame_change(self, dt, frame_index):
		"""Schedules the next frame change.

		Args:
			dt (number): The time delta (in seconds) between the current frame and the previous frame.
			frame_index (number): The index of the new frame to draw in the ``frames`` list.
		"""
		# Calculate the difference between how long it actually took and how long it was supposed to take
		time_error = dt - self.current_frame.duration

		self._change_frame(frame_index)
		next_frame_index = self._get_next_frame_index()

		# Schedule another frame change if there's another frame to draw, otherwise the animation has ended
		if next_frame_index is not None:
			schedule_once(self._schedule_frame_change, self.current_frame.duration - time_error, next_frame_index)
		else:
			self._handle_animation_end()

	def _get_next_frame_index(self):
		"""Determines the index of the next frame to draw in the ``frames`` list.

		Returns:
			A numerical index of the ``frames`` list if the animation has a next frame,
			or None if the last frame has already been drawn.
		"""
		next_frame_index = self.current_frame_index + 1

		# In this case, either the animation needs to loop or the animation is finished
		if next_frame_index == self.frame_count:
			# All loops have been completed, there is no next frame
			if self.current_loop == self.total_loops:
				return None

			return 0

		return next_frame_index

	def _get_previous_frame_index(self):
		"""Determines the index of the previously drawn frame in the ``frames`` list.

		Returns:
			A numerical index of the ``frames`` list if the animation has a previous frame,
			or None if the the current frame is the first frame.
		"""
		previous_frame_index = self.current_frame_index - 1

		# In this case, either the animation looped or the current frame is the first frame of the first loop
		if previous_frame_index < 0:
			# The current frame is the first frame in the first loop
			if self.current_loop == 0:
				return None

			return self.frame_count - 1

		return previous_frame_index

	def finish(self):
		"""Finishes the animation.

		The animation will cease to animate itself and
		an 'on_animation_end' event is dispatched.
		"""
		self.is_finished = True
		unschedule(self._schedule_frame_change)

		self.dispatch_event('on_animation_end', self)

	def _handle_animation_end(self):
		"""Handler for when the animation is finished."""
		self.finish()

	@staticmethod
	def _create_animation_frame_image(image):
		"""Creates an object for a :class:`game.animation.animation_frame.AnimationFrame` image from a :class:`pyglet.image.AbstractImage`.

		Args:
			image (:class:`pyglet.image.AbstractImage`): The image to convert for use as a :class:`game.animation.animation_frame.AnimationFrame` image.

		Returns:
			An object to be used as a :class:`game.animation.animation_frame.AnimationFrame` image.
		"""
		return image.get_texture()

	@classmethod
	def from_image_sequence(cls, sequence, durations, *args, **kwargs):
		"""Creates an animation from a list of images and a list of durations.

		Args:
			sequence (list of :class:`game.animation.animation_frame.AnimationFrame`): Images that make up the animation, in sequence.
			durations (list of numbers): A list of the number of seconds to display each image.

		Returns:
			A :class:`game.animation.basic_animation.BasicAnimation` object.
		"""
		frames = [AnimationFrame(sequence[frame], durations[frame]) for frame in xrange(len(sequence))]

		return cls(frames, *args, **kwargs)

	@classmethod
	def from_image(cls, image, rows, cols, *args, **kwargs):
		"""Creates an animation from an image.

		Args:
			image (:class:`pyglet.image.AbstractImage`): An image containing the frames of an animation.
			rows (number): The number of rows of frames in the image.
			cols (number): The number of columns of frames in the image.

		Returns:
			A :class:`game.animation.basic_animation.BasicAnimation` object.
		"""
		image_grid = ImageGrid(image, rows, cols)
		sequence = map(cls._create_animation_frame_image, image_grid)

		return cls.from_image_sequence(sequence, *args, **kwargs)

# Register animation events
BasicAnimation.register_event_type('on_animation_end')
