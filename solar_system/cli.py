"""Interactive driver -- the Python counterpart of ``FantasySolarSystem.java``.

The original prompted for a system name, then repeatedly read planet names
(stopping on ``done``), assigned each a random mass and distance in the range
``[0, 50)``, printed the planet, and finally rendered a formatted table.

Here that behaviour is split into small, testable pieces:

* :func:`random_planet` -- pure-ish factory for a randomly sized planet.
* :func:`format_table` -- turns a system into the aligned text table.
* :func:`run` -- the I/O loop, with injectable input/output/RNG so it can be
  driven from tests or another program.
"""

from __future__ import annotations

import random
from typing import Callable, TextIO

from solar_system.planet import Planet
from solar_system.solar_system import SolarSystem

# Upper bound (exclusive) for randomly generated mass and distance, matching
# the Java ``MAX_RANGE`` constant.
MAX_RANGE = 50

# The sentinel the user types to finish entering planets.
SENTINEL = "done"


def random_planet(name: str, rng: random.Random | None = None) -> Planet:
    """Create a planet with a random mass and distance in ``[0, MAX_RANGE)``.

    ``rng`` may be supplied (e.g. a seeded :class:`random.Random`) to make the
    result deterministic in tests; otherwise the module-level RNG is used.
    """
    rng = rng or random.Random()
    mass = rng.random() * MAX_RANGE
    distance = rng.random() * MAX_RANGE
    return Planet(name, mass, distance)


def format_table(system: SolarSystem) -> str:
    """Render the planets of ``system`` as an aligned text table.

    Reproduces the column layout from ``displayAllPlanets()``:
    ``Name`` (width 10) and ``Mass`` / ``Distance`` / ``Period (years)``
    (width 20 each), left-justified.
    """
    header = f"{'Name':<10} {'Mass':<20} {'Distance':<20} {'Period (years)':<20}"
    rows = [
        f"{p.name:<10} {p.mass:<20} {p.distance:<20} {p.orbital_period:<20}"
        for p in system
    ]
    return "\n".join([header, *rows])


def run(
    *,
    input_func: Callable[[str], str] = input,
    output: TextIO | None = None,
    rng: random.Random | None = None,
) -> SolarSystem:
    """Run the interactive fantasy-solar-system builder.

    Parameters are injectable so the loop can be exercised without real stdin:

    * ``input_func`` -- callable returning the next line of input.
    * ``output`` -- stream to print to (defaults to ``sys.stdout``).
    * ``rng`` -- random source for planet generation.

    Returns the populated :class:`SolarSystem`.
    """
    import sys

    out = output or sys.stdout
    rng = rng or random.Random()

    def emit(text: str = "") -> None:
        print(text, file=out)

    system_name = input_func("Enter the name of the solar system:") or "DEFAULT SYSTEM NAME"
    system = SolarSystem(system_name)

    emit("Now enter planet names - type 'done' to finish")
    while True:
        planet_name = input_func("Enter name: ")
        if planet_name == SENTINEL:
            emit()
            emit(format_table(system))
            return system
        # Skip blank lines rather than crash the Planet validator.
        if not planet_name.strip():
            continue
        planet = random_planet(planet_name, rng=rng)
        emit(str(planet))
        system.add_planet(planet)


def main() -> None:
    """Console-script entry point."""
    run()


if __name__ == "__main__":
    main()
