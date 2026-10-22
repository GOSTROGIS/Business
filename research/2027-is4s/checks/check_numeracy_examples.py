"""Check arithmetic in is4s-numeracy-starters.md using exact values.

All inputs are fictional teaching data. No technical or clinical suitability
is inferred from a passing calculation.
"""

from fractions import Fraction as F
from math import isqrt


def clock_minutes(hour, minute):
    return 60 * hour + minute


cases = {
    "Welding": [
        (4 * (125 + 3), 512),
        (600 - 4 * (125 + 3), 88),
        (6 * (125 + 3), 768),
        (6 * (125 + 3) - 600, 168),
    ],
    "Asphalt Paving": [
        (F(50, 1000), F(1, 20)),
        (8 * 3 * F(50, 1000), F(6, 5)),
        (F(6, 5) / 24, F(1, 20)),
        (10 * 3 * F(50, 1000), F(3, 2)),
    ],
    "Ironworker": [
        (12 * F(15, 2), 90),
        (10 * F(15, 2), 75),
        (2 * F(15, 2), 15),
    ],
    "Carpentry": [
        (3**2 + 4**2, 25),
        (isqrt(3**2 + 4**2), 5),
        (6**2 + 8**2, 100),
        (isqrt(6**2 + 8**2), 10),
    ],
    "Piping": [
        (F(80, 100) + F(1250, 1000) + F(65, 100), F(27, 10)),
        (800 + 1250 + 650, 2700),
        (2 * F(27, 10), F(27, 5)),
    ],
    "Tower Crane": [
        (F(45, 100) * 1000, 450),
        (750 + F(45, 100) * 1000 + 125, 1325),
        (F(1325, 1000), F(53, 40)),
        (1325 - 125, 1200),
        (F(1200, 1000), F(6, 5)),
    ],
    "Marine Mechanical Technician": [
        (clock_minutes(10, 25) - clock_minutes(9, 40), 45),
        (F(45, 60), F(3, 4)),
        (clock_minutes(11, 15) - clock_minutes(9, 40), 95),
    ],
    "Security": [
        (clock_minutes(22, 0) - clock_minutes(14, 30), 450),
        (clock_minutes(22, 0) - clock_minutes(14, 30) - 30, 420),
        (F(420, 60), 7),
        (clock_minutes(22, 15) - clock_minutes(14, 30) - 30, 435),
    ],
    "Metal Fabrication": [
        (120 * 80, 9600),
        (40 * 20, 800),
        (6 * 40 * 20, 4800),
        (F(6 * 40 * 20, 120 * 80) * 100, 50),
        (120 * 80 - 6 * 40 * 20, 4800),
        (9 * 40 * 20, 7200),
        (F(9 * 40 * 20, 120 * 80) * 100, 75),
    ],
    "Educational Assistant": [
        (10 + 15 + 20 + 15, 60),
        (F(15, 60), F(1, 4)),
        (F(15, 60) * 100, 25),
        (clock_minutes(9, 0) + 10 + 15, clock_minutes(9, 25)),
        (clock_minutes(9, 0) + 60, clock_minutes(10, 0)),
        (F(15 + 5, 60), F(1, 3)),
    ],
    "Nursing": [
        (F(15, 100) * 1000, 150),
        (250 + F(15, 100) * 1000 + 100, 500),
        (F(500, 1000), F(1, 2)),
        (F(25, 100) + F(15, 100) + F(10, 100), F(1, 2)),
        (500 + F(20, 100) * 1000, 700),
        (F(700, 1000), F(7, 10)),
    ],
}

checks = 0
for program, values in cases.items():
    for index, (actual, expected) in enumerate(values, start=1):
        assert actual == expected, (program, index, actual, expected)
        checks += 1
    print(f"PASS: {program} ({len(values)} checks)")
print(f"Verified {len(cases)} examples; {checks} exact arithmetic checks passed.")
