"""The :class:`SolarSystem` aggregate.

Mirrors ``SolarSystem.java``: a named, ordered collection of
:class:`~solar_system.planet.Planet` objects with overloaded ``addPlanet``
behaviour and a tabular ``toString``.

Java offered two ``addPlanet`` overloads -- one taking the raw fields and one
taking a ``Planet``. Python has no method overloading, so :meth:`add_planet`
accepts *either* a ready-made :class:`Planet` *or* the ``(name, mass,
distance)`` fields, dispatching on argument type. The container also leans on
Python's data model (``__iter__``, ``__len__``, ``__getitem__``) so a
``SolarSystem`` behaves like a natural read-only sequence of planets.
"""

from __future__ import annotations

from typing import Iterator, List, Optional, overload

from solar_system.planet import Planet


class SolarSystem:
    """A named collection of planets orbiting a common star."""

    __slots__ = ("_name", "_planets")

    def __init__(self, name: str) -> None:
        self.name = name
        self._planets: List[Planet] = []

    # ------------------------------------------------------------------ name
    @property
    def name(self) -> str:
        """The name of the solar system."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Solar system name must be a non-empty string.")
        self._name = value

    # ----------------------------------------------------------- mutation API
    @overload
    def add_planet(self, planet: Planet) -> Planet: ...
    @overload
    def add_planet(self, name: str, mass: float, distance: float) -> Planet: ...

    def add_planet(
        self,
        name_or_planet: "str | Planet",
        mass: Optional[float] = None,
        distance: Optional[float] = None,
    ) -> Planet:
        """Add a planet and return it.

        Two call styles, matching the Java overloads:

        * ``add_planet(planet)`` -- append an existing :class:`Planet`.
        * ``add_planet(name, mass, distance)`` -- build and append one.
        """
        if isinstance(name_or_planet, Planet):
            if mass is not None or distance is not None:
                raise TypeError(
                    "Pass either a Planet instance or (name, mass, distance), "
                    "not both."
                )
            planet = name_or_planet
        else:
            if mass is None or distance is None:
                raise TypeError(
                    "add_planet(name, mass, distance) requires mass and distance."
                )
            planet = Planet(name_or_planet, mass, distance)

        self._planets.append(planet)
        return planet

    # ------------------------------------------------------------- accessors
    def get_all_planets(self) -> List[Planet]:
        """Return a shallow copy of the planet list.

        The Java method handed back its internal ``ArrayList`` directly; we
        return a copy so callers cannot mutate the system's state by accident.
        """
        return list(self._planets)

    # --------------------------------------------------------- sequence protocol
    def __iter__(self) -> Iterator[Planet]:
        return iter(self._planets)

    def __len__(self) -> int:
        return len(self._planets)

    def __getitem__(self, index: int) -> Planet:
        return self._planets[index]

    # ------------------------------------------------------------- dunder API
    def __str__(self) -> str:
        lines = [self.name]
        lines.extend(str(planet) for planet in self._planets)
        # Trailing newline mirrors the Java toString, which appended "\n"
        # after every planet line.
        return "\n".join(lines) + "\n"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, planets={len(self)})"
