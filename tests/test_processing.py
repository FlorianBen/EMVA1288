from emva1288.common import processing as proc

import numpy as np
import pytest

class TestProcessing:
    def test_mean_grey_value(self):
        image1 = np.array([[2, 2, 2], [4, 4, 4], [8, 8, 8]])
        image2 = np.array([[1, 1, 1], [3, 3, 3], [5, 5, 5]])
        images = np.stack((image1, image2))
        mgvf = proc.mean_grey_value(images)
        assert 69/18 == pytest.approx(mgvf, 1e-6)

    def test_mean_grey_value(self):
        image1 = np.array([[2, 2, 2], [4, 4, 4], [8, 8, 8]])
        image2 = np.array([[1, 1, 1], [3, 3, 3], [5, 5, 5]])
        valtest = np.sum(np.array([[1, 1, 1], [1, 1, 1], [3, 3, 3]])**2 - 25/18)/18
        images = np.stack((image1, image2))
        vgvf = proc.var_grey_value(images)
        assert valtest == pytest.approx(vgvf, 1e-6)

    def test_snr(self):
        pass