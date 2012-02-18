#!/usr/bin/env python3

import os, sys
from distutils.core import setup

srcDirPath = os.path.join(os.getcwd(), os.path.dirname(__file__), 'src')
if srcDirPath not in sys.path:
    sys.path.insert(0, srcDirPath)

import kyunotebooklib

desktop_files = [
        ('share/icons/hicolor/48x48/apps', ['desktop/48x48/kyuNotebook.png']),
        ('share/icons/hicolor/32x32/apps', ['desktop/32x32/kyuNotebook.png']),
        ('share/icons/hicolor/24x24/apps', ['desktop/24x24/kyuNotebook.png']),
        ('share/icons/hicolor/16x16/apps', ['desktop/16x16/kyuNotebook.png']),
        ('share/applications', ['desktop/kyuNotebook.desktop'])]

if sys.platform.startswith('linux'):
    data_files = desktop_files

setup(name=kyunotebooklib.__program_name__,
      version=kyunotebooklib.__version__,
      description='Note taking program',
      long_description='''
kyuNotebook is cross-platform note-taking program. 
This program use Python3 and PyQt4.
''',
      author=kyunotebooklib.__author__,
      author_email='bluekyu.dev@gmail.com',
      url='http://www.bluekyu.me/',
      packages=['kyunotebooklib'],
      package_dir={'': 'src'},
      scripts=['src/kyunotebook'],
      data_files=data_files,
      license='GNU GPL v3'
      )
