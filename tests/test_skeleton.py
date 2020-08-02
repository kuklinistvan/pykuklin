# -*- coding: utf-8 -*-

import pytest
from pykuklin.skeleton import fib

__author__ = "Kuklin István Alexander"
__copyright__ = "Kuklin István Alexander"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
