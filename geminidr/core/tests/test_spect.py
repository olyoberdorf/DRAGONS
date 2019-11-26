#!/usr/bin/env python
"""
Tests applied to primitives_spect.py

Notes
-----

    For extraction tests, your input wants to be a 2D image with an `APERTURE`
    table attached. You'll see what happens if you take a spectrophotometric
    standard and run it through the standard reduction recipe, but the
    `APERTURE` table has one row per aperture with the following columns:

    - number : sequential list of aperture number

    - ndim, degree, domain_start, domain_end, c0, [c1, c2, c3...] : standard
    Chebyshev1D definition of the aperture centre (in pixels) as a function of
    pixel in the dispersion direction

    - aper_lower : location of bottom of aperture relative to centre (always
    negative)

    - aper_upper : location of top of aperture relative to centre (always
    positive)

    The ndim column will always be 1 since it's always 1D Chebyshev, but the
    `model_to_dict()` and `dict_to_model()` functions that convert the Model
    instance to a dict create/require this.
"""
import numpy as np
import pytest
from astropy import table
from astropy.io import fits
from astropy.modeling import models
from copy import deepcopy
from scipy import optimize

from geminidr.core import primitives_spect

astrofaker = pytest.importorskip("astrofaker")


class SkyLines:
    """
    Helper class to simulate random sky lines for tests. Use `np.random.seed()`
    to have the same lines between calls.

    Parameters
    ----------
    n_lines : int
        Number of lines to be included.
    max_position : int
        Maximum position value.
    max_value : float
        Maximum float value.

    """

    def __init__(self, n_lines, max_position, max_value):
        self.positions = np.random.randint(low=0, high=max_position, size=n_lines)
        self.intensities = np.random.random(size=n_lines) * max_value

    def __call__(self, data, axis=0):
        """
        Generates a sky frame filled with zeros and with the random sky lines.

        Parameters
        ----------
        data : ndarray
            2D ndarray representing the detector.
        axis : {0, 1}
            Dispersion axis: 0 for rows or 1 for columns.

        Returns
        -------
        numpy.ndarray
            2D array matching input shape filled with zeros and the random sky
            lines.
        """
        sky_data = np.zeros_like(data)
        if axis == 0:
            sky_data[self.positions] = self.intensities
        elif axis == 1:
            sky_data[:, self.positions] = self.intensities
        else:
            raise ValueError(
                "Wrong value for dispersion axis. "
                "Expected 0 or 1, found {:d}".format(axis))

        return sky_data


def create_zero_filled_fake_astrodata(width, height):
    """
    Helper function to generate a fake astrodata object filled with zeros.

    Parameters
    ----------
    width : int
        Number of columns.
    height : int
        Number of rows.

    Returns
    -------
    astrodata
        Single-extension zero filled object.
    """
    data = np.zeros((height, width))

    hdu = fits.ImageHDU()
    hdu.header['CCDSUM'] = "1 1"
    hdu.data = data

    ad = astrofaker.create('GMOS-S')
    ad.add_extension(hdu, pixel_scale=1.0)

    return ad


# noinspection PyPep8Naming
def test_QESpline_optimization():
    """
    Test the optimization of the QESpline. This defines 3 regions, each of a
    different constant value, with gaps between them. The spline optimization
    should determine the relative offsets.
    """
    from geminidr.core.primitives_spect import QESpline

    gap = 20
    data_length = 300
    real_coeffs = [0.5, 1.2]

    # noinspection PyTypeChecker
    data = np.array([1] * data_length +
                    [0] * gap +
                    [real_coeffs[0]] * data_length +
                    [0] * gap +
                    [real_coeffs[1]] * data_length)

    masked_data = np.ma.masked_where(data == 0, data)
    xpix = np.arange(len(data))
    weights = np.where(data > 0, 1., 0.)
    boundaries = (data_length, 2 * data_length + gap)

    coeffs = np.ones((2,))
    order = 10

    result = optimize.minimize(
        QESpline, coeffs,
        args=(xpix, masked_data, weights, boundaries, order),
        tol=1e-7,
        method='Nelder-Mead'
    )

    np.testing.assert_allclose(real_coeffs, 1. / result.x, atol=0.01)


