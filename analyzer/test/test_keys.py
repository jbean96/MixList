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
c9 = keys.Camelot(7, 'B')

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

def test_perfect_fourth():
    assert c6.perfect_fourth() == c5
    assert c6.compare(c5) == 0.5
    assert c5.perfect_fourth() == c8
    assert c5.compare(c8) == 0.5
    assert c1.perfect_fourth() == c3
    assert c1.compare(c3) == 0.5

def test_perfect_fifth():
    assert c5.perfect_fifth() == c6
    assert c5.compare(c6) == 0.5
    assert c8.perfect_fifth() == c5
    assert c8.compare(c5) == 0.5
    assert c3.perfect_fifth() == c1
    assert c3.compare(c1) == 0.5

def test_parallel_key():
    assert c1.parallel_key() == c7
    assert c1.compare(c7) == 0.2
    assert c7.parallel_key() == c1
    assert c7.compare(c1) == 0.2
    assert c9.parallel_key() == c6
    assert c9.compare(c6) == 0.2
    assert c6.parallel_key() == c9
    assert c6.compare(c9) == 0.2

def test_relative_key():
    assert c7.change_mode() == c5
    assert c7.compare(c5) == 0.3
    assert c5.change_mode() == c7
    assert c5.compare(c7) == 0.3
    assert c2.change_mode() == c1
    assert c2.compare(c1) == 0.3
    assert c1.change_mode() == c2
    assert c1.compare(c2) == 0.3