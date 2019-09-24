#!/usr/bin/env python
import os

import numpy as np
import pytest
from astropy.io.fits import ImageHDU
from astropy.nddata import NDData
from astropy.table import Table

import astrodata


def test_can_read_data(path_to_inputs):
    test_filename = "GMOS/N20110826S0336.fits"
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))
    assert len(ad) == 3


def test_append_array_to_root_no_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    ad.append(ones)
    assert len(ad) == (lbefore + 1)
    assert ad[-1].data is ones
    assert ad[-1].hdr['EXTNAME'] == 'SCI'
    assert ad[-1].hdr['EXTVER'] == len(ad)


def test_append_array_to_root_with_name_sci(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    ad.append(ones, name='SCI')
    assert len(ad) == (lbefore + 1)
    assert ad[-1].data is ones
    assert ad[-1].hdr['EXTNAME'] == 'SCI'
    assert ad[-1].hdr['EXTVER'] == len(ad)


def test_append_array_to_root_with_arbitrary_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    with pytest.raises(ValueError) as excinfo:
        ad.append(ones, name='ARBITRARY')


def test_append_array_to_extension_with_name_sci(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    with pytest.raises(ValueError) as excinfo:
        ad[0].append(ones, name='SCI')


def test_append_array_to_extension_with_arbitrary_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    ad[0].append(ones, name='ARBITRARY')

    assert len(ad) == lbefore
    assert ad[0].ARBITRARY is ones


def test_append_nddata_to_root_no_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    hdu = ImageHDU(ones)
    nd = NDData(hdu.data)
    nd.meta['header'] = hdu.header
    ad.append(nd)
    assert len(ad) == (lbefore + 1)


def test_append_nddata_to_root_with_arbitrary_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    ones = np.ones((100, 100))
    hdu = ImageHDU(ones)
    nd = NDData(hdu.data)
    nd.meta['header'] = hdu.header
    hdu.header['EXTNAME'] = 'ARBITRARY'
    with pytest.raises(ValueError) as excinfo:
        ad.append(nd)


def test_append_table_to_root(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    table = Table(([1, 2, 3], [4, 5, 6], [7, 8, 9]),
                  names=('a', 'b', 'c'))
    ad.append(table, 'MYTABLE')
    assert (ad.MYTABLE == table).all()


@pytest.mark.skip("unknown expected behaviour")
def test_append_table_to_root_without_name(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    table = Table(([1, 2, 3], [4, 5, 6], [7, 8, 9]),
                  names=('a', 'b', 'c'))

    with pytest.raises(ValueError) as excinfo:
        ad.append(table)


def test_append_table_to_extension(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    lbefore = len(ad)
    table = Table(([1, 2, 3], [4, 5, 6], [7, 8, 9]),
                  names=('a', 'b', 'c'))
    ad[0].append(table, 'MYTABLE')
    assert (ad[0].MYTABLE == table).all()


# Append / assign Gemini specific

def test_append_dq_to_root(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    dq = np.zeros(ad[0].data.shape)
    with pytest.raises(ValueError):
        ad.append(dq, 'DQ')


def test_append_dq_to_ext(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    dq = np.zeros(ad[0].data.shape)
    ad[0].append(dq, 'DQ')
    assert dq is ad[0].mask


def test_append_var_to_root(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    var = np.random.random(ad[0].data.shape)
    with pytest.raises(ValueError):
        ad.append(var, 'VAR')


def test_append_var_to_ext(path_to_inputs):
    test_filename = 'GMOS/N20160524S0119.fits'
    ad = astrodata.open(os.path.join(path_to_inputs, test_filename))

    var = np.random.random(ad[0].data.shape)
    ad[0].append(var, 'VAR')
    assert np.abs(var - ad[0].variance).mean() < 0.00000001


# Append AstroData slices

def test_append_single_slice(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))
    ad2 = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20110826S0336.fits'))

    lbefore = len(ad2)
    last_ever = ad2[-1].nddata.meta['header'].get('EXTVER', -1)
    ad2.append(ad[1])

    assert len(ad2) == (lbefore + 1)
    assert np.all(ad2[-1].data == ad[1].data)
    assert last_ever < ad2[-1].nddata.meta['header'].get('EXTVER', -1)


def test_append_non_single_slice(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))
    ad2 = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20110826S0336.fits'))

    with pytest.raises(ValueError):
        ad2.append(ad[1:])


def test_append_whole_instance(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))
    ad2 = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20110826S0336.fits'))

    with pytest.raises(ValueError):
        ad2.append(ad)


def test_append_slice_to_extension(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))
    ad2 = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20110826S0336.fits'))

    with pytest.raises(ValueError):
        ad2[0].append(ad[0], name="FOOBAR")


# Deletion
@pytest.mark.xfail(reason="file not available")
def test_delete_named_attribute_at_top_level(path_to_inputs):
    ad = from_test_data('NIRI/N20131215S0202_refcatAdded.fits')
    assert 'REFCAT' in ad.tables
    del ad.REFCAT
    assert 'REFCAT' not in ad.tables


def test_delete_named_associated_extension(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))
    table = Table(([1, 2, 3], [4, 5, 6], [7, 8, 9]),
                  names=('a', 'b', 'c'))
    ad[0].append(table, 'MYTABLE')
    assert 'MYTABLE' in ad[0]
    del ad[0].MYTABLE
    assert 'MYTABLE' not in ad[0]


def test_delete_arbitrary_attribute_from_ad(path_to_inputs):
    ad = astrodata.open(os.path.join(path_to_inputs, 'GMOS/N20160524S0119.fits'))

    with pytest.raises(AttributeError):
        ad.arbitrary

    ad.arbitrary = 15

    assert ad.arbitrary == 15

    del ad.arbitrary

    with pytest.raises(AttributeError):
        ad.arbitrary