"""Pytest configuration."""

import random

import numpy
import pytest

numpy.set_printoptions(legacy='1.21')


@pytest.fixture(autouse=True)
def doctest_config(doctest_namespace):
    """Add random and numpy to doctest namespace."""
    numpy.set_printoptions(suppress=True, precision=5)
    doctest_namespace['numpy'] = numpy
    doctest_namespace['random'] = random
