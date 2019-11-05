#!/usr/bin/env python

import glob
import os
import shutil

import pytest

from gempy.adlibrary import dataselect
from gempy.utils import logutils
from recipe_system.reduction.coreReduce import Reduce
from recipe_system.utils.reduce_utils import normalize_ucals
from .conftest import ConfigTestsGmos

try:
    import gemini_calmgr

    HAS_GEMINI_CALMGR = True
except (ImportError, ModuleNotFoundError):
    HAS_GEMINI_CALMGR = False

datasets = [
    ("GMOS/GN-2017B-LP-15", "2x2", "science"),  # GN HAM 2x2 z-band
    ("GMOS/GN-2002A-Q-89", "2x2", None),  # GN EEV 2x2 g-band
    # ('GMOS/GS-2017B-Q-6', "1x1", "science"),  # GS HAM 1x1 i-band
]


@pytest.fixture(scope='class', params=datasets)
def config(request, path_to_inputs, path_to_outputs):
    """

    """
    # Set up ---
    dataset_dir, binning, obs_class = request.param

    c = ConfigTestsGmosImaging(
        dataset_dir, binning, obs_class, path_to_inputs, path_to_outputs)

    yield c

    # Tear down ---
    if request.session.testsfailed == 0:
        shutil.rmtree(c.output_dir)

    del c


class ConfigTestsGmosImaging(ConfigTestsGmos):
    """
    Config class created for each dataset folder to be used on GMOS Imaging
    Recipes.

    Parameters
    ----------
    dataset_dir : str
        Relative path to the input dataset.
    input_root_dir : str
        Absolute path to the input root directory.
    output_root_dir : str
        Absolute path to the output root directory.
    """

    def __init__(self, dataset_dir, binning, obs_class, input_root_dir, output_root_dir):

        super(ConfigTestsGmosImaging, self).__init__(
            dataset_dir, input_root_dir, output_root_dir)

        bin_x, bin_y = binning.split('x')

        cal_select = dataselect.expr_parser(
            'detector_x_bin=={} and detector_y_bin=={}'.format(bin_x, bin_y))

        if obs_class is None:
            sci_select = cal_select
        else:
            sci_select = dataselect.expr_parser(
                '{} and observation_class=="{}"'.format(cal_select, obs_class))

        self.list_of_biases = dataselect.select_data(
            self.dataset, ['BIAS'], [], cal_select)

        self.list_of_flats = dataselect.select_data(
            self.dataset, ['FLAT'], [], cal_select)

        self.list_of_sci = dataselect.select_data(
            self.dataset, [], ['CAL'], sci_select)

        self.setup_log(__file__)


@pytest.mark.skipif('not HAS_GEMINI_CALMGR')
class TestGmosReduceImaging:
    """
    Collection of tests that will run on every `dataset_folder`.
    """

    @staticmethod
    def test_can_run_reduce_bias(config):
        # These asserts make sure tests are executed in correct order
        assert len(list(config.caldb.list_files())) == 0

        reduce = Reduce()
        reduce.files.extend(config.list_of_biases)
        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])
        assert len(list(config.caldb.list_files())) == 1

    @staticmethod
    def test_can_run_reduce_flat(config):
        assert len(list(config.caldb.list_files())) == 1

        reduce = Reduce()
        reduce.files.extend(config.list_of_flats)
        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])
        assert len(list(config.caldb.list_files())) == 2

    @staticmethod
    def test_can_make_fringe_frame(config):
        reduce = Reduce()

        print(config.list_of_sci)
        reduce.files.extend(config.list_of_sci)

        reduce.recipename = 'makeProcessedFringe'

        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])

    @staticmethod
    def test_can_reduce_science(config):
        reduce = Reduce()
        reduce.files.extend(config.list_of_sci)
        reduce.runr()


# These tests need refactoring to reduce the replication of API boilerplate

# noinspection PyPep8Naming
# @pytest.mark.skip(reason="Investigate MemoryError")
# @pytest.mark.integtest
# def test_reduce_image_GN_HAM_2x2_z(path_to_inputs):
#     logutils.config(file_name='gmos_test_reduce_image_GN_HAM_2x2_z.log')
#
#     calib_files = []
#
#     raw_subdir = 'GMOS/GN-2017B-LP-15'
#
#     all_files = sorted(glob.glob(
#         os.path.join(path_to_inputs, raw_subdir, '*.fits')))
#     assert len(all_files) > 1
#
#     list_of_bias = dataselect.select_data(
#         all_files,
#         ['BIAS'],
#         []
#     )
#
#     list_of_z_flats = dataselect.select_data(
#         all_files,
#         ['TWILIGHT'],
#         [],
#         dataselect.expr_parser('filter_name=="z"')
#     )
#
#     list_of_science_files = dataselect.select_data(
#         all_files, [],
#         ['CAL'],
#         dataselect.expr_parser(
#             'observation_class=="science" and filter_name=="z"'
#         )
#     )
#
#     reduce_bias = Reduce()
#     assert len(reduce_bias.files) == 0
#
#     reduce_bias.files.extend(list_of_bias)
#     assert len(reduce_bias.files) == len(list_of_bias)
#
#     reduce_bias.runr()
#
#     calib_files.append(
#         'processed_bias:{}'.format(reduce_bias.output_filenames[0])
#     )
#
#     reduce_flats = Reduce()
#     reduce_flats.files.extend(list_of_z_flats)
#     reduce_flats.ucals = normalize_ucals(reduce_flats.files, calib_files)
#     reduce_flats.runr()
#
#     calib_files.append(
#         'processed_flat:{}'.format(reduce_flats.output_filenames[0])
#     )
#
#     # If makeFringe is included in the science recipe, this can be omitted:
#     reduce_fringe = Reduce()
#     reduce_fringe.files.extend(list_of_science_files)
#     reduce_fringe.ucals = normalize_ucals(reduce_fringe.files, calib_files)
#     reduce_fringe.recipename = 'makeProcessedFringe'
#     reduce_fringe.runr()
#
#     calib_files.append(
#         'processed_fringe:{}'.format(reduce_fringe.output_filenames[0])
#     )
#
#     reduce_target = Reduce()
#     reduce_target.files.extend(list_of_science_files)
#     reduce_target.ucals = normalize_ucals(reduce_target.files, calib_files)
#     reduce_target.runr()


# noinspection PyPep8Naming
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


# noinspection PyPep8Naming
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


# noinspection PyPep8Naming
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
