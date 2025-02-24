import sys
import os
pypim_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PyPIM'))
sys.path.append(pypim_path)
import pypim as pim

HEAP_SIZE = 10000  # heap tensor
STACK_SIZE = 1000  # stack tensor

heap = pim.Tensor(HEAP_SIZE, 3, dtype=pim.int32)  # [tag, value/head, tail]
stack = pim.Tensor(STACK_SIZE, 6, dtype=pim.int32) # [task_type, arg1, arg2, arg3]
free = pim.Tensor(1, dtype=pim.int32)  # Next free heap index
top = pim.Tensor(1, dtype=pim.int32)   # Stack top index

free[0] = 0
top[0] = 0

def heap_get(idx, dim):
    """Get value from heap tensor at index [idx, dim]."""
    linear_idx = idx * 3 + dim
    return heap[linear_idx]

def heap_set(idx, dim, value):
    """Set value in heap tensor at index [idx, dim]."""
    linear_idx = idx * 3 + dim
    heap[linear_idx] = value

def stack_get(idx, dim):
    """Get value from stack tensor at index [idx, dim]."""
    linear_idx = idx * 6 + dim
    return stack[linear_idx]

def stack_set(idx, dim, value):
    """Set value in stack tensor at index [idx, dim]."""
    linear_idx = idx * 6 + dim
    stack[linear_idx] = value

def is_cell(idx):
    """Check if noun at index is a cell."""
    return heap_get(idx, 0) == 1

def get_value(idx):
    """Get value of an atom at index."""
    if is_cell(idx):
        raise ValueError(f"Cannot get value of a cell at index {idx}")
    return heap_get(idx, 1)

def get_head(idx):
    """Get head index of a cell."""
    if not is_cell(idx):
        raise ValueError(f"Cannot get head of an atom at index {idx}")
    return heap_get(idx, 1)

def get_tail(idx):
    """Get tail index of a cell."""
    if not is_cell(idx):
        raise ValueError(f"Cannot get tail of an atom at index {idx}")
    return heap_get(idx, 2)

def allocate_atom(value):
    """Allocate an atom in the heap with given value."""
    if value < 0:
        raise ValueError("Nock atoms must be non-negative integers")
    global free
    if free[0] >= HEAP_SIZE:
        raise MemoryError("Heap overflow")
    idx = free[0]
    heap_set(idx, 0, 0)  # tag atom
    heap_set(idx, 1, value)
    heap_set(idx, 2, 0)  # unused
    free[0] += 1
    return idx

def allocate_cell(head_idx, tail_idx):
    """Allocate a cell in the heap with head and tail indices."""
    global free
    if free[0] >= HEAP_SIZE:
        raise MemoryError("Heap overflow")
    idx = free[0]
    heap_set(idx, 0, 1)  # tag cell
    heap_set(idx, 1, head_idx)
    heap_set(idx, 2, tail_idx)
    free[0] += 1
    return idx

def push(task_type, arg1, arg2, arg3=0, arg4=0, arg5=0):
    """Push a task onto the stack."""
    global top
    if top[0] >= STACK_SIZE:
        raise MemoryError("Stack overflow")
    stack_set(top[0], 0, task_type)
    stack_set(top[0], 1, arg1)
    stack_set(top[0], 2, arg2)
    stack_set(top[0], 3, arg3)
    top[0] += 1

def pop():
    """Pop a task from the stack."""
    global top
    if top[0] <= 0:
        raise RuntimeError("Stack underflow")
    top[0] -= 1
    return (stack_get(top[0], 0), stack_get(top[0], 1), 
            stack_get(top[0], 2), stack_get(top[0], 3),
            stack_get(top[0], 4), stack_get(top[0], 5))

def slot(n, idx):
    """Fetch the nth slot from noun at idx iteratively."""
    if n < 1:
        raise ValueError("Slot number must be positive")
    current_idx = idx
    if n == 1:
        return current_idx
    while n > 1:
        if not is_cell(current_idx):
            raise ValueError(f"Cannot traverse slot {n} from atom at index {current_idx}")
        if n % 2 == 0:  # head
            current_idx = get_head(current_idx)
            n //= 2
        else:  # tail
            current_idx = get_tail(current_idx)
            n = (n - 1) // 2
    return current_idx

def noun_equal(a_idx, b_idx):
    """Check if two nouns are equal, equivalent to Nock op5."""
    # Both atoms
    if not is_cell(a_idx) and not is_cell(b_idx):
        return get_value(a_idx) == get_value(b_idx)
    # One atom, one cell
    if is_cell(a_idx) != is_cell(b_idx):
        return False
    # Both cells
    return (noun_equal(get_head(a_idx), get_head(b_idx)) and 
            noun_equal(get_tail(a_idx), get_tail(b_idx)))


