#!/usr/bin/env python3

from distutils.core import setup

longDescription = '''kyuNotebook is cross-platform note-taking program.
This program use Python and PyQt.
'''

setup(name='kyuNotebook',
      version='0.1.0',
      description='Note taking program',
      long_description=longDescription,
      author='YoungUk Kim',
      author_email='bluekyu.dev@gmail.com',
      url='http://www.bluekyu.me/',
      packages=['kyuNotebook'],
      package_dir={'': 'src'},
      scripts=['src/kyuNotebook.pyw'],
      license='GNU GPL v3'
      )
