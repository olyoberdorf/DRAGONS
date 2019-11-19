#!/usr/bin/env python

# ToDo: Clean up files if tests pass
# ToDo: Make Incremental work

import glob
import os

import pytest

from astrodata import testing
from gempy.adlibrary import dataselect
from gempy.utils import logutils
from recipe_system.reduction.coreReduce import Reduce
from recipe_system.utils.reduce_utils import normalize_ucals

test_case = [

    # GMOS-N HAM 2x2 Science ----------------
    ('GMOS/GN-2017B-LP-15', '2x2', None,
     [
         'N20170912S0295.fits',
         'N20170912S0296.fits',
         'N20170912S0297.fits',
         'N20170912S0298.fits',
         'N20170912S0299.fits',
         'N20170913S0153.fits',
         'N20170913S0154.fits',
         'N20170913S0155.fits',
         'N20170913S0156.fits',
         'N20170913S0157.fits',
         'N20170913S0158.fits',
         'N20170914S0481.fits',
         'N20170914S0482.fits',
         'N20170914S0483.fits',
         'N20170914S0484.fits',
         'N20170914S0485.fits',
         'N20170915S0274.fits',
         'N20170915S0275.fits',
         'N20170915S0276.fits',
         'N20170915S0277.fits',
         'N20170915S0278.fits',
         'N20170915S0279.fits',
         'N20170915S0280.fits',
         'N20170915S0281.fits',
         'N20170915S0282.fits',
         'N20170915S0283.fits',
         'N20170915S0284.fits',
         'N20170915S0285.fits',
         'N20170915S0286.fits',
         'N20170915S0287.fits',
         'N20170915S0337.fits',
         'N20170915S0338.fits',
         'N20170915S0339.fits',
         'N20170915S0340.fits',
         'N20170915S0341.fits']),

    # GMOS-N EEV 2x2 Science ----------------
    ('GMOS/GN-2002A-Q-89', '2x2', None,
     [
         'N20020214S059.fits',
         'N20020214S060.fits',
         'N20020214S061.fits',
         # 'N20020214S062.fits',  # Why am I commented?
         # 'N20020214S063.fits',  # Why am I commented?
         # 'N20020214S064.fits',  # Why am I commented?
         'N20020214S022.fits',
         'N20020214S023.fits',
         'N20020214S024.fits',
         # 'N20020214S025.fits',  # Why am I commented?
         # 'N20020214S026.fits',  # Why am I commented?
         'N20020211S156.fits',
         'N20020211S157.fits',
         'N20020211S158.fits',
         # 'N20020211S159.fits',  # Why am I commented?
         # 'N20020211S160.fits',  # Why am I commented?
     ]),

    # GMOS-S HAM 1x1 i-band Science
    ("GMOS/GS-2017B-Q-6", "1x1", [
        ('stackFrames:memory', 1),
        # ('addDQ:user_bpm', 'fixed_bpm_1x1_FullFrame.fits'),
        ('adjustWCSToReference:rotate', True),
        ('adjustWCSToReference:scale', True),
        ('resampleToCommonFrame:interpolator', 'spline3')],
     [
         'S20171205S0062.fits',
         'S20171205S0063.fits',
         'S20171205S0064.fits',
         'S20171205S0065.fits',
         'S20171205S0066.fits',
         'S20171205S0067.fits',
         'S20171205S0068.fits',
         'S20171205S0069.fits',
         'S20171205S0070.fits',
         'S20171205S0071.fits',
         # --- 15 files currently use too much memory ---
         # 'S20171205S0072.fits',
         # 'S20171205S0073.fits',
         # 'S20171205S0074.fits',
         # 'S20171205S0075.fits',
         # 'S20171205S0076.fits',
         # ---
         'S20171204S0022.fits',
         'S20171204S0023.fits',
         'S20171204S0024.fits',
         'S20171204S0025.fits',
         'S20171204S0026.fits',
         'S20171206S0128.fits',
         'S20171206S0129.fits',
         'S20171206S0130.fits',
         'S20171206S0131.fits',
         'S20171206S0132.fits',
         'S20171206S0120.fits',
         'S20171206S0121.fits',
         'S20171206S0124.fits',
         'S20171206S0125.fits',
         'S20171206S0126.fits',
         'S20171206S0127.fits',
     ]),

]


