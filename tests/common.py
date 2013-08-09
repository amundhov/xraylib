import unittest

class TestQuantity(unittest.TestCase):

    def assertAlmostEqualArray(self, expected_vector, test_vector, tolerance=0.00001):
        def _compare(a,b):
            return abs(a-b) <= tolerance*abs(a) and abs(a-b) <= tolerance*abs(b)
        _ = map(lambda a,b: self.assertTrue(_compare(a,b),msg='Expected: %f, got %f' % (a,b)),
                list(expected_vector),
                list(test_vector))
