from knot.knot import Knot, genDowkers
from knot.alternating_knot import AlternatingKnot
import pytest

# sample knots
trefoil = AlternatingKnot([4, 6, 2])               # 3_1
figure_eight = AlternatingKnot([4, 6, 8, 2])       # 4_1
cinquefoil = AlternatingKnot([6, 8, 10, 2, 4])     # 5_1
three_twist = AlternatingKnot([4, 8, 10, 2, 6])    # 5_2
stevedore = AlternatingKnot([4, 8, 12, 10, 2, 6])  # 6_1

@pytest.mark.parametrize("knot, expected", [
    (trefoil, True),
    (figure_eight, True),
    (cinquefoil, True),
    (three_twist, True),
    (stevedore, True),
    (AlternatingKnot([6, 8, 2, 4]), False),
    (AlternatingKnot([8, 6, 2, 4]), False),
    (AlternatingKnot([8, 10, 12, 4, 6, 2]), False),
])

def test_is_lexographic(knot, expected):
    result = knot.isLexographic()
    print(f"\n> Dowker: {knot}")
    print(f"> Expected: {expected}")
    print(f"> Returned: {result}")
    assert result == expected

@pytest.mark.parametrize("knot, expected", [
    (trefoil, True),
    (figure_eight, True),
    (cinquefoil, True),
    (three_twist, True),
    (stevedore, True),
    (AlternatingKnot([4, 6, 2, 8, 10, 12]), False),
    (AlternatingKnot([4, 6, 2, 8, 10, 12, 14, 16]), False),
    (AlternatingKnot([4, 6, 2, 8, 10, 12, 14, 16, 18, 20]), False),
    (AlternatingKnot([4, 6, 2, 8, 10, 12, 14, 16, 18]), False),
])

def test_is_prime(knot, expected):
    result = knot.isPrime()
    print(f"\n> Dowker: {knot}")
    print(f"> Expected: {expected}")
    print(f"> Returned: {result}")
    assert result == expected

@pytest.mark.parametrize("knot, expected", [
    (trefoil, True),
    (figure_eight, True),
    (cinquefoil, True),
    (three_twist, True),
    (stevedore, True),
    (AlternatingKnot([2, 4, 6, 2]), False),
    (AlternatingKnot([4, 6, 8, 10]), False),
    (AlternatingKnot([4, 8, 2, 10, 6]), False),
])

def test_is_possible(knot, expected):
    result = knot.isPossible()
    print(f"\n> Dowker: {knot}")
    print(f"> Expected: {expected}")
    print(f"> Returned: {result}")
    assert result == expected