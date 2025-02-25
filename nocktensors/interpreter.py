import sys
import os
import time
pypim_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PyPIM'))
sys.path.append(pypim_path)
import pypim as pim

# VRAM-optimized sizes (can be much larger since we're running in GPU memory)
HEAP_SIZE = 5000000   # 5M cells
STACK_SIZE = 100000   # 100K tasks

# GC configuration
GC_THRESHOLD = HEAP_SIZE * 0.7  # Run GC when heap is 70% full
GC_EMERGENCY_THRESHOLD = HEAP_SIZE * 0.9  # Emergency GC with aggressive collection
ENABLE_GC = True                # Global flag to enable/disable GC
DEBUG_GC = False                # Print GC debug information
GC_STATS_WINDOW = 10            # Number of collections to track for performance metrics

# Memory growth configuration
AUTO_EXPAND_HEAP = True         # Automatically expand heap if needed
MAX_HEAP_SIZE = 50000000        # 50M cells maximum (adjust based on available VRAM)
HEAP_GROWTH_FACTOR = 1.5        # Grow by 50% when expanding

# Memory management tensors
heap = pim.Tensor(HEAP_SIZE, 3, dtype=pim.int32)  # [tag, value/head, tail]
stack = pim.Tensor(STACK_SIZE, 6, dtype=pim.int32) # [task_type, arg1, arg2, arg3]
free = pim.Tensor(1, dtype=pim.int32)  # Next free heap index
top = pim.Tensor(1, dtype=pim.int32)   # Stack top index
gc_mark = pim.Tensor(HEAP_SIZE, dtype=pim.int32)  # For garbage collection marking
gc_generations = pim.Tensor(HEAP_SIZE, dtype=pim.int32)  # Track object age for generational GC

# GC statistics
gc_stats = {
    "collections": 0,
    "freed_cells": 0,
    "total_time_ms": 0,
    "last_run_time_ms": 0,
    "collection_times": [],  # Track recent collection times
    "collection_freed": [],  # Track cells freed in recent collections
    "heap_expansions": 0,    # Track number of heap expansions
    "emergency_collections": 0,  # Track emergency collections
    "current_heap_size": HEAP_SIZE, # Current heap size (may grow)
    "high_water_mark": 0     # Highest heap usage observed
}

# Initialize memory
free[0] = 0
top[0] = 0
gc_mark.fill(0)       # Initialize all cells as unmarked
gc_generations.fill(0)  # Initialize all cells as generation 0

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

def gc_mark_noun(idx):
    """Mark a noun and all its children as reachable during garbage collection."""
    if idx >= free[0] or idx < 0:
        return  # Index out of range, skip
    
    # If already marked, avoid infinite recursion
    if gc_mark[idx] == 1:
        return
    
    # Mark the current node
    gc_mark[idx] = 1
    
    # If it's a cell, recursively mark its head and tail
    if is_cell(idx):
        gc_mark_noun(heap_get(idx, 1))  # Mark head
        gc_mark_noun(heap_get(idx, 2))  # Mark tail

def expand_heap():
    """Expand the heap size to accommodate more objects."""
    global heap, gc_mark, gc_generations, HEAP_SIZE, gc_stats
    
    if not AUTO_EXPAND_HEAP:
        return False
    
    old_size = HEAP_SIZE
    new_size = min(int(HEAP_SIZE * HEAP_GROWTH_FACTOR), MAX_HEAP_SIZE)
    
    if new_size <= old_size:
        return False  # Already at maximum size
    
    if DEBUG_GC:
        print(f"GC: Expanding heap from {old_size} to {new_size} cells")
    
    # Create new, larger tensors
    new_heap = pim.Tensor(new_size, 3, dtype=pim.int32)
    new_gc_mark = pim.Tensor(new_size, dtype=pim.int32)
    new_gc_generations = pim.Tensor(new_size, dtype=pim.int32)
    
    # Copy data from old tensors to new tensors
    for i in range(free[0]):
        for j in range(3):
            new_heap[i * 3 + j] = heap[i * 3 + j]
    
    new_gc_mark.fill(0)
    new_gc_generations.fill(0)
    
    # For existing objects, copy their generation information
    for i in range(free[0]):
        new_gc_generations[i] = gc_generations[i]
    
    # Update references
    heap = new_heap
    gc_mark = new_gc_mark
    gc_generations = new_gc_generations
    HEAP_SIZE = new_size
    
    # Update statistics
    gc_stats["heap_expansions"] += 1
    gc_stats["current_heap_size"] = new_size
    
    return True

