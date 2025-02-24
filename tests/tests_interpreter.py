import unittest
from nocktensors.interface import nock
from nocktensors.utils import create_noun
from nocktensors.interpreter import free, top, is_cell, get_head, get_tail

class TestNockInterpreter(unittest.TestCase):
    def setUp(self):
        # Reset heap and stack pointers before each test
        free[0] = 0
        top[0] = 0

    def test_op0_slot(self):
        self.assertEqual(nock([4, 5], [0, 2]), 4)  # *[ [4 5] [0 2] ] → 4
        self.assertEqual(nock([4, 5], [0, 3]), 5)  # *[ [4 5] [0 3] ] → 5

    def test_op1_constant(self):
        self.assertEqual(nock(42, [1, 3]), 3)  # *[ 42 [1 3] ] → 3

    def test_op2_compose(self):
        self.assertEqual(nock(42, [2, [1, 5], [1, 6]]), [5, 6])  # *[ 42 [2 [1 5] [1 6]] ] → [5 6]

    def test_op3_is_cell(self):
        self.assertEqual(nock([4, 5], [3, [0, 1]]), 0)  # *[ [4 5] [3 [0 1]] ] → 0 (cell)
        self.assertEqual(nock(7, [3, [0, 1]]), 1)       # *[ 7 [3 [0 1]] ] → 1 (atom)

    def test_op4_increment(self):
        self.assertEqual(nock(7, [4, [0, 1]]), 8)  # *[ 7 [4 [0 1]] ] → 8

    def test_op5_equals(self):
        self.assertEqual(nock([4, 4], [5, [0, 1]]), 0)  # *[ [4 4] [5 [0 1]] ] → 0 (equal)
        self.assertEqual(nock([4, 5], [5, [0, 1]]), 1)  # *[ [4 5] [5 [0 1]] ] → 1 (not equal)

    def test_op6_if(self):
        self.assertEqual(nock(42, [6, [1, 0], [1, 8], [1, 9]]), 8)  # if 0 then 8 else 9
        self.assertEqual(nock(42, [6, [1, 1], [1, 8], [1, 9]]), 9)  # if 1 then 9 else 8

    def test_op7_compose(self):
        self.assertEqual(nock(42, [7, [1, 5], [4, [0, 1]]]), 6)  # *[ *[42 [1 5]] [4 [0 1]] ] → 6

    def test_op8_push(self):
        self.assertEqual(nock(42, [8, [1, 7], [0, 2]]), 7) # *[ [7 42] [0 2] ] → 42

    def test_op9_invoke(self):
        self.assertEqual(nock([0, 42], [9, 3, [0, 1]]), 42)  # Invoke slot 3 on [0 42]

    def test_op10_noop(self):
        self.assertEqual(nock(42, [10, [2, 3], [1, 7]]), 7)  # *[ 42 [1 7] ] → 7 (hint ignored)

    def test_op11_hint(self):
        self.assertEqual(nock(42, [11, 99, [1, 7]]), 7)  # *[ 42 [1 7] ] → 7 (hint ignored)

if __name__ == "__main__":
    unittest.main()