def op0_compute(subject_idx, formula_idx, result_idx):
    if not is_cell(formula_idx):
        heap_set(result_idx, 0, 0) # Tag as atom
        heap_set(result_idx, 1, get_value(formula_idx))
        heap_set(result_idx, 2, 0)
    else:
        head_idx = get_head(formula_idx)
        if is_cell(head_idx):
            raise ValueError(f"Formula head at {head_idx} is a cell; only atoms 0-11 supported")
        op = get_value(head_idx)
        handlers = {
            0: nock_0, 1: nock_1, 2: nock_2, 3: nock_3, 4: nock_4,
            5: nock_5, 6: nock_6, 7: nock_7, 8: nock_8, 9: nock_9,
            10: nock_10, 11: nock_11
        }
        if op in handlers:
            handlers[op](subject_idx, formula_idx, result_idx)
        else:
            raise ValueError(f"Unsupported op{op}")

def nock_0(subject_idx, formula_idx, result_idx):
    """op0: [a 0 b] → /[b] a (slot operation)."""
    b_idx = get_tail(formula_idx)
    b = get_value(b_idx)
    slot_idx = slot(b, subject_idx)
    heap_set(result_idx, 0, heap_get(slot_idx, 0))
    heap_set(result_idx, 1, heap_get(slot_idx, 1))
    heap_set(result_idx, 2, heap_get(slot_idx, 2))

def nock_1(subject_idx, formula_idx, result_idx):
    """op1: [a 1 b] → b (constant)."""
    b_idx = get_tail(formula_idx)
    heap_set(result_idx, 0, heap_get(b_idx, 0))
    heap_set(result_idx, 1, heap_get(b_idx, 1))
    heap_set(result_idx, 2, heap_get(b_idx, 2))

def nock_2(subject_idx, formula_idx, result_idx):
    """op2: [a 2 b c] → *[*[a b] *[a c]]."""
    tail_idx = get_tail(formula_idx)
    b_idx = get_head(tail_idx)
    c_idx = get_tail(tail_idx)
    temp_x_idx = allocate_atom(0)
    temp_y_idx = allocate_atom(0)
    push(10, temp_x_idx, temp_y_idx, result_idx)
    push(0, subject_idx, c_idx, temp_y_idx)
    push(0, subject_idx, b_idx, temp_x_idx)

def nock_3(subject_idx, formula_idx, result_idx):
    """op3: [a 3 b] → ?*[a b] (is cell)."""
    b_idx = get_tail(formula_idx)
    temp = allocate_atom(0)  # hold *[a b]
    push(2, temp, result_idx, 0)  # check if temp is a cell
    push(0, subject_idx, b_idx, temp)  # compute *[a b]

def nock_4(subject_idx, formula_idx, result_idx):
    """op4: [a 4 b] → +*[a b] (increment)."""
    b_idx = get_tail(formula_idx)
    temp = allocate_atom(0)  # will hold *[a b]
    push(3, temp, result_idx, 0)  # increment temp
    push(0, subject_idx, b_idx, temp)  # compute *[a b]

def nock_5(subject_idx, formula_idx, result_idx):
    """op5: [a 5 b] → =*[a b] (equals)."""
    b_idx = get_tail(formula_idx)
    temp = allocate_atom(0)  # *[a b]
    push(4, temp, result_idx)  # equality check
    push(0, subject_idx, b_idx, temp)  # compute *[a b]

def nock_6(subject_idx, formula_idx, result_idx):
    """op6: [a 6 b c d] → *[a c] if *[a b]=0, *[a d] if *[a b]=1."""
    tail_idx = get_tail(formula_idx)
    b_idx = get_head(tail_idx)
    tail_tail_idx = get_tail(tail_idx)
    c_idx = get_head(tail_tail_idx)
    d_idx = get_tail(tail_tail_idx)
    temp = allocate_atom(0)
    push(6, temp, c_idx, d_idx, subject_idx, result_idx)  # use indices directly
    push(0, subject_idx, b_idx, temp)

def nock_7(subject_idx, formula_idx, result_idx):
    """op7: [a 7 b c] → *[*[a b] c] (compose)."""
    tail_idx = get_tail(formula_idx)
    b_idx = get_head(tail_idx)
    c_idx = get_tail(tail_idx)
    temp = allocate_atom(0)  # *[a b]
    push(7, temp, c_idx, result_idx)  # compose: *[temp c]
    push(0, subject_idx, b_idx, temp)  # compute *[a b]

def nock_8(subject_idx, formula_idx, result_idx):
    """op8: [a 8 b c] → *[[*[a b] a] c] (push)."""
    tail_idx = get_tail(formula_idx)
    b_idx = get_head(tail_idx)
    c_idx = get_tail(tail_idx)
    temp = allocate_atom(0) # *[a b]
    push(8, temp, subject_idx, c_idx, result_idx)  # pass c_idx directly
    push(0, subject_idx, b_idx, temp)  # compute *[a b]

