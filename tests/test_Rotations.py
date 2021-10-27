from unittest import TestCase

import numpy as np
from binq.src.QC.Rotations import R, Rz


#TODO GETTERS TO FINISH


class Testcustom_Unitary(TestCase):

    def test_cost(self):
        self.fail()


class TestR(TestCase):
    def setUp(self) -> None:
        self.R1 = R( np.pi / 36, 0, 1, 2, 3)
        self.R2 = R( np.pi / 12, 0, 1, 2, 3)
        self.R3 = R( np.pi / 4, 0, 1,  2, 3)


    def test_theta_corrector(self):
        self.assertAlmostEqual(self.R1.theta, 6.367, places=2)
        self.assertAlmostEqual(self.R2.theta, 6.541, places=2)
        self.assertAlmostEqual(self.R3.theta, 0.785, places=2)


    def test_dag(self):
        self.fail()

    def test_cost(self):
        self.fail()




class TestRz(TestCase):
    def setUp(self) -> None:
        self.R1 = Rz( np.pi / 36, 0, 3)
        self.R2 = Rz( np.pi / 12, 0, 3)
        self.R3 = Rz( np.pi / 4, 0, 3)

    def test_theta_corrector(self):
        self.assertAlmostEqual(self.R1.theta, 6.367, places=2)
        self.assertAlmostEqual(self.R2.theta, 6.541, places=2)
        self.assertAlmostEqual(self.R3.theta, 0.785, places=2)

    def test_dag(self):
        self.fail()

    def test_cost(self):
        self.fail()


class TestPI_PULSE(TestCase):
    pass
