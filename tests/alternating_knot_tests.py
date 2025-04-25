from knot.knot import Knot, genDowkers
import unittest
from knot.alternating_knot import AlternatingKnot

trefoil = AlternatingKnot([4, 6, 2]) # 3_1
figure_eight = AlternatingKnot([4, 6, 8, 2]) # 4_1
cinquefoil = AlternatingKnot([6, 8, 10, 2, 4]) # 5_1
three_twist = AlternatingKnot([4, 8, 10, 2, 6]) # 5_2
stevedore = AlternatingKnot([4, 8, 12, 10, 2, 6]) # 6_1

class TestKnotProperties(unittest.TestCase):
    def test_isLexographic(self):
        print(f"\n\n------------ Testing isLexographic() -----------------------------------------")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),
            
            (AlternatingKnot([6, 8, 2, 4]), False),
            (AlternatingKnot([8, 6, 2, 4]), False),
            (AlternatingKnot([8, 10, 12, 4, 6, 2]), False),
        ]

        for knot, expected in cases:
            result = knot.isLexographic()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

        print(f"\n------------ PASS ------------------------------------------------------------")

    def test_isPrime(self):
        print(f"\n\n------------ Testing isPrime() -----------------------------------------------")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),

            (AlternatingKnot([4, 8, 6, 2]), False),
            (AlternatingKnot([2, 8, 6, 4]), False),
            (AlternatingKnot([6, 4, 2, 8]), False),
            (AlternatingKnot([6, 8, 10, 2, 4, 12]), False),  

            (AlternatingKnot([4, 6, 2, 10, 12, 8]), False), 
        ]

        for knot, expected in cases:
            result = knot.isPrime()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

        # print(f"\n------------ PASS ------------------------------------------------------------")

    def test_isPossible(self):
        print(f"\n\n------------ Testing isPossible() --------------------------------------------")
        cases = [
            (trefoil, True),
            (figure_eight, True),
            (cinquefoil, True),
            (three_twist, True),
            (stevedore, True),

            (AlternatingKnot([2, 4, 6, 2]), False),
            (AlternatingKnot([4, 6, 8, 10]), False),
            (AlternatingKnot([4, 8, 2, 10, 6]), False),
        ]

        for knot, expected in cases:
            result = knot.isPossible()
            print(f"\n> Dowker: {knot} \n> Expected: {expected}\n> Returned: {result}")
            self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")

        print(f"\n------------ PASS ------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()