def gc_collect(emergency=False):
    """
    Run garbage collection to reclaim unused memory.
    
    Args:
        emergency: If True, perform more aggressive collection 
                  and attempt to expand the heap if needed.
    """
    if not ENABLE_GC:
        return
    
    global free, gc_stats
    start_time = time.time()
    
    # Update high water mark
    gc_stats["high_water_mark"] = max(gc_stats["high_water_mark"], free[0])
    
    if DEBUG_GC:
        if emergency:
            print(f"GC: Starting EMERGENCY collection. Heap usage: {free[0]}/{HEAP_SIZE} ({free[0]/HEAP_SIZE*100:.1f}%)")
        else:
            print(f"GC: Starting collection. Heap usage: {free[0]}/{HEAP_SIZE} ({free[0]/HEAP_SIZE*100:.1f}%)")
    
    # Update statistics for emergency collections
    if emergency:
        gc_stats["emergency_collections"] += 1
    
    # Reset all marks
    gc_mark.fill(0)
    
    # Mark phase: Mark all reachable objects from stack roots
    for i in range(top[0]):
        for j in range(1, 6):  # Check all args on stack (more thorough)
            idx = stack_get(i, j)
            if idx > 0 and idx < free[0]:
                gc_mark_noun(idx)
    
    # Compact phase: Move all marked objects to the front of the heap
    # Create a mapping from old to new indices
    new_indices = pim.Tensor(HEAP_SIZE, dtype=pim.int32)
    new_indices.fill(0)
    
    new_free_idx = 0
    for i in range(free[0]):
        if gc_mark[i] == 1:
            new_indices[i] = new_free_idx
            new_free_idx += 1
    
    # Now remap all references and compact the heap
    compact_heap = pim.Tensor(HEAP_SIZE, 3, dtype=pim.int32)
    compact_heap.fill(0)
    
    # Copy marked cells to their new positions
    for i in range(free[0]):
        if gc_mark[i] == 1:
            new_idx = new_indices[i]
            compact_heap[new_idx * 3] = heap_get(i, 0)  # tag
            
            if is_cell(i):
                # Update head/tail references to their new locations
                head_idx = heap_get(i, 1)
                tail_idx = heap_get(i, 2)
                if head_idx < free[0] and gc_mark[head_idx] == 1:
                    compact_heap[new_idx * 3 + 1] = new_indices[head_idx]
                if tail_idx < free[0] and gc_mark[tail_idx] == 1:
                    compact_heap[new_idx * 3 + 2] = new_indices[tail_idx]
            else:
                # For atoms, just copy the value
                compact_heap[new_idx * 3 + 1] = heap_get(i, 1)
            
            # Age the object (for generational GC)
            if gc_generations[i] < 3:  # Cap at generation 3
                gc_generations[new_idx] = gc_generations[i] + 1
            else:
                gc_generations[new_idx] = 3
    
    # Switch to the compacted heap
    cells_freed = free[0] - new_free_idx
    old_free = free[0]
    free[0] = new_free_idx
    
    # Copy the compacted heap back to the original heap tensor
    for i in range(free[0]):
        for j in range(3):
            heap[i * 3 + j] = compact_heap[i * 3 + j]
    
    # If emergency and still not enough space, try to expand the heap
    if emergency and (free[0] > HEAP_SIZE * 0.9) and AUTO_EXPAND_HEAP:
        expand_heap()
    
    # Update statistics
    collection_time_ms = (time.time() - start_time) * 1000
    gc_stats["collections"] += 1
    gc_stats["freed_cells"] += cells_freed
    gc_stats["last_run_time_ms"] = collection_time_ms
    gc_stats["total_time_ms"] += collection_time_ms
    
    # Maintain a window of recent collection metrics
    gc_stats["collection_times"].append(collection_time_ms)
    gc_stats["collection_freed"].append(cells_freed)
    
    # Keep only the most recent GC_STATS_WINDOW collections
    if len(gc_stats["collection_times"]) > GC_STATS_WINDOW:
        gc_stats["collection_times"] = gc_stats["collection_times"][-GC_STATS_WINDOW:]
        gc_stats["collection_freed"] = gc_stats["collection_freed"][-GC_STATS_WINDOW:]
    
    if DEBUG_GC:
        print(f"GC: Completed. Freed {cells_freed} cells ({cells_freed/old_free*100:.1f}%).")
        print(f"GC: New heap usage: {free[0]}/{HEAP_SIZE} ({free[0]/HEAP_SIZE*100:.1f}%)")
        print(f"GC: Time taken: {collection_time_ms:.2f}ms")
        
    return cells_freed

