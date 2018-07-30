import unittest
from learn.mathfunc import *


class TestMathFunc(unittest.TestCase):

    def setUp(self):
        print("do something before test.Prepare environment")

    def tearDown(self):
        print('do something after test.Clean up')

    def test_add(self):
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """
        test_divide
        *
        :return:
        """
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """
        test_divide
        /
        :return:
        """
        self.assertEqual(3, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
