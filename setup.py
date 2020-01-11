# transformations/setup.py

"""Transformations package setuptools script."""

import sys
import re
import warnings

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext


with open('transformations/transformations.py') as fh:
    code = fh.read()

version = re.search(r"__version__ = '(.*?)'", code).groups()[0]

description = re.search(r'"""(.*)\.(?:\r\n|\r|\n)', code).groups()[0]

readme = re.search(r'(?:\r\n|\r|\n){2}"""(.*)"""(?:\r\n|\r|\n){2}__version__',
                   code, re.MULTILINE | re.DOTALL).groups()[0]

readme = '\n'.join([description, '=' * len(description)] +
                   readme.splitlines()[1:])

license = re.search(r'(# Copyright.*?(?:\r\n|\r|\n))(?:\r\n|\r|\n)+""', code,
                    re.MULTILINE | re.DOTALL).groups()[0]

license = license.replace('# ', '').replace('#', '')

if 'sdist' in sys.argv:
    with open('LICENSE', 'w') as fh:
        fh.write('BSD 3-Clause License\n\n')
        fh.write(license)
    with open('README.rst', 'w') as fh:
        fh.write(readme)


class build_ext(_build_ext):
    """Delay import numpy until build."""
    def finalize_options(self):
        _build_ext.finalize_options(self)
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


ext_modules = [
    Extension('transformations._transformations',
              ['transformations/transformations.c'])]

setup_args = dict(
    name='transformations',
    version=version,
    description=description,
    long_description=readme,
    author='Christoph Gohlke',
    author_email='cgohlke@uci.edu',
    url='https://www.lfd.uci.edu/~gohlke/',
    python_requires='>=3.6',
    install_requires=['numpy>=1.14.5'],
    setup_requires=['setuptools>=18.0', 'numpy>=1.14.5'],
    cmdclass={'build_ext': build_ext},
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
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
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
