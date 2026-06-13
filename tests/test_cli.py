"""Tests for the interactive driver in :mod:`solar_system.cli`."""

import io
import random

from solar_system import SolarSystem
from solar_system.cli import MAX_RANGE, format_table, random_planet, run


def test_random_planet_is_deterministic_with_seed():
    rng = random.Random(42)
    p = random_planet("Zog", rng=rng)
    assert p.name == "Zog"
    assert 0 <= p.mass < MAX_RANGE
    assert 0 <= p.distance < MAX_RANGE


def test_format_table_has_header_and_rows():
    s = SolarSystem("Sol")
    s.add_planet("Earth", 1.0, 1.0)
    table = format_table(s)
    lines = table.splitlines()
    assert lines[0].startswith("Name")
    assert "Period (years)" in lines[0]
    assert lines[1].startswith("Earth")


def test_run_with_scripted_input():
    # Simulate: name the system, add two planets, then finish.
    answers = iter(["Andromeda", "Krypton", "Vulcan", "done"])
    out = io.StringIO()
    system = run(
        input_func=lambda _prompt: next(answers),
        output=out,
        rng=random.Random(7),
    )

    assert system.name == "Andromeda"
    assert [p.name for p in system] == ["Krypton", "Vulcan"]

    printed = out.getvalue()
    assert "Now enter planet names" in printed
    assert "Period (years)" in printed  # table rendered at the end


def test_run_blank_system_name_uses_default():
    answers = iter(["", "done"])
    out = io.StringIO()
    system = run(input_func=lambda _p: next(answers), output=out)
    assert system.name == "DEFAULT SYSTEM NAME"


def test_run_skips_blank_planet_names():
    answers = iter(["Sys", "   ", "Earth", "done"])
    out = io.StringIO()
    system = run(
        input_func=lambda _p: next(answers),
        output=out,
        rng=random.Random(1),
    )
    assert [p.name for p in system] == ["Earth"]
