from .interpreter import nock_interpreter, heap, heap_get, heap_set, is_cell, get_head, get_tail, get_value
from .utils import create_noun, print_noun

def nock(subject, formula):
    """
    Evaluate a Nock expression *[subject formula].
    """
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    return noun_to_python(result_idx)

def noun_to_python(idx):
    """
    Convert a heap index back to a Python representation.
    """
    if is_cell(idx):
        return [noun_to_python(get_head(idx)), noun_to_python(get_tail(idx))]
    else:
        return get_value(idx)