def allocate_atom(value):
    """Allocate an atom in the heap with given value."""
    if value < 0:
        raise ValueError("Nock atoms must be non-negative integers")
    global free
    
    # Check if normal garbage collection is needed
    if ENABLE_GC and free[0] >= int(GC_THRESHOLD):
        gc_collect()
    
    # Emergency collection if we're still close to capacity
    if ENABLE_GC and free[0] >= int(GC_EMERGENCY_THRESHOLD):
        freed = gc_collect(emergency=True)
        
        # If emergency collection didn't free enough, try to expand the heap
        if freed < 100 and AUTO_EXPAND_HEAP:
            expand_heap()
    
    # Final check if we have enough space
    if free[0] >= HEAP_SIZE:
        # One last attempt - emergency collection and forced expansion
        if ENABLE_GC and AUTO_EXPAND_HEAP:
            gc_collect(emergency=True)
            if not expand_heap():
                raise MemoryError(f"Heap overflow ({free[0]}/{HEAP_SIZE}). Could not expand beyond maximum size.")
        else:
            raise MemoryError(f"Heap overflow ({free[0]}/{HEAP_SIZE}). GC: {ENABLE_GC}, Expand: {AUTO_EXPAND_HEAP}")
    
    idx = free[0]
    heap_set(idx, 0, 0)  # tag atom
    heap_set(idx, 1, value)
    heap_set(idx, 2, 0)  # unused
    
    # For new objects, generation is always 0
    gc_generations[idx] = 0
    
    free[0] += 1
    return idx

def allocate_cell(head_idx, tail_idx):
    """Allocate a cell in the heap with head and tail indices."""
    global free
    
    # Check if normal garbage collection is needed
    if ENABLE_GC and free[0] >= int(GC_THRESHOLD):
        gc_collect()
    
    # Emergency collection if we're still close to capacity
    if ENABLE_GC and free[0] >= int(GC_EMERGENCY_THRESHOLD):
        freed = gc_collect(emergency=True)
        
        # If emergency collection didn't free enough, try to expand the heap
        if freed < 100 and AUTO_EXPAND_HEAP:
            expand_heap()
    
    # Final check if we have enough space
    if free[0] >= HEAP_SIZE:
        # One last attempt - emergency collection and forced expansion
        if ENABLE_GC and AUTO_EXPAND_HEAP:
            gc_collect(emergency=True)
            if not expand_heap():
                raise MemoryError(f"Heap overflow ({free[0]}/{HEAP_SIZE}). Could not expand beyond maximum size.")
        else:
            raise MemoryError(f"Heap overflow ({free[0]}/{HEAP_SIZE}). GC: {ENABLE_GC}, Expand: {AUTO_EXPAND_HEAP}")
    
    idx = free[0]
    heap_set(idx, 0, 1)  # tag cell
    heap_set(idx, 1, head_idx)
    heap_set(idx, 2, tail_idx)
    
    # For new objects, generation is always 0
    gc_generations[idx] = 0
    
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

