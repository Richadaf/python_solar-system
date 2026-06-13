# python_solar-system

An object-oriented model of a (fantasy) solar system - a Python re-imagining of
the original `java_solar-system` project, preserving its domain principles
while expressing them idiomatically in Python.

## Domain principles (carried over from the Java version)

| Java                         | Python                                   | Principle |
|------------------------------|------------------------------------------|-----------|
| `Planet.java`                | `solar_system/planet.py`                 | A planet has a name, mass (Earth masses) and distance (AU); it derives its orbital period from Kepler's third law `T = √(a³)`. |
| getters/setters over fields  | validated `@property` accessors          | Encapsulation - values are validated on assignment and reported rounded to 3 decimals. |
| `SolarSystem.java`           | `solar_system/solar_system.py`           | A named, ordered collection of planets with an overloaded `add_planet`. |
| overloaded `addPlanet`       | type-dispatching `add_planet`            | Accepts either a `Planet` or `(name, mass, distance)`. |
| `FantasySolarSystem.java`    | `solar_system/cli.py`                    | Interactive driver: prompts for a system name, reads planet names until `done`, assigns random mass/distance in `[0, 50)`, prints each planet, then a formatted table. |

## Layout

```
python_solar-system/
├── solar_system/
│   ├── __init__.py        # package exports (Planet, SolarSystem)
│   ├── planet.py          # Planet domain object
│   ├── solar_system.py    # SolarSystem aggregate (sequence protocol)
│   ├── cli.py             # interactive driver + table formatting
│   └── __main__.py        # `python -m solar_system`
├── tests/                 # pytest suite
├── pyproject.toml
└── README.md
```

## Running

From inside `python_solar-system/`:

```bash
# Run the interactive fantasy builder
python -m solar_system

# Or, after `pip install -e .`
fantasy-solar-system
```

Example session:

```
Enter the name of the solar system:Andromeda
Now enter planet names - type 'done' to finish
Enter name: Krypton
Planet Krypton has a mass of 12.34 Earths, is 5.6AU from its star, and orbits in 13.25 years
Enter name: done

Name       Mass                 Distance             Period (years)
Krypton    12.34                5.6                  13.25
```

## Programmatic use

```python
from solar_system import Planet, SolarSystem

system = SolarSystem("Sol")
system.add_planet("Earth", mass=1.0, distance=1.0)
system.add_planet(Planet("Mars", 0.107, 1.524))

for planet in system:               # SolarSystem is iterable
    print(planet.name, planet.orbital_period)

print(system)                        # full multi-line summary
```

## Tests

```bash
pip install -e ".[test]"
pytest
```

## Credit

Domain and behaviour derived from the original Java project,
© 2017 Richard A. Famoroti.
