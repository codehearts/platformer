import unittest
from game import util

class TestUtilities(unittest.TestCase):

    # Tests list equalization
    def test_list_equalizer(self):
        self.assertEqual([1,2,1,2,1], util.equalize_list_sizes(range(5), [1,2]), 'List equalization failed')
        self.assertEqual([1,2,1,2], util.equalize_list_sizes(range(4), [1,2]), 'List equalization failed')
        self.assertEqual([1,1,1,1], util.equalize_list_sizes(range(4), [1]), 'List equalization failed')
        self.assertEqual([1,2,3,4], util.equalize_list_sizes(range(4), [1,2,3,4]), 'List equalization failed')
        self.assertEqual([1,2,3,4,1,2,3,4], util.equalize_list_sizes(range(8), [1,2,3,4]), 'List equalization failed')
        self.assertEqual([1,2,3,4,1,2,3], util.equalize_list_sizes(range(7), [1,2,3,4]), 'List equalization failed')
