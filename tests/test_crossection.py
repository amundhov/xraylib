import unittest
import numpy as np

from common import TestQuantity
from xraylib import crossection

class TestCrossSection(TestQuantity):
    _atomic_numbers = [1, 8, 29]
    _beam_energy = [0.8147, 9.058, 12.70, 913.4, 6324]
    _two_theta = [0,25,50,75,170]


    def setUp(self):
        pass

    def test_get_cross_section(self):
        _answers =  [[ 24.119999072747  , 0.648409153300992 , 0.662589775575706 , 0.233702026296182 , 0.212014021542921 ], \
                     [ 205161.127778596 , 203.725953841301  , 74.0449409454463  , 1.8637202419898   , 1.94693837559426 ], \
                     [ 449.754260316238 , 29815.7154364634  , 12355.0786595886  , 6.4299680021192   , 2.21077239448201 ] ]
        for i in xrange(0,len(self._atomic_numbers)):
            self.assertAlmostEqualArray(
                    _answers[i],
                    crossection.get_cross_section(self._beam_energy,self._atomic_numbers[i])[0,:]
            )

    def test_klein_nishina(self):
        _answers = [[0.0794078763692949, 0.143187420478865,  0.288771922524017,  0.411832551154411,   0.089615194454024],
                    [0.0794078763692949, 0.142755740108656,  0.285475810005038,  0.402175973694339,   0.0842012324316349],
                    [0.0794078763692949, 0.142565696861413,  0.284038309747185,  0.398020846452724,   0.081986778429254],
                    [0.0794078763692949, 0.10578487605983,   0.111363835093867,  0.0819222447961106,  0.00967343980724931],
                    [0.0794078763692949, 0.0360135742945785, 0.0147097669843463, 0.00716247320814965, 0.0015720142476563] ]
        for i in xrange(0,len(self._two_theta)):
            # test array input of scattering angles
            self.assertAlmostEqualArray(
                _answers[i],
                crossection.klein_nishina(self._beam_energy[i], self._two_theta, 10)[0]
            )
            # test array input of beam energies
            self.assertAlmostEqualArray(
                # "transpose" answers
                np.array(_answers).T.tolist()[i],
                crossection.klein_nishina(self._beam_energy, self._two_theta[i], 10)[0]
            )

    def test_thomson(self):
        _answers = [0.079407876369295, 0.143230200356376, 0.289100922504049, 0.412806384142071, 0.090182858423070]
        self.assertAlmostEqualArray(
            _answers,
            crossection.thomson(self._two_theta, 10)
        )

if __name__ == '__main__':
    unittest.main()
