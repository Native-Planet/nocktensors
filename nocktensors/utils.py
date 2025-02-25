from .interpreter import heap, heap_get, allocate_atom, allocate_cell, get_head, get_tail

def create_noun(noun, _depth=0):
    """
    Create a noun in the heap from a Python object.
    
    Args:
        noun: The Python object to convert
        _depth: Internal parameter to track recursion depth
    """
    # Safety check for maximum recursion depth
    if _depth > 500:
        raise RecursionError("Maximum recursion depth exceeded when creating noun")
        
    if isinstance(noun, int):
        return allocate_atom(noun)
    elif isinstance(noun, list) and len(noun) == 2:
        head_idx = create_noun(noun[0], _depth + 1)
        tail_idx = create_noun(noun[1], _depth + 1)
        return allocate_cell(head_idx, tail_idx)
    elif isinstance(noun, list) and len(noun) > 2:
        # Convert to a right-nested binary tree non-recursively
        result = None
        for i in range(len(noun) - 1, -1, -1):
            if isinstance(noun[i], int):
                item_idx = allocate_atom(noun[i])
            elif isinstance(noun[i], list):
                item_idx = create_noun(noun[i], _depth + 1)
            else:
                raise ValueError(f"Invalid noun value: {noun[i]}")
                
            if result is None:
                result = item_idx
            else:
                result = allocate_cell(item_idx, result)
        return result
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