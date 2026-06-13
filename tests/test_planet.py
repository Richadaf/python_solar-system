"""Tests for :class:`solar_system.planet.Planet`."""

import math

import pytest

from solar_system import Planet


def test_construction_and_accessors():
    p = Planet("Earth", mass=1.0, distance=1.0)
    assert p.name == "Earth"
    assert p.mass == 1.0
    assert p.distance == 1.0


def test_values_are_rounded_to_three_places():
    p = Planet("Rounder", mass=1.23456, distance=9.87654)
    assert p.mass == 1.235
    assert p.distance == 9.877


def test_orbital_period_uses_keplers_third_law():
    # T = sqrt(a**3); for a = 4 AU -> sqrt(64) = 8 years.
    p = Planet("Far", mass=1.0, distance=4.0)
    assert p.orbital_period == 8.0
    assert math.isclose(p.orbital_period, math.sqrt(4.0 ** 3))


def test_earth_orbits_in_one_year():
    p = Planet("Earth", mass=1.0, distance=1.0)
    assert p.orbital_period == 1.0


def test_setters_validate():
    p = Planet("X", mass=1.0, distance=1.0)
    with pytest.raises(ValueError):
        p.mass = -1
    with pytest.raises(ValueError):
        p.distance = -5
    with pytest.raises(ValueError):
        p.name = "   "


def test_str_matches_expected_sentence():
    p = Planet("Earth", mass=1.0, distance=1.0)
    assert str(p) == (
        "Planet Earth has a mass of 1.0 Earths, "
        "is 1.0AU from its star, and orbits in 1.0 years"
    )


def test_equality_and_hash():
    a = Planet("Earth", 1.0, 1.0)
    b = Planet("Earth", 1.0, 1.0)
    c = Planet("Mars", 0.107, 1.524)
    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert len({a, b, c}) == 2
