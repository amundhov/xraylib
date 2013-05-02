import unittest

import xraylib
from xraylib import common


class TestCommon(unittest.TestCase):
    def setUp(self):
        pass

    def test_strtoz(self):
        self.assertEqual(common.strtoz('H'),{ ('H',1):1, })
        self.assertEqual(common.strtoz('O2'), { ('O',8): 2, })
        self.assertEqual(common.strtoz('(H)'), { ('H',1):1, })
        self.assertEqual(common.strtoz('(H)2'), { ('H',1):2, })
        self.assertEqual(common.strtoz('(H)()'), { ('H',1):1, })
        self.assertEqual(common.strtoz('Air'), { ('N',7) : 4, ('O',8) : 1 })

if __name__ == '__main__':
    unittest.main()