def nock_9(subject_idx, formula_idx, result_idx):
    """op9: [a 9 b c] → *[*[a c] /[b] *[a c]] (invoke)."""
    tail_idx = get_tail(formula_idx)
    b_idx = get_head(tail_idx)
    c_idx = get_tail(tail_idx)
    b = get_value(b_idx)  # slot number
    core_idx = allocate_atom(0)  # index to hold computed *[a c] (core)
    push(9, core_idx, b_idx, result_idx) # continuation
    push(0, subject_idx, c_idx, core_idx)  # compute core *[a c] first

def nock_10(subject_idx, formula_idx, result_idx):
    """op10: [a 10 [b c] d] → *[a d] with slot b = c."""
    # simplified, assumes static edit not supported in this context
    # we compute *[a d]
    tail_idx = get_tail(formula_idx)
    edit_idx = get_head(tail_idx)
    d_idx = get_tail(tail_idx)
    push(0, subject_idx, d_idx, result_idx)  # Compute *[a d]

def nock_11(subject_idx, formula_idx, result_idx):
    """op11: [a 11 b c] → *[a c]; hints ignored."""
    tail_idx = get_tail(formula_idx)
    _ = get_head(tail_idx)  # b (hint), ignored
    c_idx = get_tail(tail_idx)
    push(0, subject_idx, c_idx, result_idx)  # compute *[a c]

def nock_interpreter(subject_idx, formula_idx):
    """Evaluate Nock expression *[subject formula], return result index."""
    result_idx = allocate_cell(0, 0)
    push(0, subject_idx, formula_idx, result_idx)
    while top[0] > 0:
        task_type, arg1, arg2, arg3, arg4, arg5 = pop()
        
        if task_type == 0:  # *[subject formula] → result_idx
            subject_idx, formula_idx, result_idx = arg1, arg2, arg3
            op0_compute(subject_idx, formula_idx, result_idx)

        elif task_type == 1:  # *[arg1 arg2] → arg3
            push(0, arg1, arg2, arg3)
            
        elif task_type == 2:  # 0 if arg1 is cell, 1 if atom
            temp, result_idx = arg1, arg2
            value = 0 if is_cell(temp) else 1
            heap_set(result_idx, 0, 0)
            heap_set(result_idx, 1, value)
            heap_set(result_idx, 2, 0)
            
        elif task_type == 3:  # arg1 + 1 → arg2
            temp, result_idx = arg1, arg2
            if is_cell(temp):
                raise ValueError(f"Cannot increment cell at index {temp}")
            value = get_value(temp)
            heap_set(result_idx, 0, 0)
            heap_set(result_idx, 1, value + 1)
            heap_set(result_idx, 2, 0)
            
        elif task_type == 4:  # =[head tail] of arg1 → arg2
            temp, result_idx = arg1, arg2
            if not is_cell(temp):
                raise ValueError(f"Expected cell for equality at index {temp}")
            value = 0 if noun_equal(get_head(temp), get_tail(temp)) else 1
            heap_set(result_idx, 0, 0)
            heap_set(result_idx, 1, value)
            heap_set(result_idx, 2, 0)
            
        elif task_type == 6:  # if-then-else
            temp, c_idx, d_idx, subject_idx, result_idx = arg1, arg2, arg3, arg4, arg5
            if is_cell(temp):
                raise ValueError(f"Condition must be an atom at index {temp}")
            value = get_value(temp)
            if value == 0:
                push(0, subject_idx, c_idx, result_idx)
            elif value == 1:
                push(0, subject_idx, d_idx, result_idx)
            else:
                raise ValueError(f"Invalid condition value {value}")
                
        elif task_type == 7:  # *[arg1 arg2] → arg3
            push(0, arg1, arg2, arg3)
            
        elif task_type == 8:  # *[[arg1 arg2] arg3] → arg4
            temp, subject_idx, c_idx, result_idx = arg1, arg2, arg3, arg4
            pair_idx = allocate_cell(temp, subject_idx)
            push(0, pair_idx, c_idx, result_idx)
            
        elif task_type == 9: # continuation for op9 after core is computed
            core_idx, b_idx, result_idx = arg1, arg2, arg3
            b = get_value(b_idx) 
            slot_idx = slot(b, core_idx)
            push(0, core_idx, slot_idx, result_idx)

        elif task_type == 10: # continuation after computing temp_x and temp_y
            temp_x, temp_y, result_idx = arg1, arg2, arg3
            heap_set(result_idx, 0, 1)  # Tag: cell
            heap_set(result_idx, 1, arg1)  # Head = temp_x
            heap_set(result_idx, 2, arg2)  # Tail = temp_y

    return result_idx