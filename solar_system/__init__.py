"""An object-oriented model of a (fantasy) solar system.

This package is a Python re-imagining of the original Java
``java_solar-system`` project. It keeps the same domain principles:

* A :class:`~solar_system.planet.Planet` is an immutable-ish value with a
  name, a mass (in Earth masses) and an orbital distance (in AU), and it
  can compute its orbital period from Kepler's third law.
* A :class:`~solar_system.solar_system.SolarSystem` is a named collection of
  planets.
* The :mod:`solar_system.cli` module provides the interactive "fantasy"
  driver that builds a random system from user input.

Typical use::

    from solar_system import Planet, SolarSystem

    system = SolarSystem("Sol")
    system.add_planet("Earth", mass=1.0, distance=1.0)
    print(system)
"""

from solar_system.planet import Planet
from solar_system.solar_system import SolarSystem

__all__ = ["Planet", "SolarSystem"]
__version__ = "1.0.0"
