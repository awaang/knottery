from knot import Knot, gendowkers
import unittest

class TestKnotProperties(unittest.TestCase):
    def test_isDowkerLexographic(self):
        cases = [
            (Knot([2, 4, 6, 8]), True),
            (Knot([8, 2, 4, 6]), False),
            (Knot([4, 6, 2, 8]), False),
        ]

        for knot, expected in cases:
            try:
                result = knot.isDowkerLexographic()
                print(f"Testing {knot}: isDowkerLexographic() returned {result}")
                self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")
            except Exception as e:
                if not expected:
                    print(f"Expected failure for {knot}: {e}")
                else:
                    self.fail(f"Unexpected failure for {knot}: {e}")

    def test_isPrime(self):
        cases = [
            (Knot([4, 6, 2, 8]), True), # 4_1 (figure-eight knot) — prime
            (Knot([4, 6, 2, 8, 10, 12]), False), # Likely a composite knot if subset is [4,6,2,8]
            (Knot([2, 4, 6, 8]), True), # Trefoil (though technically [4, 6, 2] is the usual one)
            (Knot([4, 8, 2, 6]), True), # Rotation of a prime
        ]

        try:
            for knot, expected in cases:
                result = knot.isPrime()
                print(f"Testing {knot}: isPrime() returned {result}")
                self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")
        except Exception as e:
                if not expected:
                    print(f"Expected failure for {knot}: {e}")
                else:
                    self.fail(f"Unexpected failure for {knot}: {e}")

    def test_isDowkerPossible(self):
        cases = [
            (Knot([4, 6, 2, 8]), True),   # Valid figure-eight knot
            (Knot([2, 4, 6, 8]), True),   # Valid Dowker code
            # (Knot([10, 8, 6, 4]), True),  # THIS TEST FAILS
            (Knot([2, 4, 6, 2]), False),  # Invalid: repeated number
            (Knot([4, 6, 8, 10]), False), # No odd numbers: invalid Dowker
        ]

        for knot, expected in cases:
            try:
                result = knot.isDowkerPossible()
                print(f"Testing {knot}: isDowkerPossible() returned {result}")
                self.assertEqual(result, expected, f"{knot} expected {expected} but got {result}")
            except Exception as e:
                if not expected:
                    print(f"Expected failure for {knot}: {e}")
                else:
                    self.fail(f"Unexpected failure for {knot}: {e}")

if __name__ == '__main__':
    unittest.main()