@pytest.fixture(scope="session")
def output_dir(tmp_path_factory):
    """
    Temporary output directory factory that relies on PyTest's build-in
    session-scoped `tmp_path_factory` fixture.

    Parameters
    ----------
    tmp_path_factory : fixture
        PyTest's built-in session-scoped fixture that creates a temporary
        directory in the system's temp folder. This can be set by adding
        `--basetemp=mydir` when calling via command line.

    Returns
    -------
    callable
        This is a function that creates a sub-directory inside the temporary
        path and changes the current working directory to it so reduced data is
        stored there.
    """
    tmp_path = tmp_path_factory.mktemp('dragons-tests')

    def _output_dir(path):
        _dir = tmp_path / path
        _dir.mkdir(parents=True, exist_ok=True)
        os.chdir(_dir)
        return _dir

    return _output_dir


def setup_log(path):
    """
    Setup log file to run in quiet mode.

    Parameters
    ----------
    path : fixture
        PyTest's build-in fixture used to create a temporary directory.
    """
    log_file = os.path.basename(__file__).replace('.py', '.log')
    log_file = path / log_file

    print("Setting up log file: {}".format(log_file))
    logutils.config(mode='standard', file_name=log_file)


def _reduce(list_of_files, binning, tags=None, xtags=None, expression='True',
            calib_files=None, recipe_name='_default', user_parameters=None):
    """
    Helper function to minimize repeated steps.

    Parameters
    ----------
    list_of_files : list
        Input files
    binning : str
        A "{}x{}" formatted string where the first field is the binning in X and
        the second is the binning in Y.
    tags : {None, list}
        Tags that would be used to include files from the selected file list.
    xtags : {None, list}
        Tags that would be used to remove files from the selected file list.
    expression : str
        Boolean expression to select data based on descriptors.
    calib_files : {None, list}
        List of calibrations files with their proper prefix added.
        E.g.: `processed_bias:X20001231Q000_bias.fits`
    recipe_name : str
        Name of the recipe used by `Reduce` ("_default").
    user_parameters : tuple
        Pairs containing "primitive_name:parameter" and value.

    Returns
    -------
    str
        The first file name of the reduced data.
    """
    tags = tags if tags is not None else []
    xtags = xtags if xtags is not None else []
    calib_files = calib_files if calib_files is not None else []
    user_parameters = user_parameters if user_parameters is not None else []

    bin_x, bin_y = binning.split('x')

    bin_expression = \
        "detector_x_bin=={:s} and detector_y_bin=={:s}".format(bin_x, bin_y)

    e = dataselect.expr_parser(
        "{:s} and {:s}".format(expression, bin_expression))

    data = dataselect.select_data(
        list_of_files, tags=tags, xtags=xtags, expression=e)

    r = Reduce()
    r.files.extend(data)
    r.recipename = recipe_name
    r.ucals = normalize_ucals(r.files, calib_files)
    r.uparms = user_parameters
    r.runr()

    return r.output_filenames[0]


@pytest.fixture(scope="module")
def calibrations():
    return []


# @pytest.mark.remote_data
@pytest.mark.parametrize("path,binning,upars,files", test_case, scope="module")
def test_gmos_sq_image(path, binning, upars, files, calibrations, output_dir):

    # Setting up
    calibrations.clear()
    setup_log(output_dir(path))

    # Test reduce bias
    files = [testing.download_from_archive(f, path) for f in files]
    master_bias = _reduce(files, binning, tags=['BIAS'])
    calibrations.append('processed_bias:{:s}'.format(master_bias))

    # Test reduce flat
    files = [testing.download_from_archive(f, path) for f in files]
    master_flat = _reduce(files, binning, tags=['FLAT'], calib_files=calibrations)
    calibrations.append('processed_flat:{:s}'.format(master_flat))

    # Test reduce fringe
    expression = 'observation_class=="science" or observation_class==None'
    files = [testing.download_from_archive(f, path) for f in files]
    master_fringe = _reduce(
        files,
        binning,
        xtags=['CAL'],
        expression=expression,
        user_parameters=upars,
        calib_files=calibrations,
        recipe_name='makeProcessedFringe')

    calibrations.append('processed_fringe:{:s}'.format(master_fringe))

    # Test reduce sci
    expression = 'observation_class=="science" or observation_class==None'
    files = [testing.download_from_archive(f, path) for f in files]
    _reduce(
        files,
        binning,
        xtags=['CAL'],
        expression=expression,
        user_parameters=upars,
        calib_files=calibrations)



# ==============================================================================
# These tests need refactoring to reduce the replication of API boilerplate

