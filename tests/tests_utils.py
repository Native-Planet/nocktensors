import unittest
from nocktensors.interface import nock
from nocktensors.utils import create_noun
from nocktensors.interpreter import free, top, is_cell, get_head, get_tail, get_value

class TestNockUtils(unittest.TestCase):
    def test_create_noun_atom(self):
            idx = create_noun(42)
            self.assertFalse(is_cell(idx))
            self.assertEqual(get_value(idx), 42)

    def test_create_noun_cell(self):
        idx = create_noun([1, 2])
        self.assertTrue(is_cell(idx))
        self.assertEqual(get_value(get_head(idx)), 1)
        self.assertEqual(get_value(get_tail(idx)), 2)

    def test_create_noun_nested_cell(self):
        idx = create_noun([1, [2, 3]])
        self.assertTrue(is_cell(idx))
        head_idx = get_head(idx)
        tail_idx = get_tail(idx)
        self.assertEqual(get_value(head_idx), 1)
        self.assertTrue(is_cell(tail_idx))
        self.assertEqual(get_value(get_head(tail_idx)), 2)
        self.assertEqual(get_value(get_tail(tail_idx)), 3)

    def test_create_noun_list_longer_than_2(self):
        idx = create_noun([1, 2, 3, 4]) # should become [1, [2, [3, 4]]]
        self.assertTrue(is_cell(idx))
        head1_idx = get_head(idx)
        tail1_idx = get_tail(idx)
        self.assertEqual(get_value(head1_idx), 1)
        self.assertTrue(is_cell(tail1_idx))
        head2_idx = get_head(tail1_idx)
        tail2_idx = get_tail(tail1_idx)
        self.assertEqual(get_value(head2_idx), 2)
        self.assertTrue(is_cell(tail2_idx))
        head3_idx = get_head(tail2_idx)
        tail3_idx = get_tail(tail2_idx)
        self.assertEqual(get_value(head3_idx), 3)
        self.assertEqual(get_value(tail3_idx), 4)