def get_gc_stats():
    """Return the current garbage collection statistics."""
    # Calculate recent stats
    recent_avg_time = 0
    recent_avg_freed = 0
    if gc_stats["collection_times"]:
        recent_avg_time = sum(gc_stats["collection_times"]) / len(gc_stats["collection_times"])
    if gc_stats["collection_freed"]:
        recent_avg_freed = sum(gc_stats["collection_freed"]) / len(gc_stats["collection_freed"])
    
    return {
        # Heap statistics
        "heap_usage": free[0],
        "heap_capacity": HEAP_SIZE,
        "usage_percentage": (free[0] / HEAP_SIZE) * 100,
        "high_water_mark": gc_stats["high_water_mark"],
        "high_water_percentage": (gc_stats["high_water_mark"] / HEAP_SIZE) * 100,
        
        # Collection statistics
        "collections": gc_stats["collections"],
        "emergency_collections": gc_stats["emergency_collections"],
        "cells_freed": gc_stats["freed_cells"],
        
        # Time statistics
        "total_gc_time_ms": gc_stats["total_time_ms"],
        "avg_gc_time_ms": gc_stats["total_time_ms"] / max(1, gc_stats["collections"]),
        "last_gc_time_ms": gc_stats["last_run_time_ms"],
        "recent_avg_time_ms": recent_avg_time,
        
        # Efficiency statistics
        "recent_avg_freed": recent_avg_freed,
        "heap_expansions": gc_stats["heap_expansions"],
        "current_heap_size": gc_stats["current_heap_size"]
    }

def manual_gc(emergency=False):
    """
    Manually trigger garbage collection.
    
    Args:
        emergency: If True, perform more aggressive collection
                  and attempt to expand the heap if needed.
    """
    if not ENABLE_GC:
        print("Garbage collection is disabled.")
        return
    
    old_usage = free[0]
    if emergency:
        freed = gc_collect(emergency=True)
    else:
        freed = gc_collect()
    new_usage = free[0]
    
    print(f"GC: Manual {'emergency ' if emergency else ''}collection completed.")
    print(f"  Before: {old_usage}/{HEAP_SIZE} cells used ({old_usage/HEAP_SIZE*100:.1f}%)")
    print(f"  After: {new_usage}/{HEAP_SIZE} cells used ({new_usage/HEAP_SIZE*100:.1f}%)")
    print(f"  Freed: {old_usage - new_usage} cells")
    print(f"  Time: {gc_stats['last_run_time_ms']:.2f}ms")
    
    stats = get_gc_stats()
    
    # Show additional memory information
    print(f"\nGC Status:")
    print(f"  Total collections:   {stats['collections']}")
    print(f"  Emergency collections: {stats['emergency_collections']}")
    print(f"  Heap expansions:     {stats['heap_expansions']}")
    print(f"  High water mark:     {stats['high_water_mark']} cells ({stats['high_water_percentage']:.1f}%)")
    print(f"  Average GC time:     {stats['avg_gc_time_ms']:.2f}ms")
    print(f"  Recent GC time:      {stats['recent_avg_time_ms']:.2f}ms")
    
    return stats

def set_gc_config(enable=None, threshold=None, debug=None):
    """Configure garbage collection parameters."""
    global ENABLE_GC, GC_THRESHOLD, DEBUG_GC
    
    if enable is not None:
        ENABLE_GC = bool(enable)
    
    if threshold is not None:
        if threshold <= 0 or threshold >= 1.0:
            raise ValueError("GC threshold must be between 0 and 1.0")
        GC_THRESHOLD = HEAP_SIZE * threshold
    
    if debug is not None:
        DEBUG_GC = bool(debug)
    
    return {
        "enable": ENABLE_GC,
        "threshold": GC_THRESHOLD / HEAP_SIZE,
        "debug": DEBUG_GC
    }

