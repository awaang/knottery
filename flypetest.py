from knot import Knot
import unittest

class TestKnotLexographic(unittest.TestCase):
    def test_makelexographic_rotation(self):
        # Dowker code that is not lex minimal
        code = [6, 8, 2, 4]
        knot = Knot(code)
        lex_min = knot.makelexographic()

        # This is expected to match the minimal rotation
        expected = [2, 4, 6, 8]
        self.assertEqual([int(x) for x in lex_min], expected)

class TestKnotFlypes(unittest.TestCase):
    def test_flypedetect_basic(self):
        code = [4, 6, 2, 8]  # An example 4-crossing prime knot
        knot = Knot(code)
        flypes = knot.flypedetect()

        # Ensure flypes are returned as a list of [seq1, seq2, crossing]
        self.assertTrue(all(len(f) == 3 for f in flypes))

    def test_performflype_inverts(self):
        code = [4, 6, 2, 8]
        knot = Knot(code)
        flypes = knot.flypedetect()

        if flypes:
            flyped_code = knot.performflype(flypes[0])
            self.assertIsInstance(flyped_code, list)
            self.assertEqual(len(flyped_code), len(code))

    def test_findflypeclass_consistency(self):
        code = [4, 6, 2, 8]
        knot = Knot(code)
        flypeclass = knot.findflypeclass([code])
        
        for k in flypeclass:
            self.assertIsInstance(k, list)
            self.assertEqual(len(k), len(code))
