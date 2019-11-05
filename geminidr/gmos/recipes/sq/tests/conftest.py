#!/usr/bin/env python
"""
Configuration file for tests in `geminidr.gmos.recipes.sq`.
"""

import glob
import os

# noinspection PyUnresolvedReferences
from astrodata.testing import path_to_inputs, path_to_refs, path_to_outputs
from gempy.utils import logutils
from recipe_system import cal_service


class ConfigTestsGmos:
    """
    Config class created for each dataset folder.

    Parameters
    ----------
    dataset_dir : str
        Relative path to the input dataset.
    input_root_dir : str
        Absolute path to the input root directory.
    output_root_dir : str
        Absolute path to the output root directory.
    """

    def __init__(self, dataset_dir, input_root_dir, output_root_dir):
        self.dataset_dir = dataset_dir
        self.input_dir = os.path.join(input_root_dir, dataset_dir)
        self.output_dir = os.path.join(output_root_dir, dataset_dir)

        os.makedirs(self.output_dir, exist_ok=True)
        os.chdir(self.output_dir)

        self.caldb = self.setup_caldb()

        self.dataset = sorted(glob.glob(os.path.join(self.input_dir, '*.fits')))

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

    def setup_log(self, filename):
        """
        Set up log to be saved with the output data.

        Parameters
        ----------
        filename : str
            Name of the python test file that invokes this method.
        """
        log_file = os.path.basename(filename).replace('.py', '.log')
        log_file = os.path.join(self.output_dir, log_file)
        logutils.config(mode='quiet', file_name=log_file)
