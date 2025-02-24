from .interpreter import heap, heap_get, allocate_atom, allocate_cell, get_head, get_tail

def create_noun(noun):
    """Create a noun in the heap from a Python object."""
    if isinstance(noun, int):
        return allocate_atom(noun)
    elif isinstance(noun, list) and len(noun) == 2:
        head_idx = create_noun(noun[0])
        tail_idx = create_noun(noun[1])
        return allocate_cell(head_idx, tail_idx)
    elif isinstance(noun, list) and len(noun) > 2:
        # Convert [a, b, c, ...] to [a, [b, [c, ...]]]
        result = create_noun(noun[-1])
        for item in reversed(noun[1:-1]):
            result = allocate_cell(create_noun(item), result)
        return allocate_cell(create_noun(noun[0]), result)
    else:
        raise ValueError(f"Invalid noun structure: {noun}")

def print_noun(idx):
    """Print the noun at the given index."""
    if heap_get(idx, 0) == 0:  # Atom
        print(heap_get(idx, 1), end='')
    else:  # Cell
        print('[', end='')
        print_noun(get_head(idx))
        print(' ', end='')
        print_noun(get_tail(idx))
        print(']', end='')