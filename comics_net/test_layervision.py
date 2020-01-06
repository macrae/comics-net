import numpy as np
import torch
from torch import tensor

import comics_net.layervision as layervision


def test_init_pixel_buf():
    actual = layervision.init_pixel_buf(size=3, seed=42)

    expected = np.array(
        [
            [
                [
                    [0.5009, 0.4993, 0.4997],
                    [0.4998, 0.4994, 0.5001],
                    [0.5025, 0.5044, 0.4990],
                ],
                [
                    [0.5005, 0.5023, 0.4996],
                    [0.5041, 0.5045, 0.4992],
                    [0.4962, 0.4993, 0.5013],
                ],
                [
                    [0.5039, 0.4965, 0.4999],
                    [0.5012, 0.5006, 0.4935],
                    [0.4992, 0.4978, 0.4968],
                ],
            ]
        ]
    )

    expected = torch.from_numpy(expected).float()
    torch.testing.assert_allclose(actual, expected, rtol=0.01, atol=0.01)


def test_init_fft_buf():
    actual = layervision.init_fft_buf(size=3, sd=0.01, seed=42)

    expected = np.array(
        [
            [
                [
                    [[0.0050, -0.0014], [0.0065, 0.0152]],
                    [[-0.0023, -0.0023], [0.0158, 0.0077]],
                    [[-0.0047, 0.0054], [-0.0046, -0.0047]],
                ],
                [
                    [[0.0024, -0.0191], [-0.0172, -0.0056]],
                    [[-0.0101, 0.0031], [-0.0091, -0.0141]],
                    [[0.0147, -0.0023], [0.0007, -0.0142]],
                ],
                [
                    [[-0.0054, 0.0011], [-0.0115, 0.0038]],
                    [[-0.0060, -0.0029], [-0.0060, 0.0185]],
                    [[-0.0001, -0.0106], [0.0082, -0.0122]],
                ],
            ]
        ]
    )

    expected = torch.from_numpy(expected).float()
    torch.testing.assert_allclose(actual, expected, rtol=0.01, atol=0.01)


def test_fft_to_rgb():
    t = layervision.init_fft_buf(size=3, sd=0.01, seed=42)
    actual = layervision.fft_to_rgb(t, d=0.5, decay_power=1, seed=42)

    expected = np.array(
        [
            [
                [
                    [0.0042, -0.0049, 0.0026],
                    [0.0008, -0.0031, 0.0084],
                    [0.0035, -0.0006, 0.0001],
                ],
                [
                    [-0.0077, 0.0065, -0.0046],
                    [-0.0024, 0.0033, 0.0026],
                    [-0.0010, 0.0021, 0.0066],
                ],
                [
                    [-0.0053, -0.0034, 0.0002],
                    [-0.0078, 0.0055, 0.0024],
                    [0.0004, -0.0043, 0.0002],
                ],
            ]
        ]
    )

    expected = torch.from_numpy(expected).float()
    torch.testing.assert_allclose(actual, expected, rtol=0.01, atol=0.01)


def test_lucid_to_rgb():
    fft = layervision.init_fft_buf(size=3, sd=0.01, seed=42)
    rgb = layervision.fft_to_rgb(fft, d=0.5, decay_power=1, seed=42)
    actual = layervision.lucid_to_rgb(t=rgb, seed=42)

    expected = np.array(
        [
            [
                [
                    [6.5426e-04, -1.6316e-03, 5.8751e-04],
                    [-3.6030e-04, -8.6372e-04, 5.3695e-03],
                    [1.8194e-03, -1.1289e-04, 1.3584e-03],
                ],
                [
                    [3.0619e-03, -2.4953e-03, 1.5138e-03],
                    [1.2992e-03, -2.4072e-03, 4.6805e-03],
                    [2.0317e-03, 1.1727e-04, 5.5938e-05],
                ],
                [
                    [3.6406e-03, -4.3567e-03, 2.4358e-03],
                    [4.2316e-04, -2.1077e-03, 4.5723e-03],
                    [2.2940e-03, -1.0283e-03, -1.1971e-03],
                ],
            ]
        ]
    )

    expected = torch.from_numpy(expected).float()
    torch.testing.assert_allclose(actual, expected, rtol=0.01, atol=0.01)


def test_image_buf_to_rgb():
    size = 3
    jitter = 10
    fft = True
    img_buf = (
        layervision.init_fft_buf(size + jitter)
        if fft
        else layervision.init_pixel_buf(size + jitter)
    )

    actual = layervision.image_buf_to_rgb(
        img_buf, jitter=10, decorrelate=True, fft=True, decay_power=1, seed=42
    )

    expected = np.array(
        [
            [
                [0.4996, 0.5001, 0.5007],
                [0.4979, 0.4991, 0.4994],
                [0.4997, 0.4999, 0.4998],
            ],
            [
                [0.4994, 0.5000, 0.5008],
                [0.4980, 0.4989, 0.4998],
                [0.4998, 0.4996, 0.5002],
            ],
            [
                [0.4996, 0.4999, 0.5005],
                [0.4981, 0.4987, 0.4997],
                [0.4994, 0.4993, 0.5000],
            ],
        ]
    )

    expected = torch.from_numpy(expected).float()
    torch.testing.assert_allclose(actual, expected, rtol=0.01, atol=0.01)
