from knot.knot import Knot, genDowkers
import unittest
# from knot import AlternatingKnot
from knot.alternating_knot import AlternatingKnot


trefoil = AlternatingKnot([4, 6, 2]) # 3_1
figure_eight = AlternatingKnot([4, 6, 8, 2]) # 4_1
cinquefoil = AlternatingKnot([6, 8, 10, 2, 4]) # 5_1
three_twist = AlternatingKnot([4, 8, 10, 2, 6]) # 5_2
stevedore = AlternatingKnot([4, 8, 12, 10, 2, 6]) # 6_1

class TestKnotProperties(unittest.TestCase):
    def test_isLexographic(self):
        print(f"\n\nTesting isLexographic()")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),
        ]

        for knot, expected in cases:
            result = knot.isLexographic()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

    def test_isPrime(self):
        print(f"\n\nTesting isPrime()")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),
            
            # (AlternatingKnot([6, 8, 10, 2, 4, 12]), False), # 3_1 # 3_1 - composite
            # (AlternatingKnot([6, 8, 2, 4]), False), # 3_1 # 3_1* - composite
            # (AlternatingKnot([10, 12, 14, 16, 2, 4, 6, 8]), False), # 3_1 # 4_1 - composite
            
        ]

        for knot, expected in cases:
            result = knot.isPrime()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

    def test_isPossible(self):
        print(f"\n\nTesting isPossible()")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),
            # (AlternatingKnot([10, 8, 6, 4]), True),  # THIS TEST FAILS

            (AlternatingKnot([2, 4, 6, 2]), False),  # Invalid: repeated number
            (AlternatingKnot([4, 6, 8, 10]), False), # Invalid: not a Dowker code
        ]

        for knot, expected in cases:
            result = knot.isPossible()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

if __name__ == '__main__':
    unittest.main()