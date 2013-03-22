import unittest

import xraylib
from xraylib import strtoz


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_strtoz(self):
        self.assertEqual(strtoz('H'),{ ('H',1):1, })
        self.assertEqual(strtoz('O2'), { ('O',8): 2, })
        self.assertEqual(strtoz('(H)'), { ('H',1):1, })
        self.assertEqual(strtoz('(H)2'), { ('H',1):2, })
        self.assertEqual(strtoz('(H)()'), { ('H',1):1, })
        self.assertEqual(strtoz('Air'), { ('N',7) : 4, ('O',8) : 1 })

if __name__ == '__main__':
    unittest.main()
