from .interpreter import (
    nock_interpreter, heap, heap_get, heap_set, is_cell, get_head, get_tail, get_value,
    get_gc_stats, manual_gc, set_gc_config, ENABLE_GC, GC_THRESHOLD, DEBUG_GC,
    HEAP_SIZE, AUTO_EXPAND_HEAP, MAX_HEAP_SIZE
)
from .utils import create_noun, print_noun

def nock(subject, formula, auto_gc=True, auto_expand=True, verbose=False):
    """
    Evaluate a Nock expression *[subject formula].
    
    Parameters:
        subject: The subject noun (can be an integer atom or a list for a cell).
        formula: The formula noun (can be an integer atom or a list for a cell).
        auto_gc: Whether to enable automatic garbage collection (default True).
        auto_expand: Whether to enable automatic heap expansion (default True).
        verbose: Whether to print performance information (default False).
    
    Returns:
        The result of the Nock computation, converted to Python representation.
    """
    import time
    start_time = time.time()
    
    # Import these at function level to avoid circular import issues
    from .interpreter import set_gc_config, AUTO_EXPAND_HEAP
    
    # Save the current GC and heap settings
    prev_gc_state = ENABLE_GC
    prev_auto_expand = AUTO_EXPAND_HEAP
    
    # Configure GC and heap expansion
    if prev_gc_state != auto_gc or prev_auto_expand != auto_expand:
        set_gc_config(enable=auto_gc)
        globals()['AUTO_EXPAND_HEAP'] = auto_expand
    
    try:
        # Create the nouns
        subject_creation_start = time.time()
        subject_idx = create_noun(subject)
        subject_creation_time = time.time() - subject_creation_start
        
        formula_creation_start = time.time()
        formula_idx = create_noun(formula)
        formula_creation_time = time.time() - formula_creation_start
        
        # Run the interpreter
        interpret_start = time.time()
        result_idx = nock_interpreter(subject_idx, formula_idx)
        interpret_time = time.time() - interpret_start
        
        # Convert the result back to Python
        conversion_start = time.time()
        result = noun_to_python(result_idx)
        conversion_time = time.time() - conversion_start
        
        total_time = time.time() - start_time
        
        # Print performance information if requested
        if verbose:
            print(f"Performance:")
            print(f"- Subject creation: {subject_creation_time*1000:.2f}ms")
            print(f"- Formula creation: {formula_creation_time*1000:.2f}ms")
            print(f"- Interpretation:   {interpret_time*1000:.2f}ms")
            print(f"- Result conversion: {conversion_time*1000:.2f}ms")
            print(f"- Total time:       {total_time*1000:.2f}ms")
            print(f"- Memory usage:     {get_gc_stats()['heap_usage']} / {get_gc_stats()['heap_capacity']} cells")
        
        return result
    finally:
        # Restore the previous settings
        if prev_gc_state != auto_gc or prev_auto_expand != auto_expand:
            set_gc_config(enable=prev_gc_state)
            AUTO_EXPAND_HEAP = prev_auto_expand

def noun_to_python(idx):
    """
    Convert a heap index back to a Python representation.
    """
    if is_cell(idx):
        return [noun_to_python(get_head(idx)), noun_to_python(get_tail(idx))]
    else:
        return get_value(idx)

def gc_status():
    """Get the current status of the garbage collector."""
    return get_gc_stats()

def run_gc(emergency=False):
    """
    Manually trigger the garbage collector.
    
    Args:
        emergency: If True, perform more aggressive collection
                  and attempt to expand the heap if needed.
    """
    return manual_gc(emergency=emergency)

def configure_gc(enable=None, threshold=None, debug=None, auto_expand=None, max_heap=None):
    """
    Configure garbage collection and heap parameters.
    
    Args:
        enable: Enable or disable garbage collection
        threshold: Set the GC threshold (between 0.0 and 1.0)
        debug: Enable or disable debug logging
        auto_expand: Enable or disable automatic heap expansion
        max_heap: Set the maximum heap size in cells
        
    Returns:
        A dictionary with the current configuration
    """
    global AUTO_EXPAND_HEAP
    
    if auto_expand is not None:
        AUTO_EXPAND_HEAP = bool(auto_expand)
    
    if max_heap is not None:
        from .interpreter import MAX_HEAP_SIZE as interpreter_max_heap
        interpreter_max_heap = int(max_heap)
    
    result = set_gc_config(enable, threshold, debug)
    
    # Add heap configuration to the result
    result.update({
        "auto_expand": AUTO_EXPAND_HEAP,
        "max_heap_size": MAX_HEAP_SIZE
    })
    
    return result

def reset_memory():
    """
    Reset all memory state (heap, stack, GC stats).
    This is useful for testing and benchmarking.
    """
    from .interpreter import free, top, gc_mark, gc_generations, heap, stack, gc_stats
    
    # Reset all tensors
    free[0] = 0
    top[0] = 0
    gc_mark.fill(0)
    gc_generations.fill(0)
    
    # Reset stats
    gc_stats.update({
        "collections": 0,
        "freed_cells": 0,
        "total_time_ms": 0,
        "last_run_time_ms": 0,
        "collection_times": [],
        "collection_freed": [],
        "heap_expansions": 0,
        "emergency_collections": 0,
        "high_water_mark": 0
    })
    
    from .interpreter import HEAP_SIZE, STACK_SIZE
    return {"status": "Memory reset", "heap_size": HEAP_SIZE, "stack_size": STACK_SIZE}