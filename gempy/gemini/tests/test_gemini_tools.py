# pytest suite
"""
Tests for gemini_tools.

This is a suite of tests to be run with pytest.

To run:
    1) Set the environment variable GEMPYTHON_TESTDATA to the path that
       contains the directories with the test data.
       Eg. /net/chara/data2/pub/gempython_testdata/
    2) From the ??? (location): py.test -v --capture=no
"""
import os
import numpy as np
import astrodata
import gemini_instruments
from datetime import datetime
from gempy.gemini import gemini_tools as gt
from geminidr.gemini.lookups.keyword_comments import keyword_comments

TESTDATAPATH = os.getenv('GEMPYTHON_TESTDATA', '.')

class TestGeminiTools:
    """
    Suite of tests for the functions in the gemini_tools module.
    """
    @classmethod
    def setup_class(cls):
        """Run once at the beginning."""
        pass

    @classmethod
    def teardown_class(cls):
        """Run once at the end."""
        pass

    def setup_method(self, method):
        """Run once before every test."""
        pass

    def teardown_method(self, method):
        """Run once after every test."""
        pass

    def test_add_objcat(self):
        pass

    def test_array_information(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GMOS',
                                            'N20110524S0358_varAdded.fits'))
        ret = gt.array_information(ad)
        assert ret == {'amps_per_array': {1: 1, 2: 1, 3: 1},
                      'amps_order': [0, 1, 2], 'array_number': [1, 2, 3],
                      'reference_extension': 2}

    def test_check_inputs_match(self):
        ad1 = astrodata.open(os.path.join(TESTDATAPATH, 'NIRI',
                                          'N20130404S0372_aligned.fits'))
        ad2 = astrodata.open(os.path.join(TESTDATAPATH, 'NIRI',
                                          'N20130404S0373_aligned.fits'))
        gt.check_inputs_match(ad1, ad2)

    def test_matching_inst_config(self):
        ad1 = astrodata.open(os.path.join(TESTDATAPATH, 'NIRI',
                                          'N20130404S0372_aligned.fits'))
        ad2 = astrodata.open(os.path.join(TESTDATAPATH, 'NIRI',
                                          'N20130404S0373_aligned.fits'))
        assert gt.matching_inst_config(ad1, ad2)

    def test_clip_auxiliary_data(self):
        pass

    def test_clip_auxliary_data_GSAOI(self):
        pass

    def test_clip_sources(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GSAOI',
                                    'S20150110S0208_sourcesDetected.fits'))
        ret = gt.clip_sources(ad)
        # Only check the x-values, which are all unique in the table
        correct_x_values = [(1174.81,), (200.874,1616.33),
                    (915.444,1047.15,1106.54,1315.22), (136.063,957.848)]
        for rv, cv in zip([objcat['x'].data for objcat in ret], correct_x_values):
            assert len(rv) == len(cv)
            for a, b in zip(np.sort(rv), np.sort(cv)):
                assert abs(a-b) < 0.01

    def test_convert_to_cal_header(self):
        pass

    def test_filename_updater(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GMOS',
                                            'N20110524S0358_varAdded.fits'))
        ret = gt.filename_updater(ad, suffix='_forStack', strip=True)
        assert ret == 'N20110524S0358_forStack.fits'

    def test_finalise_ad_input(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GSAOI',
                                    'S20150110S0208_sourcesDetected.fits'))
        tlm = datetime.now()
        ret = gt.finalise_adinput(ad, 'ASSOCSKY', '_forSky')
        dt1 = datetime.strptime(ret.phu.get('ASSOCSKY'), '%Y-%m-%dT%H:%M:%S')
        dt2 = datetime.strptime(ret.phu.get('GEM-TLM'), '%Y-%m-%dT%H:%M:%S')
        assert ret.filename == 'S20150110S0208_forSky.fits'
        assert abs(dt1 - tlm).total_seconds() <= 1
        assert abs(dt2 - tlm).total_seconds() <= 1

    def test_fit_continuum(self):
        pass

    def test_fitsstore_report(self):
        pass

    def test_send_fitsstore_report(self):
        pass

    def test_log_message(self):
        ret = gt.log_message("primitive", "stackSkyFrames", "starting")
        assert ret == 'Starting the primitive stackSkyFrames'
        ret = gt.log_message("primitive", "stackSkyFrames", "completed")
        assert ret == 'The stackSkyFrames primitive completed successfully'

    def test_make_dict(self):
        ret = gt.make_dict([1,2,3], 4)
        assert ret == {1: 4, 2: 4, 3: 4}

    def test_measure_bg_from_image(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GSAOI',
                                    'S20150110S0208_sourcesDetected.fits'))
        ret = gt.measure_bg_from_image(ad)
        correct = [(4766.1092957925521, 133.05741868184813),
                   (4751.3978053635265, 139.48162435882048),
                   (4795.2896966415474, 147.26329160720647),
                   (4757.0842356247831, 137.44112506830069)]
        for rv, cv in zip(ret, correct):
            for a, b in zip(rv, cv):
                assert abs(a - b) < 0.001, 'Problem with gaussfit=True'
        ret = gt.measure_bg_from_image(ad, gaussfit=False)
        correct = [(4766.8877, 118.89507), (4751.3643, 123.5854),
                   (4795.1802, 129.7478), (4756.998, 121.68998)]
        for rv, cv in zip(ret, correct):
            for a, b in zip(rv, cv):
                assert abs(a - b) < 0.001, 'Problem with gaussfit=False'

    def test_measure_bg_from_objcat(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GSAOI',
                                    'S20150110S0208_sourcesDetected.fits'))
        ret = gt.measure_bg_from_objcat(ad)
        correct = [(4790.828125, 42.164431523670345, 14),
                   (4769.064778645833, 68.642491699141189, 24),
                   (4804.6222656250002, 61.375171842936616, 20),
                   (4762.951171875, 23.738846579268809, 16)]
        for rv, cv in zip(ret, correct):
            for a, b in zip(rv, cv):
                assert abs(a - b) < 0.001

    def obsmode_add_del_mark_history(self):
        # Tests obsmode_add, obsmode_del, and mark_history
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GMOS',
                                         'S20160914S0274.fits'))
        tlm = datetime.now().isoformat()[0:-7]
        ad = gt.obsmode_add(ad)
        assert ad.phu.get('OBSMODE') == 'LONGSLIT'
        assert ad.phu.get('GSREDUCE') == ad.phu.get('GEM-TLM') == tlm
        ad = gt.obsmode_del(ad)
        assert ad.phu.get('OBSMODE') == ad.phu.get('GSREDUCE') == None
        pass

    def test_parse_sextractor_param(self):
        pass

    def test_read_database(self):
        pass

    def test_trim_to_data_section(self):
        ad = astrodata.open(os.path.join(TESTDATAPATH, 'GMOS',
                                         'S20160914S0274.fits'))
        new_crpix1 = [ext.hdr.CRPIX1 - (32 if ext.hdr.EXTVER%2==0 else 0)
                      for ext in ad]
        ret = gt.trim_to_data_section(ad, keyword_comments)
        assert all([ext.data.shape == (2112,256) for ext in ret])
        for rv, cv in zip(ret.hdr.CRPIX1, new_crpix1):
            assert abs(rv -cv) < 0.001


    def test_write_database(self):
        pass
