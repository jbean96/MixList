# pylint: disable=import-error
# pylint: disable=no-name-in-module

import sys

sys.path.append("..")

from analyzer import keys

c1 = keys.Camelot(12, 'A')
c2 = keys.Camelot(12, 'B')
c3 = keys.Camelot(11, 'A')
c4 = keys.Camelot(1, 'A')
c5 = keys.Camelot(3, 'A')
c6 = keys.Camelot(4, 'A')
c7 = keys.Camelot(3, 'B')
c8 = keys.Camelot(2, 'A')

def test_shift_up():
    assert c1.shift_up() == c4
    assert c5.shift_up() == c6
    assert c3.shift_up() == c1

def test_shift_down():
    assert c1.shift_down() == c3
    assert c6.shift_down() == c5
    assert c5.shift_down() == c8
    assert c8.shift_down() == c4

def test_change_mode():
    assert c7.change_mode() == c5
    assert c5.change_mode() == c7
    assert c2.change_mode() == c1
    assert c1.change_mode() == c2