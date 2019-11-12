#!/usr/bin/env python
"""
Configuration file for tests in `geminidr.gmos.recipes.sq`.
"""

import pytest

# noinspection PyUnresolvedReferences
from astrodata.testing import path_to_inputs, path_to_refs, path_to_outputs


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({})".format(previousfailed.name))

