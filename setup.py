#!/usr/bin/env python

from distutils.core import setup

setup(name='gitli',
      version='0.4',
      description='Simple issue management for git',
      long_description=
      '''
gitli is a simple git extension to manage issues in single-developer projects.

The issues are stored in the current branch of the git repository. gitli is
**not** a distributed issue tracker so merges need to be done by hand for now.

To use gitli, simply type ``git li init``, then ``git li new 'issue title'``,
and ``git li list``.

Go to the `gitli homepage <https://github.com/bartdag/gitli>`_ to read the
documentation.

The script does not attempt to prevent goofs and error messages can make
children cry.
      ''',
      author='Barthelemy Dagenais',
      author_email='barthe@users.sourceforge.net',
      license='BSD License',
      url='https://github.com/bartdag/gitli',
      py_modules=['gitli'],
      scripts=['git-li'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Topic :: Software Development :: Bug Tracking',
          ],
     )
      
