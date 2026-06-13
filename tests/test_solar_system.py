"""Tests for :class:`solar_system.solar_system.SolarSystem`."""

import pytest

from solar_system import Planet, SolarSystem


def test_add_planet_by_fields():
    s = SolarSystem("Sol")
    returned = s.add_planet("Earth", mass=1.0, distance=1.0)
    assert isinstance(returned, Planet)
    assert len(s) == 1
    assert s[0].name == "Earth"


def test_add_planet_by_instance():
    s = SolarSystem("Sol")
    mars = Planet("Mars", 0.107, 1.524)
    s.add_planet(mars)
    assert s[0] is mars


def test_add_planet_rejects_mixed_arguments():
    s = SolarSystem("Sol")
    with pytest.raises(TypeError):
        s.add_planet(Planet("Mars", 0.1, 1.5), mass=2.0)
    with pytest.raises(TypeError):
        s.add_planet("Venus")  # missing mass/distance


def test_get_all_planets_returns_a_copy():
    s = SolarSystem("Sol")
    s.add_planet("Earth", 1.0, 1.0)
    planets = s.get_all_planets()
    planets.clear()
    assert len(s) == 1  # internal state untouched


def test_iteration_and_len():
    s = SolarSystem("Sol")
    s.add_planet("A", 1, 1)
    s.add_planet("B", 2, 2)
    names = [p.name for p in s]
    assert names == ["A", "B"]
    assert len(s) == 2


def test_name_validation():
    with pytest.raises(ValueError):
        SolarSystem("")


def test_str_lists_name_then_planets():
    s = SolarSystem("Sol")
    s.add_planet("Earth", 1.0, 1.0)
    text = str(s)
    assert text.startswith("Sol\n")
    assert "Planet Earth" in text
    assert text.endswith("\n")
