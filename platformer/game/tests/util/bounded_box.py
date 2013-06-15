from game.settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT
from math import ceil

"""Utilities for testing various aspects of :class:`game.bounded_box.BoundedBox` and its subclasses.

Any test class using these utilities is expected to have an ``expected_x``,
``expected_y``, ``expected_width``, ``expected_height``, and ``test_box``
property. The class should also provide its own ``create_box`` method which
accepts ``x``, ``y``, ``width``, and ``height`` as its arguments. The
method should return a BoundedBox object or an object of one of its
subclasses.

Methods provided by this class include:
	``run_intersection_tests`` to test bounding boxes within boxes.
	``run_box_equality_tests`` to test boxes for equality.
	``run_positioning_tests`` to test box positioning.
	``run_dimension_tests`` to test box dimensions.
"""

def run_intersection_tests(self):
	"""Runs tests on intersecting a BoundedBox with another BoundedBox."""
	# Larger than test box by 10 pixels on every side
	larger_box = self.create_box(-10, -10, 52, 52)

	# Test bounding within a larger box
	reset_test_box(self)
	self.expected_x = self.test_box.x
	self.expected_y = self.test_box.y
	self.expected_width = self.test_box.width
	self.expected_height = self.test_box.height

	self.test_box = self.test_box.get_intersection(larger_box)
	assert_coordinates(self, 'Bounded within a larger box.')
	assert_dimensions(self, 'Bounded within a larger box.')

	# Test bounding with a box that is entirely within the test box
	smaller_box = self.create_box(10, 10, 12, 12)

	reset_test_box(self)
	self.expected_x = 10
	self.expected_y = 10
	self.expected_width = self.test_box.width - 20
	self.expected_height = self.test_box.height - 20

	self.test_box = self.test_box.get_intersection(smaller_box)
	assert_coordinates(self, 'Bounded within a smaller box.')
	assert_dimensions(self, 'Bounded within a smaller box.')

	# Overlaps upper right corner of test box only
	upper_right_overlap_box = self.create_box(10, 10, 32, 32)

	reset_test_box(self)
	self.expected_x = 10
	self.expected_y = 10
	self.expected_width = self.test_box.width - 10
	self.expected_height = self.test_box.height - 10

	self.test_box = self.test_box.get_intersection(upper_right_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps upper right corner.')
	assert_dimensions(self, 'Bounded within a box which overlaps upper right corner.')

	# Overlaps upper left corner of test box only
	upper_left_overlap_box = self.create_box(-10, 10, 32, 32)

	reset_test_box(self)
	self.expected_x = 0
	self.expected_y = 10
	self.expected_width = self.test_box.width - 10
	self.expected_height = self.test_box.height - 10

	self.test_box = self.test_box.get_intersection(upper_left_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps upper left corner.')
	assert_dimensions(self, 'Bounded within a box which overlaps upper left corner.')

	# Overlaps lower right corner of test box only
	lower_right_overlap_box = self.create_box(10, -10, 32, 32)

	reset_test_box(self)
	self.expected_x = 10
	self.expected_y = 0
	self.expected_width = self.test_box.width - 10
	self.expected_height = self.test_box.height - 10

	self.test_box = self.test_box.get_intersection(lower_right_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps lower right corner.')
	assert_dimensions(self, 'Bounded within a box which overlaps lower right corner.')

	# Overlaps lower left corner of test box only
	lower_left_overlap_box = self.create_box(-10, -10, 32, 32)

	reset_test_box(self)
	self.expected_x = 0
	self.expected_y = 0
	self.expected_width = self.test_box.width - 10
	self.expected_height = self.test_box.height - 10

	self.test_box = self.test_box.get_intersection(lower_left_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps lower left corner.')
	assert_dimensions(self, 'Bounded within a box which overlaps lower left corner.')

	# Overlaps top of test box only
	top_overlap_box = self.create_box(0, 16, 32, 32)

	reset_test_box(self)
	self.expected_x = 0
	self.expected_y = 16
	self.expected_width = self.test_box.width
	self.expected_height = self.test_box.height - 16

	self.test_box = self.test_box.get_intersection(top_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps top side.')
	assert_dimensions(self, 'Bounded within a box which overlaps top side.')

	# Overlaps bottom of test box only
	bottom_overlap_box = self.create_box(0, 0, 32, 16)

	reset_test_box(self)
	self.expected_x = 0
	self.expected_y = 0
	self.expected_width = self.test_box.width
	self.expected_height = self.test_box.height - 16

	self.test_box = self.test_box.get_intersection(bottom_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps bottom side.')
	assert_dimensions(self, 'Bounded within a box which overlaps bottom side.')

	# Overlaps left of test box only
	left_overlap_box = self.create_box(0, 0, 16, 32)

	reset_test_box(self)
	self.expected_x = 0
	self.expected_y = 0
	self.expected_width = self.test_box.width - 16
	self.expected_height = self.test_box.height

	self.test_box = self.test_box.get_intersection(left_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps left side.')
	assert_dimensions(self, 'Bounded within a box which overlaps left side.')

	# Overlaps right of test box only
	right_overlap_box = self.create_box(16, 0, 16, 32)

	reset_test_box(self)
	self.expected_x = 16
	self.expected_y = 0
	self.expected_width = self.test_box.width - 16
	self.expected_height = self.test_box.height

	self.test_box = self.test_box.get_intersection(right_overlap_box)
	assert_coordinates(self, 'Bounded within a box which overlaps right side.')
	assert_dimensions(self, 'Bounded within a box which overlaps right side.')



def run_box_equality_tests(self):
	"""Runs tests which check the equality of bounded boxes."""
	box1 = self.create_box(0, 0, 32, 32)
	box2 = self.create_box(0, 0, 32, 32)
	box3 = self.create_box(32, 32, 128, 64)

	self.assertEqual(box1, box2, "Similar boxes claimed to be unequal.")
	self.assertNotEqual(box1, box3, "Different boxes claimed to be equal.")
	self.assertNotEqual(box2, box3, "Different boxes claimed to be equal.")

	# Test after a box's position has changed to be different from all other boxes
	box2.x = 16
	self.assertNotEqual(box1, box2, "Different boxes claimed to be equal after similar box was changed to be different.")
	self.assertNotEqual(box2, box3, "Different boxes claimed to be equal after different box was changed to remain different.")

	# Test after a box has been changed to be similar to another box
	box2.x = 32
	box2.y = 32
	box2.width = 128
	box2.height = 64
	self.assertNotEqual(box1, box2, "Different boxes claimed to be equal after different box was changed to remain different.")
	self.assertEqual(box2, box3, "Similar boxes claimed to be unequal after different box was changed to be similar.")



def run_box_initialization_tests(self):
	"""Tests the properties of a bounded box after intialization.

	The values in these tests are hardcoded to check conditions around tile
	boundaries, as well as values at negative coordinates.
	"""
	self.test_box = self.create_box(0, 0, TILE_SIZE * 2, TILE_SIZE * 2)
	self.expected_values = {
		'x': 0,
		'y': 0,
		'mid_x': TILE_SIZE,
		'mid_y': TILE_SIZE,
		'x2': TILE_SIZE * 2,
		'y2': TILE_SIZE * 2,
		'x_tile': 0,
		'y_tile': 0,
		'mid_x_tile': 0,
		'mid_y_tile': 0,
		'x2_tile': 1,
		'y2_tile': 1,
		'width': TILE_SIZE * 2,
		'height': TILE_SIZE * 2,
		'half_width': TILE_SIZE,
		'half_height': TILE_SIZE,
		'tile_width': 2,
		'tile_height': 2,
		'half_tile_width': 1,
		'half_tile_height': 1,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '2x2-tile box at (0, 0)')

	self.test_box = self.create_box(1, 1, TILE_SIZE * 2, TILE_SIZE * 2)
	self.expected_values = {
		'x': 1,
		'y': 1,
		'mid_x': TILE_SIZE + 1,
		'mid_y': TILE_SIZE + 1,
		'x2': TILE_SIZE * 2 + 1,
		'y2': TILE_SIZE * 2 + 1,
		'x_tile': 0,
		'y_tile': 0,
		'mid_x_tile': 1,
		'mid_y_tile': 1,
		'x2_tile': 2,
		'y2_tile': 2,
		'width': TILE_SIZE * 2,
		'height': TILE_SIZE * 2,
		'half_width': TILE_SIZE,
		'half_height': TILE_SIZE,
		'tile_width': 2,
		'tile_height': 2,
		'half_tile_width': 1,
		'half_tile_height': 1,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '2x2-tile box at (1, 1)')

	self.test_box = self.create_box(0, 0, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
	self.expected_values = {
		'x': 0,
		'y': 0,
		'mid_x': TILE_SIZE * 0.75,
		'mid_y': TILE_SIZE * 0.75,
		'x2': TILE_SIZE * 1.5,
		'y2': TILE_SIZE * 1.5,
		'x_tile': 0,
		'y_tile': 0,
		'mid_x_tile': 0,
		'mid_y_tile': 0,
		'x2_tile': 1,
		'y2_tile': 1,
		'width': TILE_SIZE * 1.5,
		'height': TILE_SIZE * 1.5,
		'half_width': TILE_SIZE * 0.75,
		'half_height': TILE_SIZE * 0.75,
		'tile_width': 1.5,
		'tile_height': 1.5,
		'half_tile_width': 0.75,
		'half_tile_height': 0.75,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '1.5x1.5-tile box at (0, 0)')

	self.test_box = self.create_box(TILE_SIZE // 2, TILE_SIZE // 2, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
	self.expected_values = {
		'x': TILE_SIZE // 2,
		'y': TILE_SIZE // 2,
		'mid_x': TILE_SIZE * 0.75 + TILE_SIZE // 2,
		'mid_y': TILE_SIZE * 0.75 + TILE_SIZE // 2,
		'x2': TILE_SIZE * 1.5 + TILE_SIZE // 2,
		'y2': TILE_SIZE * 1.5 + TILE_SIZE // 2,
		'x_tile': 0,
		'y_tile': 0,
		'mid_x_tile': 1,
		'mid_y_tile': 1,
		'x2_tile': 1,
		'y2_tile': 1,
		'width': TILE_SIZE * 1.5,
		'height': TILE_SIZE * 1.5,
		'half_width': TILE_SIZE * 0.75,
		'half_height': TILE_SIZE * 0.75,
		'tile_width': 1.5,
		'tile_height': 1.5,
		'half_tile_width': 0.75,
		'half_tile_height': 0.75,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '1.5x1.5-tile box at (TILE_SIZE/2, TILE_SIZE/2)')

	self.test_box = self.create_box(TILE_SIZE // 2 + 1, TILE_SIZE // 2 + 1, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
	self.expected_values = {
		'x': TILE_SIZE // 2 + 1,
		'y': TILE_SIZE // 2 + 1,
		'mid_x': TILE_SIZE * 0.75 + TILE_SIZE // 2 + 1,
		'mid_y': TILE_SIZE * 0.75 + TILE_SIZE // 2 + 1,
		'x2': TILE_SIZE * 1.5 + TILE_SIZE // 2 + 1,
		'y2': TILE_SIZE * 1.5 + TILE_SIZE // 2 + 1,
		'x_tile': 0,
		'y_tile': 0,
		'mid_x_tile': 1,
		'mid_y_tile': 1,
		'x2_tile': 2,
		'y2_tile': 2,
		'width': TILE_SIZE * 1.5,
		'height': TILE_SIZE * 1.5,
		'half_width': TILE_SIZE * 0.75,
		'half_height': TILE_SIZE * 0.75,
		'tile_width': 1.5,
		'tile_height': 1.5,
		'half_tile_width': 0.75,
		'half_tile_height': 0.75,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '1.5x1.5-tile box at (TILE_SIZE/2 + 1, TILE_SIZE/2 + 1)')

	self.test_box = self.create_box(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 2)
	self.expected_values = {
		'x': -TILE_SIZE,
		'y': -TILE_SIZE,
		'mid_x': 0,
		'mid_y': 0,
		'x2': TILE_SIZE,
		'y2': TILE_SIZE,
		'x_tile': -1,
		'y_tile': -1,
		'mid_x_tile': 0,
		'mid_y_tile': 0,
		'x2_tile': 0,
		'y2_tile': 0,
		'width': TILE_SIZE * 2,
		'height': TILE_SIZE * 2,
		'half_width': TILE_SIZE,
		'half_height': TILE_SIZE,
		'tile_width': 2,
		'tile_height': 2,
		'half_tile_width': 1,
		'half_tile_height': 1,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '2x2-tile box at (-TILE_SIZE, -TILE_SIZE)')

	self.test_box = self.create_box(-TILE_SIZE - 1, -TILE_SIZE - 1, TILE_SIZE * 2, TILE_SIZE * 2)
	self.expected_values = {
		'x': -TILE_SIZE - 1,
		'y': -TILE_SIZE - 1,
		'mid_x': -1,
		'mid_y': -1,
		'x2': TILE_SIZE - 1,
		'y2': TILE_SIZE - 1,
		'x_tile': -2,
		'y_tile': -2,
		'mid_x_tile': -1,
		'mid_y_tile': -1,
		'x2_tile': 0,
		'y2_tile': 0,
		'width': TILE_SIZE * 2,
		'height': TILE_SIZE * 2,
		'half_width': TILE_SIZE,
		'half_height': TILE_SIZE,
		'tile_width': 2,
		'tile_height': 2,
		'half_tile_width': 1,
		'half_tile_height': 1,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '2x2-tile box at (-TILE_SIZE - 1, -TILE_SIZE - 1)')

	self.test_box = self.create_box(-TILE_SIZE * 2.5, -TILE_SIZE * 2.5, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
	self.expected_values = {
		'x': -TILE_SIZE * 2.5,
		'y': -TILE_SIZE * 2.5,
		'mid_x': TILE_SIZE * 0.75 - TILE_SIZE * 2.5,
		'mid_y': TILE_SIZE * 0.75 - TILE_SIZE * 2.5,
		'x2': TILE_SIZE * 1.5 - TILE_SIZE * 2.5,
		'y2': TILE_SIZE * 1.5 - TILE_SIZE * 2.5,
		'x_tile': -3,
		'y_tile': -3,
		'mid_x_tile': -2,
		'mid_y_tile': -2,
		'x2_tile': -2,
		'y2_tile': -2,
		'width': TILE_SIZE * 1.5,
		'height': TILE_SIZE * 1.5,
		'half_width': TILE_SIZE * 0.75,
		'half_height': TILE_SIZE * 0.75,
		'tile_width': 1.5,
		'tile_height': 1.5,
		'half_tile_width': 0.75,
		'half_tile_height': 0.75,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '1.5x1.5-tile box at (-TILE_SIZE*2.5, -TILE_SIZE*2.5)')

	self.test_box = self.create_box(-TILE_SIZE * 2.5 + 1, -TILE_SIZE * 2.5 + 1, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
	self.expected_values = {
		'x': -TILE_SIZE * 2.5 + 1,
		'y': -TILE_SIZE * 2.5 + 1,
		'mid_x': TILE_SIZE * 0.75 - TILE_SIZE * 2.5 + 1,
		'mid_y': TILE_SIZE * 0.75 - TILE_SIZE * 2.5 + 1,
		'x2': TILE_SIZE * 1.5 - TILE_SIZE * 2.5 + 1,
		'y2': TILE_SIZE * 1.5 - TILE_SIZE * 2.5 + 1,
		'x_tile': -3,
		'y_tile': -3,
		'mid_x_tile': -2,
		'mid_y_tile': -2,
		'x2_tile': -1,
		'y2_tile': -1,
		'width': TILE_SIZE * 1.5,
		'height': TILE_SIZE * 1.5,
		'half_width': TILE_SIZE * 0.75,
		'half_height': TILE_SIZE * 0.75,
		'tile_width': 1.5,
		'tile_height': 1.5,
		'half_tile_width': 0.75,
		'half_tile_height': 0.75,
		'tile_width_span': 2,
		'tile_height_span': 2,
	}
	assert_expected_values(self, '1.5x1.5-tile box at (-TILE_SIZE*2.5 + 1, -TILE_SIZE*2.5 + 1)')



def run_positioning_tests(self):
	"""Tests the positioning of a BoundedBox object."""
	self.expected_x = TILE_SIZE * 3
	self.expected_y = TILE_SIZE

	self.test_box = self.create_box(self.expected_x, self.expected_y, self.expected_width, self.expected_height)

	assert_coordinates(self, 'After initialization.')
	assert_dimensions(self, 'After initialization.')

	# Change the tile's lower left coordinates
	self.expected_x = self.expected_width
	self.expected_y = self.expected_height
	self.test_box.x = self.expected_x
	self.test_box.y = self.expected_y

	assert_coordinates(self, 'Moved via x and y attributes.')

	# Change the tile's middle coordinates
	self.expected_x = self.expected_width
	self.expected_y = self.expected_height
	self.test_box.mid_x = self.expected_x + int(expected_half_width(self))
	self.test_box.mid_y = self.expected_y + int(expected_half_height(self))

	assert_coordinates(self, 'Moved via mid_x and mid_y attributes.')

	# Change the tile's upper right coordinates
	self.expected_x = self.expected_width * 2
	self.expected_y = self.expected_height * 2
	self.test_box.x2 = expected_x2(self)
	self.test_box.y2 = expected_y2(self)

	assert_coordinates(self, 'Moved via x2 and y2 attributes.')

	# Change the tile's lower left tile index
	self.expected_x = int(3.25 * TILE_SIZE)
	self.expected_y = int(4.1 * TILE_SIZE)
	self.test_box.x_tile = 3.25
	self.test_box.y_tile = 4.1

	assert_coordinates(self, 'Moved via x_tile and y_tile attributes.')

	# Change the tile's middle tile index
	self.expected_x = (int(4.1) - int(expected_half_tile_width(self))) * TILE_SIZE
	self.expected_y = (int(3.25) - int(expected_half_tile_height(self))) * TILE_SIZE
	self.test_box.mid_x_tile = 4.1
	self.test_box.mid_y_tile = 3.25

	assert_coordinates(self, 'Moved via mid_x_tile and mid_y_tile attributes.')

	# Change the tile's upper right tile index
	self.expected_x = 5 * TILE_SIZE - self.expected_width
	self.expected_y = ceil(2.5 * TILE_SIZE) - self.expected_height
	self.test_box.x2_tile = 5
	self.test_box.y2_tile = 2.5

	assert_coordinates(self, 'Moved via x2_tile and y2_tile attributes.')

	# Change the tile's lower left tile coordinates
	self.expected_x = self.expected_width * 4
	self.expected_y = self.expected_height * 5
	self.test_box.tile_x = expected_tile_x(self)
	self.test_box.tile_y = expected_tile_y(self)

	assert_coordinates(self, 'Moved via tile_x and tile_y attributes.')

	# Change the tile's upper right tile coordinates
	self.expected_x = self.expected_width * 8
	self.expected_y = self.expected_height * 2
	self.test_box.tile_x2 = expected_tile_x2(self)
	self.test_box.tile_y2 = expected_tile_y2(self)

	assert_coordinates(self, 'Moved via tile_x2 and tile_y2 attributes.')

	# Change the tile's coordinates with floats
	self.expected_x = 1.5
	self.expected_y = 15.725
	self.test_box.x = self.expected_x
	self.test_box.y = self.expected_y
	self.expected_x = int(self.expected_x)
	self.expected_y = int(self.expected_y)

	assert_coordinates(self, 'Moved via passing float to x and y attributes.')

	# Change the tile's coordinates with floats
	self.expected_x = 3.1415
	self.expected_y = 0.9999
	self.test_box.x2 = expected_x2(self)
	self.test_box.y2 = expected_y2(self)
	self.expected_x = int(self.expected_x)
	self.expected_y = int(self.expected_y)

	assert_coordinates(self, 'Moved via passing float to x2 and y2 attributes.')

	# Change the tile's coordinates with floats
	self.expected_x = 59.6
	self.expected_y = 2.171819
	self.test_box.tile_x = expected_tile_x(self)
	self.test_box.tile_y = expected_tile_y(self)
	self.expected_x = int(self.expected_x)
	self.expected_y = int(self.expected_y)

	assert_coordinates(self, 'Moved via passing float to tile_x and tile_y attributes.')

	# Change the tile's coordinates with floats
	self.expected_x = 23.375
	self.expected_y = 348.408
	self.test_box.tile_x2 = expected_tile_x2(self)
	self.test_box.tile_y2 = expected_tile_y2(self)
	self.expected_x = int(self.expected_x)
	self.expected_y = int(self.expected_y)

	assert_coordinates(self, 'Moved via passing float to tile_x2 and tile_y2 attributes.')



def run_dimension_tests(self):
	"""Tests the dimensions of a BoundedBox object."""
	self.test_box = self.create_box(self.expected_x, self.expected_y, self.expected_width, self.expected_height)

	assert_dimensions(self, 'Box was initialized.')

	# Expand the box via width and height
	self.expected_width += self.expected_width / 2
	self.expected_height += self.expected_height / 2
	self.test_box.width = self.expected_width
	self.test_box.height = self.expected_height

	# Ensure that the dimensions and any coordinates depending on the dimensions were updated
	assert_dimensions(self, 'Box was expanded via width and height attributes.')
	assert_coordinates(self, 'Box was expanded via width and height attributes.')

	# Shrink the box via tile_width and tile_height
	self.expected_width -= self.expected_width / 2
	self.expected_height -= self.expected_height / 2
	self.test_box.tile_width = self.expected_width / TILE_SIZE_FLOAT
	self.test_box.tile_height = self.expected_height / TILE_SIZE_FLOAT

	# Ensure that the dimensions and any coordinates depending on the dimensions were updated
	assert_dimensions(self, 'Box was shrunk via tile_width and tile_height attributes.')
	assert_coordinates(self, 'Box was shrunk via tile_width and tile_height attributes.')

	# Resize the box via half_width and half_height
	self.test_box.half_width = 31.5
	self.test_box.half_height = 127.25
	self.expected_width = int(31.5 * 2)
	self.expected_height = int(127.25 * 2)

	# Ensure that the dimensions and any coordinates depending on the dimensions were updated
	assert_dimensions(self, 'Box was resized via half_width and half_height attributes.')
	assert_coordinates(self, 'Box was resized via half_width and half_height attributes.')

	# Resize the box via tile_width_span and tile_height_span
	self.expected_width = int(4 * TILE_SIZE_FLOAT)
	self.expected_height = int(ceil(1.25) * TILE_SIZE_FLOAT)
	self.test_box.tile_width_span = 4
	self.test_box.tile_height_span = 1.25

	# Ensure that the dimensions and any coordinates depending on the dimensions were updated
	assert_dimensions(self, 'Box was resized via tile_width_span and tile_height_span attributes.')
	assert_coordinates(self, 'Box was resized via tile_width_span and tile_height_span attributes.')

	# Resize the box via half_tile_width and half_tile_height
	self.expected_width += self.expected_width / 1.618
	self.expected_height -= self.expected_height * 1.618
	self.test_box.half_tile_width = expected_half_tile_width(self)
	self.test_box.half_tile_height = expected_half_tile_height(self)
	self.expected_width = int(expected_half_tile_width(self)*2*TILE_SIZE)
	self.expected_height = int(expected_half_tile_height(self)*2*TILE_SIZE)

	# Ensure that the dimensions and any coordinates depending on the dimensions were updated
	assert_dimensions(self, 'Box was resized via half_tile_width and half_tile_height attributes.')
	assert_coordinates(self, 'Box was resized via half_tile_width and half_tile_height attributes.')



# Helper methods



def assert_expected_values(self, condition='box'):
	"""Asserts that the box has the expected property values."""
	for prop, value in self.expected_values.iteritems():
		actual_value = getattr(self.test_box, prop)
		self.assertEqual(actual_value, value,
			"%s of %s is %d instead of %d." % (prop, condition, actual_value, value))



def assert_coordinates(self, condition=''):
	"""Asserts that the box's coordinates are correct."""
	if condition:
		condition = ' Condition: '+condition

	# Test lower left coordinates
	self.assertEqual(self.test_box.x, self.expected_x,
		"Box has incorrect x coordinate." + condition)
	self.assertEqual(self.test_box.y, self.expected_y,
		"Box has incorrect y coordinate." + condition)

	# Test middle coordinates
	self.assertEqual(self.test_box.mid_x, expected_mid_x(self),
		"Box has incorrect mid-x coordinate." + condition)
	self.assertEqual(self.test_box.mid_y, expected_mid_y(self),
		"Box has incorrect mid-y coordinate." + condition)

	# Test upper right coordinates
	self.assertEqual(self.test_box.x2, expected_x2(self),
		"Box has incorrect x2 coordinate." + condition)
	self.assertEqual(self.test_box.y2, expected_y2(self),
		"Box has incorrect y2 coordinate." + condition)

	# Test tile of lower left coordinates
	self.assertEqual(self.test_box.x_tile, expected_x_tile(self),
		"Box has incorrect x_tile index." + condition)
	self.assertEqual(self.test_box.y_tile, expected_y_tile(self),
		"Box has incorrect y_tile index." + condition)

	# Test tile of middle coordinates
	self.assertEqual(self.test_box.mid_x_tile, expected_mid_x_tile(self),
		"Box has incorrect mid_x_tile index." + condition)
	self.assertEqual(self.test_box.mid_y_tile, expected_mid_y_tile(self),
		"Box has incorrect mid_y_tile index." + condition)

	# Test tile of upper right coordinates
	self.assertEqual(self.test_box.x2_tile, expected_x2_tile(self),
		"Box has incorrect x2_tile index." + condition)
	self.assertEqual(self.test_box.y2_tile, expected_y2_tile(self),
		"Box has incorrect y2_tile index." + condition)

	# Test lower left tile coordinates
	self.assertEqual(self.test_box.tile_x, expected_tile_x(self),
		"Box has incorrect tile x coordinate." + condition)
	self.assertEqual(self.test_box.tile_y, expected_tile_y(self),
		"Box has incorrect tile y coordinate." + condition)

	# Test upper right tile coordinates
	self.assertEqual(self.test_box.tile_x2, expected_tile_x2(self),
		"Box has incorrect tile x2 coordinate." + condition)
	self.assertEqual(self.test_box.tile_y2, expected_tile_y2(self),
		"Box has incorrect tile y2 coordinate." + condition)



def assert_dimensions(self, condition=''):
	"""Asserts that the box's dimensions are correct."""
	if condition:
		condition = ' Condition: '+condition

	# Test pixel dimensions
	self.assertEqual(self.test_box.width, self.expected_width,
		"Box has incorrect width." + condition)
	self.assertEqual(self.test_box.height, self.expected_height,
		"Box has incorrect height." + condition)

	# Test half pixel dimensions
	self.assertEqual(self.test_box.half_width, expected_half_width(self),
		"Box has incorrect half_width." + condition)
	self.assertEqual(self.test_box.half_height, expected_half_height(self),
		"Box has incorrect half_height." + condition)

	# Test tile dimensions
	self.assertEqual(self.test_box.tile_width, expected_tile_width(self),
		"Box has incorrect tile width." + condition)
	self.assertEqual(self.test_box.tile_height, expected_tile_height(self),
		"Box has incorrect tile height." + condition)

	# Test half tile dimensions
	self.assertEqual(self.test_box.half_tile_width, expected_half_tile_width(self),
		"Box has incorrect half_tile_width." + condition)
	self.assertEqual(self.test_box.half_tile_height, expected_half_tile_height(self),
		"Box has incorrect half_tile_height." + condition)

	# Test tile span dimensions
	self.assertEqual(self.test_box.tile_width_span, expected_tile_width_span(self),
		"Box has incorrect tile width span." + condition)
	self.assertEqual(self.test_box.tile_height_span, expected_tile_height_span(self),
		"Box has incorrect tile height span." + condition)



def reset_test_box(self):
	"""Resets the test box to a 32x32 pixel box at (0,0)"""
	self.test_box = self.create_box(0, 0, 32, 32)

def expected_mid_x(self):
	"""Returns mid_x for the current test coordinate values."""
	return self.expected_x + int(expected_half_width(self))

def expected_mid_y(self):
	"""Returns mid_y for the current test coordinate values."""
	return self.expected_y + int(expected_half_height(self))

def expected_x2(self):
	"""Returns x2 for the current test coordinate values."""
	return self.expected_x + self.expected_width

def expected_y2(self):
	"""Returns y2 for the current test coordinate values."""
	return self.expected_y + self.expected_height

def expected_x_tile(self):
	"""Returns x_tile for the current test coordinate values."""
	if self.expected_x < 0 and self.expected_x % TILE_SIZE != 0:
		return int(expected_tile_x(self)) - 1
	return int(expected_tile_x(self))

def expected_y_tile(self):
	"""Returns y_tile for the current test coordinate values."""
	if self.expected_y < 0 and self.expected_y % TILE_SIZE != 0:
		return int(expected_tile_y(self)) - 1
	return int(expected_tile_y(self))

def expected_mid_x_tile(self):
	"""Returns mid_x_tile for the current test coordinate values."""
	x_tile = int(expected_tile_x(self) + expected_half_tile_width(self))
	mid_x = expected_mid_x(self)
	if (mid_x > 0 and mid_x % TILE_SIZE == 0):
		x_tile -= 1
	elif (mid_x < 0 and mid_x % TILE_SIZE != 0):
		x_tile -= 1

	return x_tile

def expected_mid_y_tile(self):
	"""Returns mid_y_tile for the current test coordinate values."""
	y_tile = int(expected_tile_y(self) + expected_half_tile_height(self))
	mid_y = expected_mid_y(self)
	if (mid_y > 0 and mid_y % TILE_SIZE == 0):
		y_tile -= 1
	elif (mid_y < 0 and mid_y % TILE_SIZE != 0):
		y_tile -= 1

	return y_tile

def expected_x2_tile(self):
	"""Returns x2_tile for the current test coordinate values."""
	x2_tile = int(expected_tile_x2(self))
	x2 = expected_x2(self)
	if (x2 > 0 and x2 % TILE_SIZE == 0):
		x2_tile -= 1
	elif (x2 < 0):
		x2_tile -= 1

	return x2_tile

def expected_y2_tile(self):
	"""Returns y2_tile for the current test coordinate values."""
	y2_tile = int(expected_tile_y2(self))
	y2 = expected_y2(self)
	if (y2 > 0 and y2 % TILE_SIZE == 0):
		y2_tile -= 1
	elif (y2 < 0):
		y2_tile -= 1

	return y2_tile

def expected_tile_x(self):
	"""Returns tile_x for the current test coordinate values."""
	return self.expected_x / TILE_SIZE_FLOAT

def expected_tile_y(self):
	"""Returns tile_y for the current test coordinate values."""
	return self.expected_y / TILE_SIZE_FLOAT

def expected_tile_x2(self):
	"""Returns tile_x2 for the current test coordinate values."""
	return expected_x2(self) / TILE_SIZE_FLOAT

def expected_tile_y2(self):
	"""Returns tile_y2 for the current test coordinate values."""
	return expected_y2(self) / TILE_SIZE_FLOAT

def expected_half_width(self):
	"""Returns half_width for the current test coordinate values."""
	return self.expected_width / 2.0

def expected_half_height(self):
	"""Returns half_height for the current test coordinate values."""
	return self.expected_height / 2.0

def expected_tile_width(self):
	"""Returns tile_width for the current test coordinate values."""
	return self.expected_width / TILE_SIZE_FLOAT

def expected_tile_height(self):
	"""Returns tile_height for the current test coordinate values."""
	return self.expected_height / TILE_SIZE_FLOAT

def expected_half_tile_width(self):
	"""Returns half_tile_width for the current test coordinate values."""
	return expected_tile_width(self) / 2.0

def expected_half_tile_height(self):
	"""Returns half_tile_height for the current test coordinate values."""
	return expected_tile_height(self) / 2.0

def expected_tile_width_span(self):
	"""Returns tile_width_span for the current test coordinate values."""
	return ceil(expected_tile_width(self))

def expected_tile_height_span(self):
	"""Returns tile_height_span for the current test coordinate values."""
	return ceil(expected_tile_height(self))