@pytest.fixture(scope="module")
def fake_data():
    data = np.zeros((100, 200))
    data[50] = 10.

    hdu = fits.ImageHDU()
    hdu.header['CCDSUM'] = "1 1"
    hdu.data = data

    aperture = table.Table(
        [[1],  # Number
         [1],  # ndim
         [0],  # degree
         [0],  # domain_start
         [data.shape[1] - 1],  # domain_end
         [50],  # c0
         [-3],  # aper_lower
         [3],  # aper_upper
         ],
        names=[
            'number',
            'ndim',
            'degree',
            'domain_start',
            'domain_end',
            'c0',
            'aper_lower',
            'aper_upper'],
    )

    ad = astrofaker.create('GMOS-S')
    ad.add_extension(hdu, pixel_scale=1.0)
    ad[0].APERTURE = aperture

    return ad


@pytest.mark.xfail(reason="The fake data needs a DQ plane")
def test_find_apertures(fake_data):
    _p = primitives_spect.Spect([])
    _p.findSourceApertures(fake_data)


def test_trace_apertures():
    # Config ---
    width = 400
    height = 200
    trace_model_parameters = {'c0': height // 2, 'c1': 5.0, 'c2': -0.5, 'c3': 0.5}

    # Generate fake point source ---
    trace_model = models.Chebyshev1D(4, domain=[0, width - 1], **trace_model_parameters)

    rows = np.arange(height)
    cols = np.arange(width)

    gaussian_model = models.Gaussian1D(stddev=5, amplitude=1)

    data = np.zeros((height, width))

    def gaussian(index):
        gaussian_model.mean = trace_model(index)
        return gaussian_model(rows)

    for col in cols:
        data[:, col] = gaussian(col)

    # Convert to astrodata ---
    hdu = fits.ImageHDU()
    hdu.header['CCDSUM'] = "1 1"
    hdu.data = data

    aperture = table.Table([[1],  # Number
                            [1],  # ndim
                            [2],  # degree
                            [0],  # domain_start
                            [data.shape[1] - 1],  # domain_end
                            [data.shape[0] // 2],  # c0
                            [-10],  # aper_lower
                            [10],  # aper_upper
                            ],
                           names=[
                               'number',
                               'ndim',
                               'degree',
                               'domain_start',
                               'domain_end',
                               'c0',
                               'aper_lower',
                               'aper_upper'],
                           )

    ad = astrofaker.create('GMOS-S')
    ad.add_extension(hdu, pixel_scale=1.0)
    ad[0].APERTURE = aperture

    _p = primitives_spect.Spect([])
    ad_out = _p.traceApertures(ad, trace_order=4)

    keys = ['c0', 'c1', 'c2', 'c3']
    for ext in ad_out:
        desired = np.array([trace_model_parameters[k] for k in keys])
        actual = np.array([ext.APERTURE[0][k] for k in keys])
        np.testing.assert_allclose(desired, actual, atol=0.05)


def test_sky_correct_from_slit():

    # Input Parameters ----------------
    width = 200
    height = 100

    source_intensity = 1.
    source_position = height // 2
    source_fwhm = 5

    n_sky_lines = 500
    max_sky_intensity = 0.5

    # Simulate Data -------------------
    np.random.seed(0)

    gaussian = models.Gaussian1D(mean=source_position,
                                 stddev=source_fwhm / (2 * np.sqrt(2 * np.log(2))),
                                 amplitude=source_intensity)

    source = gaussian(np.arange(height))[:, np.newaxis].repeat(width, axis=1)
    sky = SkyLines(n_sky_lines, width - 1, max_sky_intensity)

    ad = create_zero_filled_fake_astrodata(width, height)
    ad[0].data += source
    ad[0].data += sky(ad[0].data, axis=1)

    # Running the test ----------------
    _p = primitives_spect.Spect([])

    # ToDo @csimpson: Is it modifying the input ad?
    ad_out = _p.skyCorrectFromSlit(deepcopy(ad))

    np.testing.assert_allclose(ad_out[0].data, source, atol=1e-3)


# def test_extract_1d_spectra():
#
#     width = 200
#     height = 100
#
#     ad = create_zero_filled_fake_astrodata(width, height)
#     ad[0].data[height//2, :] = 1.
#
#     _p = primitives_spect.Spect([])
#
#     # todo: if input is a single astrodata,
#     #  should not the output have the same format?
#     ad_out = _p.extract1DSpectra(adinputs=[ad])
#
#     print(ad_out.info())
#
#     # np.testing.assert_equal(ad_out[0].shape[0], ad[0].data.shape[1])
#     # np.testing.assert_equal(ad_out[0].data, fake_data[0].data[50])


if __name__ == '__main__':
    pytest.main()
