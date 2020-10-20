import unittest

import utils 

class UtilsTestCase(unittest.TestCase):
    def test_shifting(self):
        self.assertEqual(65, utils.shifting(65, 0))
        self.assertEqual(65, utils.shifting(90, 1))
        self.assertEqual(90, utils.shifting(65, -1))
        self.assertEqual(98, utils.shifting(122, 2, 97, 122))
        self.assertEqual(121, utils.shifting(97, -2, 97, 122))
        self.assertEqual(110, utils.shifting(110, 0, 97, 122))