@pytest.mark.skip(reason="Investigate MemoryError")
@pytest.mark.integtest
def test_reduce_image_GN_HAM_2x2_z(path_to_inputs):
    logutils.config(file_name='gmos_test_reduce_image_GN_HAM_2x2_z.log')

    calib_files = []

    raw_subdir = 'GMOS/GN-2017B-LP-15'

    all_files = sorted(glob.glob(
        os.path.join(path_to_inputs, raw_subdir, '*.fits')))
    assert len(all_files) > 1

    list_of_bias = dataselect.select_data(
        all_files,
        ['BIAS'],
        []
    )

    list_of_z_flats = dataselect.select_data(
        all_files,
        ['TWILIGHT'],
        [],
        dataselect.expr_parser('filter_name=="z"')
    )

    list_of_science_files = dataselect.select_data(
        all_files, [],
        ['CAL'],
        dataselect.expr_parser(
            'observation_class=="science" and filter_name=="z"'
        )
    )

    reduce_bias = Reduce()
    assert len(reduce_bias.files) == 0

    reduce_bias.files.extend(list_of_bias)
    assert len(reduce_bias.files) == len(list_of_bias)

    reduce_bias.runr()

    calib_files.append(
        'processed_bias:{}'.format(reduce_bias.output_filenames[0])
    )

    reduce_flats = Reduce()
    reduce_flats.files.extend(list_of_z_flats)
    reduce_flats.ucals = normalize_ucals(reduce_flats.files, calib_files)
    reduce_flats.runr()

    calib_files.append(
        'processed_flat:{}'.format(reduce_flats.output_filenames[0])
    )

    # If makeFringe is included in the science recipe, this can be omitted:
    reduce_fringe = Reduce()
    reduce_fringe.files.extend(list_of_science_files)
    reduce_fringe.ucals = normalize_ucals(reduce_fringe.files, calib_files)
    reduce_fringe.recipename = 'makeProcessedFringe'
    reduce_fringe.runr()

    calib_files.append(
        'processed_fringe:{}'.format(reduce_fringe.output_filenames[0])
    )

    reduce_target = Reduce()
    reduce_target.files.extend(list_of_science_files)
    reduce_target.ucals = normalize_ucals(reduce_target.files, calib_files)
    reduce_target.runr()


@pytest.mark.skip(reason="Investigate MemoryError")
@pytest.mark.integtest
def test_reduce_image_GN_EEV_2x2_g(path_to_inputs):
    logutils.config(file_name='gmos_test_reduce_image_GN_EEV_2x2_g.log')

    calib_files = []

    raw_subdir = 'GMOS/GN-2002A-Q-89'

    all_files = sorted(glob.glob(
        os.path.join(path_to_inputs, raw_subdir, '*.fits')))
    assert len(all_files) > 1

    list_of_bias = dataselect.select_data(
        all_files,
        ['BIAS'],
        []
    )

    list_of_flats = dataselect.select_data(
        all_files,
        ['IMAGE', 'FLAT'],
        [],
        dataselect.expr_parser('filter_name=="g"')
    )

    # These old data don't have an OBSCLASS keyword:
    list_of_science_files = dataselect.select_data(
        all_files, [],
        ['CAL'],
        dataselect.expr_parser(
            'object=="PerseusField4" and filter_name=="g"'
        )
    )

    reduce_bias = Reduce()
    assert len(reduce_bias.files) == 0

    reduce_bias.files.extend(list_of_bias)
    assert len(reduce_bias.files) == len(list_of_bias)

    reduce_bias.runr()

    calib_files.append(
        'processed_bias:{}'.format(reduce_bias.output_filenames[0])
    )

    reduce_flats = Reduce()
    reduce_flats.files.extend(list_of_flats)
    reduce_flats.ucals = normalize_ucals(reduce_flats.files, calib_files)
    reduce_flats.runr()

    calib_files.append(
        'processed_flat:{}'.format(reduce_flats.output_filenames[0])
    )

    reduce_target = Reduce()
    reduce_target.files.extend(list_of_science_files)
    reduce_target.ucals = normalize_ucals(reduce_target.files, calib_files)
    reduce_target.runr()


