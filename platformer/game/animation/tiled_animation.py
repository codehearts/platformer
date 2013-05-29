from animation_frame import AnimationFrame
from pyglet.clock import schedule_once, unschedule
from pyglet.event import EventDispatcher
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.image import ImageGrid, TileableTexture

class TiledAnimation(EventDispatcher):
	"""An animation which can be tiled efficiently.

	Attributes:
		frames (list of :class:`game.animation.animation_frame.AnimationFrame`): The frames that make up the animation.
		width (number): The width of the tiled animation.
		height (number): The height of the tiled animation.
		frame_count (number): The number of frames in the animation.
		current_frame (number): The index of the currently drawn frame in the animation's frame list.
		current_image (:class:`pyglet.image.TileableTexture`): The texture for the currently drawn frame's image.
		delay (number): The amount of time (in seconds) to wait on the first frame before animating.
		elapsed_time (number): The amount of time (in seconds) that the animation has been animated.
		is_infinite (bool): Whether this animation loops infinitely or not.
		total_loops: A number if this animation loops finitely, or ``None`` if this animation loops infinitely.
		total_duration: The number of seconds this animation runs for in total, or ``None`` if the animation loops infinitely.
		current_loop (number): The current loop in the animation.
		is_finished (bool): Whether this animation has finished animating.
	"""

	def __init__(self, frames, width, height, loops=0, delay=0):
		"""Creates a new tileable animation.

		Args:
			frames (list of :class:`game.animation.animation_frame.AnimationFrame`): The frames that make up the animation.
			width (number): The width of the tiled animation.
			height (number): The height of the tiled animation.

		Kwargs:
			loops: The number of times to loop the animation, or ``True`` to loop infinitely.
			delay (number): The amount of time (in seconds) to wait on the first frame before animating.
		"""
		self.frames = frames
		self.width = width
		self.height = height

		self.frame_count = len(frames)
		self.current_frame = 0 # TODO Rename this attribute
		self.current_image = frames[0].image
		self.delay = delay
		self.elapsed_time = 0

		self.is_infinite = (loops is True)
		if self.is_infinite:
			self.total_loops = None
			self.total_duration = None
		else:
			self.total_loops = loops
			self.total_duration = delay + (loops+1) * sum([frame.duration for frame in frames])
		self.current_loop = 0

		self.is_finished = False
		schedule_once(self._schedule_frame_change, delay + frames[0].duration, self._get_next_frame_index())


	def update(self, dt):
		"""Updates the animation."""
		self.elapsed_time += dt

	def draw(self, x=0, y=0):
		"""Draws the animation with its anchor point (usually the bottom left corner) at the given coordinates.

		Kwargs:
			x (number): The x coordinate to draw the animation's anchor point at.
			y (number): The y coordinate to draw the animation's anchor point at.
		"""
		if not self.is_finished:
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

			self.current_image.blit_tiled(x, y, 0, self.width, self.height)

	def _change_frame(self, frame):
		"""Changes the currently drawn frame in the animation.

		Args:
			frame (number): The index of the new frame to draw in the ``frames`` list.
		"""
		self.current_frame = frame
		self.current_image = self.frames[frame].image

	def _schedule_frame_change(self, dt, frame):
		"""Schedules the next frame change.

		Args:
			dt (number): The time delta (in seconds) between the current frame and the previous frame.
			frame (number): The index of the new frame to draw in the ``frames`` list.
		"""
		# Calculate the difference between how long it actually took and how long it was supposed to take
		time_error = dt - self.frames[self.current_frame].duration

		self._change_frame(frame)
		next_frame = self._get_next_frame_index()

		# Schedule another frame change if there's another frame to draw, otherwise the animation has ended
		if next_frame is not None:
			schedule_once(self._schedule_frame_change, self.frames[self.current_frame].duration - time_error, next_frame)
		else:
			self._handle_animation_end()

	def _get_next_frame_index(self):
		"""Determines the index of the next frame to draw in the ``frames`` list.

		Returns:
			A numerical index of the ``frames`` list if the animation has a next frame,
			or None if the last frame has already been drawn.
		"""
		next_frame = self.current_frame + 1

		# In this case, either the animation needs to loop or the animation is finished
		if next_frame == self.frame_count:
			# All loops have been completed, there is no next frame
			if self.current_loop == self.total_loops:
				return None

			# Otherwise, move on to the next loop
			if not self.is_infinite:
				self.current_loop += 1
			return 0

		return next_frame

	def delete(self):
		"""Deletes this animation."""
		pass

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

	@classmethod
	def from_image_sequence(cls, sequence, durations, *args, **kwargs):
		"""Creates an animation from a list of images and a list of durations.

		Args:
			frames (list of :class:`game.animation.animation_frame.AnimationFrame`): Images that make up the animation, in sequence.
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
		sequence = [TileableTexture.create_for_image(frame) for frame in image_grid]

		return cls.from_image_sequence(sequence, *args, **kwargs)

# Register animation events
TiledAnimation.register_event_type('on_animation_end')
