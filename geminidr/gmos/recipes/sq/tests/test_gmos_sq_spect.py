#!/usr/bin/python
"""
Tests related to GMOS Long-slit Spectroscopy data reduction.
"""
import glob
import os

# noinspection PyPackageRequirements
import pytest

# noinspection PyUnresolvedReferences
import gemini_instruments
from gempy.adlibrary import dataselect
from gempy.utils import logutils
from recipe_system import cal_service
from recipe_system.reduction.coreReduce import Reduce

dataset_folder_list = [
    'GMOS/GN-2017A-FT-19',
    # 'GMOS/GS-2016B-Q-54-32'
]


@pytest.fixture(scope='class', params=dataset_folder_list)
def config(request, path_to_inputs, path_to_outputs):
    """
    Fixture that returns an object with the data required for the tests
    inside this file. This super fixture avoid confusions with Pytest, Fixtures
    and Parameters that could generate a very large matrix of configurations.

    The `path_to_*` fixtures are defined inside the `conftest.py` file.

    Parameters
    ----------
    request : pytest.fixture
        A special fixture providing information of the requesting test function.
    path_to_inputs : pytest.fixture
        Fixture inherited from `astrodata.testing` with path to the input files.
    path_to_outputs : pytest.fixture
        Fixture inherited from `astrodata.testing` with path to the output files.

    Returns
    -------
    namespace
        An object that contains `.input_dir` and `.output_dir`
    """
    # Set up ---
    c = ConfigTest(request.param, path_to_inputs, path_to_outputs)
    yield c

    # Tear down ---
    os.remove(os.path.join(c.output_dir, "cal_manager.db"))
    del c


class ConfigTest:
    """
    Config class created for each dataset file. It is created from within
    this a fixture so it can inherit the `path_to_*` fixtures as well.
    """

    def __init__(self, path, input_dir, output_dir):
        self.input_dir = os.path.join(input_dir, path)
        self.output_dir = os.path.join(output_dir, path)

        os.makedirs(self.output_dir, exist_ok=True)
        os.chdir(self.output_dir)

        self.caldb = self.setup_caldb()
        self.setup_log()

        dataset = sorted(glob.glob(os.path.join(self.input_dir, '*.fits')))

        self.list_of_biases = dataselect.select_data(dataset, ['BIAS'], [])
        self.list_of_flats = dataselect.select_data(dataset, ['FLAT'], [])
        self.list_of_arcs = dataselect.select_data(dataset, ['ARC'], [])
        self.list_of_sci = dataselect.select_data(dataset, [], ['CAL'])

    def setup_caldb(self):
        """
        Setup calibration service to use new configurations for each dataset.
        """
        config_fname = os.path.join(self.output_dir, "calibration_manager.cfg")

        if os.path.exists(config_fname):
            os.remove(config_fname)

        config_file_content = (
            "[calibs]\n"
            "standalone = True\n"
            "database_dir = {:s}\n".format(self.output_dir)
        )

        with open(config_fname, mode='w') as f:
            f.write(config_file_content)

        calibration_service = cal_service.CalibrationService()
        calibration_service.config(config_file=config_fname)
        calibration_service.init(wipe=True)

        return calibration_service

    def setup_log(self):
        """
        Set up log to be saved with the output data.
        """
        log_file = os.path.basename(__file__).replace('.py', '.log')
        log_file = os.path.join(self.output_dir, log_file)
        logutils.config(mode='quiet', file_name=log_file)


@pytest.mark.gmosls
class TestGmosReduceLongslit:
    """
    Collection of tests that will run on every `dataset_folder`. Both
    `dataset_folder` and `calibrations` parameter should be present on every
    test. Even when the test does not use it.
    """

    @staticmethod
    def test_can_run_reduce_bias(config):
        """
        Make sure that the reduce_BIAS works for spectroscopic data.
        """
        # These asserts make sure tests are executed in correct order
        assert len(list(config.caldb.list_files())) == 0

        reduce = Reduce()
        reduce.files.extend(config.list_of_biases)
        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])
        assert len(list(config.caldb.list_files())) == 1

    @staticmethod
    def test_can_run_reduce_flat(config):
        """
        Make sure that the reduce_FLAT_LS_SPECT works for spectroscopic data.
        """
        assert len(list(config.caldb.list_files())) == 1

        reduce = Reduce()
        reduce.files.extend(config.list_of_flats)
        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])
        assert len(list(config.caldb.list_files())) == 2

    @staticmethod
    def test_can_run_reduce_arc(config):
        """
        Make sure that the recipes_ARC_LS_SPECT can run for spectroscopic
        data.
        """
        assert len(list(config.caldb.list_files())) == 2

        reduce = Reduce()
        reduce.files.extend(config.list_of_arcs)
        reduce.runr()

        config.caldb.add_cal(reduce.output_filenames[0])
        assert len(list(config.caldb.list_files())) == 3

    @staticmethod
    def test_can_run_reduce_science(config):
        """
        Make sure that the recipes_ARC_LS_SPECT works for spectroscopic data.
        """
        reduce = Reduce()
        reduce.files.extend(config.list_of_sci)
        reduce.runr()


if __name__ == '__main__':
    pytest.main()
