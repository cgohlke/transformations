# -*- coding: utf-8 -*-
# transformations/setup.py

"""Transformations package setuptools script."""

import sys
import re
import warnings

from setuptools import setup, Extension

import numpy

with open('transformations/transformations.py') as fh:
    code = fh.read()

version = re.search(r"__version__ = '(.*?)'", code).groups()[0]
description = re.search(r'"""(.*)\.[\r\n?|\n]', code).groups()[0]
readme = re.search(r'[\r\n?|\n]{2}"""(.*)"""[\r\n?|\n]{2}from', code,
                   re.MULTILINE | re.DOTALL).groups()[0]
license = re.search(r'(# Copyright.*?[\r\n?|\n])[\r\n?|\n]+""', code,
                    re.MULTILINE | re.DOTALL).groups()[0]

readme = '\n'.join([description, '=' * len(description)]
                   + readme.splitlines()[1:])
license = license.replace('# ', '').replace('#', '')

if 'sdist' in sys.argv:
    with open('LICENSE', 'w') as fh:
        fh.write(license)
    with open('README.rst', 'w') as fh:
        fh.write(readme)

ext_modules = [
    Extension('transformations._transformations',
              ['transformations/transformations.c'],
              include_dirs=[numpy.get_include()],)]

setup_args = dict(
    name='transformations',
    version=version,
    description=description,
    long_description=readme,
    author='Christoph Gohlke',
    author_email='cgohlke@uci.edu',
    url='https://www.lfd.uci.edu/~gohlke/',
    python_requires='>=2.7',
    install_requires=['numpy>=1.11.3'],
    packages=['transformations'],
    license='BSD',
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    )

try:
    if '--universal' in sys.argv:
        raise ValueError(
            'Not building the _transformations C extension in universal mode')
    setup(ext_modules=ext_modules, **setup_args)
except Exception as e:
    warnings.warn(str(e))
    warnings.warn(
        'The _transformations C extension module was not built.\n'
        'Using a fallback module with limited functionality and performance.')
    setup(**setup_args)
