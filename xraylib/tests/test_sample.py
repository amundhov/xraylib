import unittest
import numpy as np

from common import TestQuantity
from xraylib import sample

class TestSample(TestQuantity):
    _beam_energy = [0.8147, 9.058, 12.70, 913.4, 6324]

    def setUp(self):
        # Example samples. 1cm thick.
        self.water_sample  = sample.Sample(1, 0.999868, 'H2O', 0)
        self.copper_sample = sample.Sample(1, 8.96, 'Cu', 0)

    def test_mass_attenuation(self):
        _water_answers  = [6859.45741370395, 6.85322015083691, 2.51936905909002, 0.0779216270581452, 0.0792534149608234]
        _copper_answers = [4.26264362106791, 282.584914534112, 117.097939659441, 0.0609414173611879, 0.0209530752156647]
        self.assertAlmostEqualArray(
            _water_answers,
            self.water_sample.mass_attenuation(self._beam_energy)
        )
        self.assertAlmostEqualArray(
            _copper_answers,
            self.copper_sample.mass_attenuation(self._beam_energy)
        )



if __name__ == '__main__':
    unittest.main()