def generational_gc():
    """
    Run generational garbage collection, focusing on younger objects.
    This is more efficient for frequent collections since older objects
    tend to survive longer.
    """
    if not ENABLE_GC:
        return
    
    global free, gc_stats
    start_time = time.time()
    
    if DEBUG_GC:
        print(f"GC: Starting generational collection. Heap usage: {free[0]}/{HEAP_SIZE}")
    
    # Only mark gen 0-1 for collection, assume older objects (gen 2-3) are stable
    # Reset all marks first
    gc_mark.fill(0)
    
    # Mark phase: First mark all objects as reachable (default keeper status)
    for i in range(free[0]):
        if gc_generations[i] >= 2:  # Mark older objects immediately
            gc_mark[i] = 1
    
    # Then mark roots and their children
    for i in range(top[0]):
        for j in range(1, 6):
            idx = stack_get(i, j)
            if idx > 0 and idx < free[0]:
                gc_mark_noun(idx)
    
    # Rest of GC proceeds as normal
    new_indices = pim.Tensor(HEAP_SIZE, dtype=pim.int32)
    new_indices.fill(0)
    
    new_free_idx = 0
    for i in range(free[0]):
        if gc_mark[i] == 1:
            new_indices[i] = new_free_idx
            new_free_idx += 1
    
    # Now remap all references and compact the heap
    compact_heap = pim.Tensor(HEAP_SIZE, 3, dtype=pim.int32)
    compact_heap.fill(0)
    
    # Also track generations for the compacted heap
    new_generations = pim.Tensor(HEAP_SIZE, dtype=pim.int32)
    new_generations.fill(0)
    
    # Copy marked cells to their new positions
    for i in range(free[0]):
        if gc_mark[i] == 1:
            new_idx = new_indices[i]
            compact_heap[new_idx * 3] = heap_get(i, 0)  # tag
            
            if is_cell(i):
                # Update head/tail references to their new locations
                head_idx = heap_get(i, 1)
                tail_idx = heap_get(i, 2)
                if head_idx < free[0] and gc_mark[head_idx] == 1:
                    compact_heap[new_idx * 3 + 1] = new_indices[head_idx]
                if tail_idx < free[0] and gc_mark[tail_idx] == 1:
                    compact_heap[new_idx * 3 + 2] = new_indices[tail_idx]
            else:
                # For atoms, just copy the value
                compact_heap[new_idx * 3 + 1] = heap_get(i, 1)
            
            # Copy the generation information
            new_generations[new_idx] = gc_generations[i]
    
    # Update statistics
    cells_freed = free[0] - new_free_idx
    free[0] = new_free_idx
    
    # Copy back to the main heap
    for i in range(free[0]):
        for j in range(3):
            heap[i * 3 + j] = compact_heap[i * 3 + j]
        gc_generations[i] = new_generations[i]
    
    collection_time_ms = (time.time() - start_time) * 1000
    gc_stats["collections"] += 1
    gc_stats["freed_cells"] += cells_freed
    gc_stats["last_run_time_ms"] = collection_time_ms
    gc_stats["total_time_ms"] += collection_time_ms
    
    if DEBUG_GC:
        print(f"GC: Generational collection completed. Freed {cells_freed} cells.")
        print(f"GC: Time taken: {collection_time_ms:.2f}ms")
    
    return cells_freed

def nock_interpreter(subject_idx, formula_idx):
    """Evaluate Nock expression *[subject formula], return result index."""
    result_idx = allocate_cell(0, 0)
    push(0, subject_idx, formula_idx, result_idx)
    
    # Track interpreter performance
    interpret_start_time = time.time()
    gc_time = 0
    operations_count = 0
    
    # Main interpreter loop
    while top[0] > 0:
        task_type, arg1, arg2, arg3, arg4, arg5 = pop()
        operations_count += 1
        
        # Adaptive GC strategy:
        # 1. Use generational GC for smaller, frequent collections
        # 2. Use full GC when heap is getting fuller
        # 3. Use emergency GC with potential heap expansion when nearly full
        
        # Light generational GC for quick cleanup
        if ENABLE_GC and operations_count % 1000 == 0 and free[0] >= int(HEAP_SIZE * 0.4):
            gc_start = time.time()
            generational_gc()
            gc_time += (time.time() - gc_start)
        
        # Regular GC for moderate cleanup
        elif ENABLE_GC and free[0] >= int(GC_THRESHOLD):
            gc_start = time.time()
            gc_collect()
            gc_time += (time.time() - gc_start)
        
        # Emergency GC for when heap is nearly full
        elif ENABLE_GC and free[0] >= int(GC_EMERGENCY_THRESHOLD):
            gc_start = time.time()
            gc_collect(emergency=True)
            gc_time += (time.time() - gc_start)
        
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