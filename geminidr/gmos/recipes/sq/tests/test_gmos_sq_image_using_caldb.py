#!/usr/bin/env python

import os

import pytest

from astrodata.testing import download_from_archive
from gempy.adlibrary import dataselect
from gempy.utils import logutils
from recipe_system import cal_service
from recipe_system.reduction.coreReduce import Reduce

test_case = [

    # GMOS-N EEV 2x2 g-band ----------------------------
    ('GMOS/GN-2002A-Q-89/', [
        'N20020214S059.fits',  # Sci
        'N20020214S060.fits',  # Sci
        'N20020214S061.fits',  # Sci
        'N20020214S022.fits',  # Bias
        'N20020214S023.fits',  # Bias
        'N20020214S024.fits',  # Bias
        'N20020211S156.fits',  # Flat
        'N20020211S157.fits',  # Flat
        'N20020211S158.fits'  # Flat
    ]),

    # GMOS-N HAM 2x2 z-band ----------------------------
    ('GMOS/GN-2017B-LP-15', [
        'N20170912S0295.fits',  # Bias
        'N20170912S0296.fits',  # Bias
        'N20170912S0297.fits',  # Bias
        'N20170912S0298.fits',  # Bias
        'N20170912S0299.fits',  # Bias
        'N20170913S0153.fits',  # Sci
        'N20170913S0154.fits',  # Sci
        'N20170913S0155.fits',  # Sci
        'N20170913S0156.fits',  # Sci
        'N20170913S0157.fits',  # Sci
        'N20170913S0158.fits',  # Sci
        'N20170914S0481.fits',  # Bias
        'N20170914S0482.fits',  # Bias
        'N20170914S0483.fits',  # Bias
        'N20170914S0484.fits',  # Bias
        'N20170914S0485.fits',  # Bias
        'N20170915S0274.fits',  # Flat
        'N20170915S0275.fits',  # Flat
        'N20170915S0276.fits',  # Flat
        'N20170915S0277.fits',  # Flat
        'N20170915S0278.fits',  # Flat
        'N20170915S0279.fits',  # Flat
        'N20170915S0280.fits',  # Flat
        'N20170915S0281.fits',  # Flat
        'N20170915S0282.fits',  # Flat
        'N20170915S0283.fits',  # Flat
        'N20170915S0284.fits',  # Flat
        'N20170915S0285.fits',  # Flat
        'N20170915S0286.fits',  # Flat
        'N20170915S0287.fits',  # Flat
        'N20170915S0337.fits',  # Bias
        'N20170915S0338.fits',  # Bias
        'N20170915S0339.fits',  # Bias
        'N20170915S0340.fits',  # Bias
        'N20170915S0341.fits',  # Bias
    ])
]


@pytest.mark.remote_data
@pytest.mark.parametrize("dataset_dir,dataset", test_case)
def test_reduce_using_caldb(dataset_dir, dataset, tmp_path):
    # Download remote files ---
    dataset_files = [download_from_archive(f, path=dataset_dir) for f in dataset]

    list_of_bias = dataselect.select_data(dataset_files, ['BIAS'], [])
    list_of_flats = dataselect.select_data(dataset_files, ['FLAT'], [])
    list_of_sci = dataselect.select_data(dataset_files, [], ['CAL'])

    # # Prepare work directory ---
    output_dir = tmp_path / dataset_dir
    output_dir.mkdir(parents="True")
    os.chdir(output_dir)

    # # Setup logging system ---
    log_file = os.path.basename(__file__).replace('.py', '.log')
    log_file = os.path.join(output_dir, log_file)
    logutils.config(mode='quiet', file_name=log_file)

    # Setup Calibration Manager ---
    config_fname = os.path.join(output_dir, "calibration_manager.cfg")

    if os.path.exists(config_fname):
        os.remove(config_fname)

    config_file_content = (
        "[calibs]\n"
        "standalone = True\n"
        "database_dir = {:s}\n".format(str(output_dir))
    )

    with open(config_fname, mode='w') as f:
        f.write(config_file_content)

    calibration_service = cal_service.CalibrationService()
    calibration_service.config(config_file=config_fname, db_dir=output_dir)
    calibration_service.init()

    calibration_service.config(verbose=True)

    # # Reduce bias ---
    reduce = Reduce()
    reduce.files.extend(list_of_bias)
    reduce.runr()

    calibration_service.add_cal(os.path.join(output_dir, reduce.output_filenames[0]))

    # Reduce flats ---
    reduce = Reduce()
    reduce.files.extend(list_of_flats)
    reduce.runr()

    calibration_service.add_cal(os.path.join(output_dir, reduce.output_filenames[0]))


if __name__ == '__main__':
    pytest.main()
