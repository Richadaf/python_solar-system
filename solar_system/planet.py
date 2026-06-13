"""The :class:`Planet` domain object.

Mirrors ``Planet.java``. The Java original used public getters/setters over
package-private fields and rounded every reported value to three decimal
places. In Python we express the same encapsulation idiomatically with
``@property`` accessors that validate on assignment, and we centralise the
rounding rule in one place.
"""

from __future__ import annotations

# Number of decimal places every reported quantity is rounded to. The Java
# code hard-coded ``Math.round(x * 1000) / 1000.0`` in several spots; here the
# precision lives in a single named constant.
_DISPLAY_PRECISION = 3


class Planet:
    """A single planet orbiting a star.

    Attributes are exposed as validated properties:

    * ``name`` -- the planet's name (non-empty string).
    * ``mass`` -- mass in Earth masses (must be non-negative).
    * ``distance`` -- mean orbital radius in astronomical units, AU
      (must be non-negative).

    All numeric accessors return values rounded to
    :data:`_DISPLAY_PRECISION` decimal places, matching the Java behaviour.
    """

    __slots__ = ("_name", "_mass", "_distance")

    def __init__(self, name: str, mass: float, distance: float) -> None:
        # Route through the property setters so validation runs at construction.
        self.name = name
        self.mass = mass
        self.distance = distance

    # ------------------------------------------------------------------ name
    @property
    def name(self) -> str:
        """The planet's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Planet name must be a non-empty string.")
        self._name = value

    # ------------------------------------------------------------------ mass
    @property
    def mass(self) -> float:
        """Mass in Earth masses, rounded for display."""
        return round(self._mass, _DISPLAY_PRECISION)

    @mass.setter
    def mass(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("Mass cannot be negative.")
        self._mass = value

    # -------------------------------------------------------------- distance
    @property
    def distance(self) -> float:
        """Mean orbital distance in AU, rounded for display."""
        return round(self._distance, _DISPLAY_PRECISION)

    @distance.setter
    def distance(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("Distance cannot be negative.")
        self._distance = value

    # ----------------------------------------------------------- derived data
    @property
    def orbital_period(self) -> float:
        """Orbital period in years, from Kepler's third law.

        Kepler's third law for a body orbiting the Sun states
        ``T**2 == a**3`` (with ``T`` in years and ``a`` in AU), so
        ``T == sqrt(a**3)``. This reproduces ``getOrbitalPeriod()`` from the
        Java source, including the three-decimal rounding.
        """
        period = (self._distance ** 3) ** 0.5
        return round(period, _DISPLAY_PRECISION)

    # ------------------------------------------------------------- dunder API
    def __str__(self) -> str:
        return (
            f"Planet {self.name} has a mass of {self.mass} Earths, "
            f"is {self.distance}AU from its star, "
            f"and orbits in {self.orbital_period} years"
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(name={self.name!r}, "
            f"mass={self.mass!r}, distance={self.distance!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Planet):
            return NotImplemented
        return (
            self.name == other.name
            and self.mass == other.mass
            and self.distance == other.distance
        )

    def __hash__(self) -> int:
        return hash((self.name, self.mass, self.distance))
