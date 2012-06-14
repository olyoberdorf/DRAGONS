#!/usr/bin/env python

"""
Setup script for gempy.

The tools and modules in this package are developed by the Gemini Data Processing Software Group.

In this module:
  instruments:  Instrument specific tools or functions

Usage:
  python setup.py install --prefix=/astro/iraf/rhux-x86_64-glibc2.5/gempylocal
  python setup.py sdist
"""

import os.path
import re

from distutils.core import setup

MODULENAME = 'gempy'

# PACKAGES and PACKAGE_DIRS
SUBMODULES = []
PACKAGES = [MODULENAME]
for m in SUBMODULES:
    PACKAGES.append('.'.join([MODULENAME,m]))
PACKAGE_DIRS = {}
PACKAGE_DIRS[MODULENAME] = '.'

# PACKAGE_DATA
PACKAGE_DATA = {}
for p in PACKAGES:
    PACKAGE_DATA[p]=['Copyright',
                     'ReleaseNote',
                     'README',
                     'INSTALL',
                     ]

DATA_FILES = []
DOC_DIR = os.path.join('share','gempy')
svndir = re.compile('.svn')
for root, dirs, files in os.walk('doc'):
    if not svndir.search(root) and len(files) > 0:
        dest = root.split('/',1)[1] if len(root.split('/',1)) > 1 else ""
        DOC_FILES = map((lambda f: os.path.join(root,f)), files)      
        DATA_FILES.append( (os.path.join(DOC_DIR,dest), DOC_FILES) )
for root, dirs, files in os.walk('doc-local'):
    if not svndir.search(root) and len(files) > 0:
        dest = root.split('/',1)[1] if len(root.split('/',1)) > 1 else ""
        DOC_FILES = map((lambda f: os.path.join(root,f)), files)      
        DATA_FILES.append( (os.path.join(DOC_DIR,dest), DOC_FILES) )


# SCRIPTS
GEMPY_SCRIPTS = [ os.path.join('scripts','redux'),
                  os.path.join('scripts','fwhm_histogram'),
                  os.path.join('scripts','psf_plot'),
                  os.path.join('scripts','zp_histogram')
#                 os.path.join('iqtool','iqtool'),
                 ]
##SCRIPTS = [os.path.join('scripts','cleanir.py')]
SCRIPTS = []
SCRIPTS.extend(GEMPY_SCRIPTS)

EXTENSIONS = None

setup ( name='gempy',
        version='0.1.0',
        description='Gemini Data Reduction Software',
        author='Gemini Data Processing Software Group',
        author_email='klabrie@gemini.edu',
        url='http://www.gemini.edu',
        maintainer='Gemini Data Processing Software Group',
        packages=PACKAGES,
        package_dir=PACKAGE_DIRS,
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        scripts=SCRIPTS,
        ext_modules=EXTENSIONS,
        classifiers=[
            'Development Status :: Beta',
            'Intended Audience :: Gemini Staff',
            'Operating System :: Linux :: RHEL',
            'Programming Language :: Python',
            'Topic :: Gemini',
            'Topic :: Data Reduction',
            'Topic :: Astronomy',
            ],
      )