@pytest.mark.skip(reason="Investigate MemoryError")
@pytest.mark.integtest
def test_reduce_image_GS_HAM_1x1_i(path_to_inputs):
    logutils.config(file_name='gmos_test_reduce_image_GS_HAM_1x1_i.log')

    calib_files = []

    raw_subdir = 'GMOS/GS-2017B-Q-6'

    all_files = sorted(glob.glob(
        os.path.join(path_to_inputs, raw_subdir, '*.fits')))
    assert len(all_files) > 1

    list_of_sci_bias = dataselect.select_data(
        all_files,
        ['BIAS'],
        [],
        dataselect.expr_parser('detector_x_bin==1 and detector_y_bin==1')
    )

    list_of_sci_flats = dataselect.select_data(
        all_files,
        ['TWILIGHT'],
        [],
        dataselect.expr_parser(
            'filter_name=="i" and detector_x_bin==1 and detector_y_bin==1'
        )
    )

    list_of_science_files = dataselect.select_data(
        all_files, [],
        ['CAL'],
        dataselect.expr_parser(
            'observation_class=="science" and filter_name=="i"'
        )
    )

    reduce_bias = Reduce()
    assert len(reduce_bias.files) == 0

    reduce_bias.files.extend(list_of_sci_bias)
    assert len(reduce_bias.files) == len(list_of_sci_bias)

    reduce_bias.runr()

    calib_files.append(
        'processed_bias:{}'.format(reduce_bias.output_filenames[0])
    )

    reduce_flats = Reduce()
    reduce_flats.files.extend(list_of_sci_flats)
    # reduce_flats.uparms = [('addDQ:user_bpm', 'fixed_bpm_1x1_FullFrame.fits')]
    reduce_flats.ucals = normalize_ucals(reduce_flats.files, calib_files)
    reduce_flats.runr()

    calib_files.append(
        'processed_flat:{}'.format(reduce_flats.output_filenames[0])
    )

    reduce_target = Reduce()
    reduce_target.files.extend(list_of_science_files)
    reduce_target.ucals = normalize_ucals(reduce_target.files, calib_files)
    reduce_target.uparms = [
        ('stackFrames:memory', 1),
        # ('addDQ:user_bpm', 'fixed_bpm_1x1_FullFrame.fits'),
        ('adjustWCSToReference:rotate', True),
        ('adjustWCSToReference:scale', True),
        ('resampleToCommonFrame:interpolator', 'spline3')
    ]
    reduce_target.runr()


@pytest.mark.skip(reason="Investigate MemoryError")
@pytest.mark.integtest
def test_reduce_image_GS_HAM_2x2_i_std(path_to_inputs):
    logutils.config(file_name='gmos_test_reduce_image_GS_HAM_1x1_i.log')

    calib_files = []

    raw_subdir = 'GMOS/GS-2017B-Q-6'

    all_files = sorted(glob.glob(
        os.path.join(path_to_inputs, raw_subdir, '*.fits')))
    assert len(all_files) > 1

    list_of_sci_bias = dataselect.select_data(
        all_files,
        ['BIAS'],
        [],
        dataselect.expr_parser('detector_x_bin==2 and detector_y_bin==2')
    )

    list_of_sci_flats = dataselect.select_data(
        all_files,
        ['TWILIGHT'],
        [],
        dataselect.expr_parser(
            'filter_name=="i" and detector_x_bin==2 and detector_y_bin==2'
        )
    )

    list_of_science_files = dataselect.select_data(
        all_files, [],
        [],
        dataselect.expr_parser(
            'observation_class=="partnerCal" and filter_name=="i"'
        )
    )

    reduce_bias = Reduce()
    assert len(reduce_bias.files) == 0

    reduce_bias.files.extend(list_of_sci_bias)
    assert len(reduce_bias.files) == len(list_of_sci_bias)

    reduce_bias.runr()

    calib_files.append(
        'processed_bias:{}'.format(reduce_bias.output_filenames[0])
    )

    reduce_flats = Reduce()
    reduce_flats.files.extend(list_of_sci_flats)
    # reduce_flats.uparms = [('addDQ:user_bpm', 'fixed_bpm_2x2_FullFrame.fits')]
    reduce_flats.ucals = normalize_ucals(reduce_flats.files, calib_files)
    reduce_flats.runr()

    calib_files.append(
        'processed_flat:{}'.format(reduce_flats.output_filenames[0])
    )

    reduce_target = Reduce()
    reduce_target.files.extend(list_of_science_files)
    reduce_target.ucals = normalize_ucals(reduce_target.files, calib_files)
    reduce_target.uparms = [
        ('stackFrames:memory', 1),
        # ('addDQ:user_bpm', 'fixed_bpm_2x2_FullFrame.fits'),
        ('resampleToCommonFrame:interpolator', 'spline3')
    ]
    reduce_target.runr()


if __name__ == '__main__':
    pytest.main()
