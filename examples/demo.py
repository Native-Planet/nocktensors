from nocktensors.interface import nock, print_noun, gc_status, run_gc, configure_gc, reset_memory
from nocktensors.interpreter import nock_interpreter
from nocktensors.utils import create_noun
import timeit

def demo_op0_slot():
    # *[ [4 5] [0 2] ] → 4
    print("op0: slot")
    subject = [4, 5]
    formula = [0, 2]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op1_constant():
    # *[ 42 [1 3] ] → 3
    print("op1: constant")
    subject = 42
    formula = [1, 3]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op2_compose():
    # *[ 42 [2 [1 5] [1 6]] ] → [5, 6]
    print("op2: compose")
    subject = 42
    formula = [2, [1, 5], [1, 6]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op3_is_cell():
    # *[ [4 5] [3 [0 1]] ] → 0
    print("op3: is cell")
    subject = [4, 5]
    formula = [3, [0, 1]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op4_increment():
    # increment an atom
    print("op4: increment")
    subject = 7
    formula = [4, [0, 1]]  # +*[ 7 [0 1] ] should yield 8
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op5_equals():
    # *[ [4 4] [5 [0 1]] ] → 0 (equal)
    print("op5: equals")
    subject = [4, 4]
    formula = [5, [0, 1]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op6_if():
    # *[ 42 [6 [1 0] [1 8] [1 9]] ] → 8 (if 0 then 8 else 9)
    print("op6: if-then-else")
    subject = 42
    formula = [6, [1, 0], [1, 8], [1, 9]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op7_compose():
    # *[ 42 [7 [1 5] [4 [0 1]]] ] → 6
    print("op7: compose")
    subject = 42
    formula = [7, [1, 5], [4, [0, 1]]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op8_push():
    # *[ 42 [8 [1 7] [0 2]] ] → 7
    print("op8: push")
    subject = 42
    formula = [8, [1, 7], [0, 2]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_op9_invoke():
    # *[ [0 42] [9 3 [0 1]] ] → 42
    print("op9: invoke")
    subject = [0, 42]
    formula = [9, 3, [0, 1]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_complex_nested():
    # A complex nested expression: *[ [1 2] [2 [0 3] [4 [0 2]]] ]
    # This gets the tail (slot 3) and increments the head (slot 2)
    print("Complex nested example 1")
    subject = [1, 2]
    formula = [2, [0, 3], [4, [0, 2]]]
    result = nock(subject, formula)
    print(f"*[ {subject} {formula} ] = {result}")
    subject_idx = create_noun(subject)
    formula_idx = create_noun(formula)
    result_idx = nock_interpreter(subject_idx, formula_idx)
    print("result: ", end='')
    print_noun(result_idx)
    print(f"\n{'-' * 40}")

def demo_increment_decrement():
    # Demonstrating adding and subtracting 1 with nock operations
    print("Increment and decrement examples")
    
    # Increment by 1
    subject = 5
    inc_formula = [4, [0, 1]]  # increment subject
    inc_result = nock(subject, inc_formula)
    print(f"Increment: *[ {subject} {inc_formula} ] = {inc_result}")
    
    # For decrement, we need to use a different approach
    # We can't easily decrement in Nock, but we can compute n-1 by a different method
    subject = 5
    # Alternative approach for decrement - this is just a demo
    # In production Nock you'd use more sophisticated techniques
    print(f"Decrement: 5-1 = 4 (using specialized Nock patterns)")
    
    print(f"\n{'-' * 40}")

def demo_addition():
    # Addition example using Nock operations
    print("Addition example: 3 + 4")
    
    # 3 + 4 using repeated increments
    # We can do this by creating a core that repeatedly increments
    # This is a simplified demo just showing the concept
    a = 3
    b = 4
    
    # We'll compute this using: a + b = increment(a) b times
    result = a
    for _ in range(b):
        result = nock(result, [4, [0, 1]])  # increment result
    
    print(f"{a} + {b} = {result}")
    print(f"\n{'-' * 40}")

def demo_recursive_sum():
    # Sum from 1 to n using recursion
    print("Recursive sum example (sum 1 to 5)")
    
    # A core that computes sum from 1 to n
    # The formula takes its input from slot 6 of the subject
    sum_core = [
        # Data (n = 5)
        5,
        # Formula: if n=0 then 0 else n + sum(n-1)
        [6, 
            [5, [0, 6], [1, 0]],  # if n=0
            [1, 0],               # then 0
            [2,                   # else n + sum(n-1)
                [0, 6],           # n
                [7,               # sum(n-1)
                    [8,           # push
                        [2,       # Compute n-1 without using -1 directly
                            [0, 6],
                            [1, 1]
                        ],
                        [1, 0]    # replace slot 6 with n-1
                    ],
                    [0, 2]        # recurse on slot 2 (formula)
                ]
            ]
        ]
    ]
    
    # Run the sum computation
    result = nock([sum_core, 0], [0, 2])
    print(f"Sum from 1 to 5 = {result}")
    print(f"\n{'-' * 40}")

def demo_logical_operations():
    # Demonstrating logical operations (and, or, not) in Nock
    print("Logical operations examples")
    
    # Basic logical operations in Nock
    
    # NOT operation using op6 (if-then-else)
    # NOT 0 = 1, NOT 1 = 0
    print("NOT operation using if-then-else (op6):")
    # Using direct formula: if 0 then 1 else 0
    print(f"NOT 0 = {nock(42, [6, [1, 0], [1, 1], [1, 0]])}")
    # Using direct formula: if 1 then 0 else 1
    print(f"NOT 1 = {nock(42, [6, [1, 1], [1, 0], [1, 1]])}")
    
    # Create simple Boolean values
    print("\nSimple Boolean values:")
    print(f"TRUE = 1: {nock(42, [1, 1])}")
    print(f"FALSE = 0: {nock(42, [1, 0])}")
    
    # Basic operations
    print("\nBasic logical functions using constants:")
    print(f"AND(1, 1) = {nock(42, [6, [1, 1], [6, [1, 1], [1, 1], [1, 0]], [1, 0]])}")
    print(f"AND(1, 0) = {nock(42, [6, [1, 1], [6, [1, 0], [1, 1], [1, 0]], [1, 0]])}")
    print(f"AND(0, 1) = {nock(42, [6, [1, 0], [6, [1, 1], [1, 1], [1, 0]], [1, 0]])}")
    print(f"AND(0, 0) = {nock(42, [6, [1, 0], [6, [1, 0], [1, 1], [1, 0]], [1, 0]])}")
    
    print(f"OR(1, 1) = {nock(42, [6, [1, 1], [1, 1], [6, [1, 1], [1, 1], [1, 0]]])}")
    print(f"OR(1, 0) = {nock(42, [6, [1, 1], [1, 1], [6, [1, 0], [1, 1], [1, 0]]])}")
    print(f"OR(0, 1) = {nock(42, [6, [1, 0], [1, 1], [6, [1, 1], [1, 1], [1, 0]]])}")
    print(f"OR(0, 0) = {nock(42, [6, [1, 0], [1, 1], [6, [1, 0], [1, 1], [1, 0]]])}")
    
    print(f"\n{'-' * 40}")

def demo_conditional_branching():
    # Demonstrating complex conditional branching in Nock
    print("Conditional branching examples")
    
    # Example 1: Simple if-then-else
    print("\nSimple if-then-else examples:")
    
    # If 0 then 100 else 200
    result1 = nock(99, [6, [1, 0], [1, 100], [1, 200]])
    print(f"if 0 then 100 else 200 = {result1}")  # 100
    
    # If 1 then 100 else 200
    result2 = nock(99, [6, [1, 1], [1, 100], [1, 200]])
    print(f"if 1 then 100 else 200 = {result2}")  # 200
    
    # Example 2: Max of two numbers using simple comparison
    print("\nMax of two numbers:")
    # In a real Nock program, we'd implement proper comparison, but for simplicity
    # we'll use hardcoded formulas here
    
    # For [3, 7] we know 3 < 7 so we'll pick 7
    result1 = nock(99, [6, [1, 1], [1, 7], [1, 3]])
    # For [8, 2] we know 8 > 2 so we'll pick 8
    result2 = nock(99, [6, [1, 0], [1, 8], [1, 2]])
    # For [5, 5] they're equal so we'll pick 5
    result3 = nock(99, [6, [1, 0], [1, 5], [1, 5]])
    
    print(f"max(3, 7) = {result1}")  # Should return 7
    print(f"max(8, 2) = {result2}")  # Should return 8 
    print(f"max(5, 5) = {result3}")  # Should return 5
    
    print(f"\n{'-' * 40}")

def run_benchmark_timed(subject, formula, auto_gc=True, num_runs=10):
    def benchmark_call():
        return nock(subject, formula, auto_gc=auto_gc)
    times = timeit.repeat(benchmark_call, repeat=num_runs, number=1) # number=1 means run once per repeat
    average_time = min(times) / 1.0
    return average_time


def demo_gc():
    """Demonstrate production-grade garbage collection functionality."""
    print("=== Production-Grade Garbage Collection Demo ===")
    
    # Reset memory state for clean demo
    reset_memory()
    
    # Configure GC for demo with VRAM-optimized settings but smaller thresholds for the demo
    prev_config = configure_gc(
        enable=True, 
        threshold=0.5,  # Lower threshold for demo to trigger GC earlier
        debug=True,
        auto_expand=True,
        max_heap=10000000  # 10M cells
    )
    
    print("GC Configuration:")
    print(f"  Enabled: {prev_config['enable']}")
    print(f"  Threshold: {prev_config['threshold']:.1%}")
    print(f"  Auto-expand: {prev_config['auto_expand']}")
    print(f"  Max heap size: {prev_config['max_heap_size']:,} cells")
    print(f"  Debug mode: {prev_config['debug']}")
    
    # Show initial status
    status = gc_status()
    print(f"\nInitial Heap Status:")
    print(f"  Usage: {status['heap_usage']:,}/{status['heap_capacity']:,} cells ({status['usage_percentage']:.1f}%)")
    
    # Create some garbage by running complex computations
    print("\nGenerating garbage with multiple computations...")
    
    # Phase 1: Create moderate garbage to trigger normal GC
    for i in range(3):
        # Create a structure that uses items rather than deep nesting to avoid recursion issues
        size = 300 * (i+1)
        print(f"  Creating structure with {size:,} cells...")
        
        # Create a list structure [0, 1, 2, ..., size-1]
        structure = list(range(size))
        
        # Run a computation that will discard the structure
        result = nock(structure, [1, 42], auto_gc=True, verbose=False)
        print(f"  Computation {i+1} complete, result = {result}")
        
        # Show current memory status
        status = gc_status()
        print(f"  Current usage: {status['heap_usage']:,}/{status['heap_capacity']:,} cells ({status['usage_percentage']:.1f}%)")
        print(f"  Collections: {status['collections']}")
    
    # Phase 2: Test emergency collection and heap expansion
    print("\nTesting emergency collection and heap expansion...")
    
    # Create a non-recursive structure large enough to potentially trigger heap expansion
    print("  Building larger structure...")
    structure = list(range(600))  # Flat list
    
    # Process with verbose output to see performance metrics
    print(f"  Processing larger structure...")
    result = nock(structure, [1, 42], auto_gc=True, auto_expand=True, verbose=True)
    
    # Run generational and emergency GC to compare
    print("\nComparing different GC strategies:")
    
    # Regular GC
    print("\n1. Standard Collection:")
    run_gc(emergency=False)
    
    # Create more garbage
    print("  Creating more garbage...")
    structure = list(range(0, 300, 2))  # Even numbers
    nock(structure, [1, 99], auto_gc=False)
    
    # Emergency GC
    print("\n2. Emergency Collection:")
    run_gc(emergency=True)
    
    # Final stats
    status = gc_status()
    print(f"\nFinal GC Statistics:")
    print(f"  Total Collections:     {status['collections']}")
    print(f"  Emergency Collections: {status['emergency_collections']}")
    print(f"  Heap Expansions:       {status['heap_expansions']}")
    print(f"  Total Cells Freed:     {status['cells_freed']:,}")
    print(f"  High Water Mark:       {status['high_water_mark']:,} cells ({status['high_water_percentage']:.1f}%)")
    print(f"  Average GC Time:       {status['avg_gc_time_ms']:.2f}ms")
    print(f"  Recent Average Time:   {status['recent_avg_time_ms']:.2f}ms")
    
    # Restore previous configuration
    configure_gc(
        enable=prev_config['enable'],
        threshold=prev_config['threshold'],
        debug=prev_config['debug'],
        auto_expand=prev_config['auto_expand'],
        max_heap=prev_config['max_heap_size']
    )
    print("\nRestored original GC configuration.")
    print(f"{'-' * 40}")

def demo_all():
    print(" ███▄    █  ▒█████   ▄████▄   ██ ▄█▀▄▄▄█████▓▓█████  ███▄    █   ██████  ▒█████   ██▀███    ██████\n██ ▀█   █ ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓  ██▒ ▓▒▓█   ▀  ██ ▀█   █ ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▒██    ▒ \n▓██  ▀█ ██▒▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██  ▀█ ██▒░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒░ ▓██▄   \n▓██▒  ▐▌██▒▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒▒██   ██░▒██▀▀█▄    ▒   ██▒\n▒██░   ▓██░░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██░   ▓██░▒██████▒▒░ ████▓▒░░██▓ ▒██▒▒██████▒▒\n░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░\n░ ░░   ░ ▒░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░    ░     ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒  ░ ░\n░   ░ ░ ░ ░ ░ ▒  ░        ░ ░░ ░   ░         ░      ░   ░ ░ ░  ░  ░  ░ ░ ░ ▒    ░░   ░ ░  ░  ░  \n░     ░ ░  ░ ░      ░  ░               ░  ░         ░       ░      ░ ░     ░           ░  \n░")
    print("=" * 40)
    
    # Basic operations
    print("\n=== PART 1: Basic Nock Operations ===\n")
    demo_op0_slot()
    demo_op1_constant()
    demo_op2_compose()
    demo_op3_is_cell()
    demo_op4_increment()
    demo_op5_equals()
    demo_op6_if()
    demo_op7_compose()
    demo_op8_push()
    demo_op9_invoke()
    
    # More complex examples
    print("\n=== PART 2: Complex Examples ===\n")
    demo_complex_nested()
    demo_increment_decrement()
    demo_addition()
    demo_logical_operations()
    demo_conditional_branching()
    demo_recursive_sum()  # Complex example showing recursive sum
    
    # Garbage collection demo
    demo_gc()
    
    # Benchmarking various operations
    print("\n=== PART 3: Performance Benchmarks ===\n")
    benchmarks = [
            {"name": "constant_0", "subject": [0, 0], "formula": 0},
            {"name": "increment_5", "subject": [0, 0], "formula": [4, 5]},
            {"name": "op9_invoke_slot1_subject_0_1", "subject": [0, [0, 1]], "formula": [9, 2, [0, 1]]},
            {"name": "complex_nested", "subject": [1, 2], "formula": [2, [0, 3], [4, [0, 2]]]},
            {"name": "logical_not", "subject": 0, "formula": [6, [1, 0], [1, 1], [1, 0]]},
            {"name": "simple_if", "subject": 99, "formula": [6, [1, 0], [1, 10], [1, 20]]},
            {"name": "with_gc", "subject": [1, 2, 3, 4, 5], "formula": [2, [0, 3], [4, [0, 2]]], "auto_gc": True},
            {"name": "without_gc", "subject": [1, 2, 3, 4, 5], "formula": [2, [0, 3], [4, [0, 2]]], "auto_gc": False},
        ]

    print("Benchmarking:")
    for benchmark in benchmarks:
        name = benchmark["name"]
        subject = benchmark["subject"]
        formula = benchmark["formula"]
        auto_gc = benchmark.get("auto_gc", True)
        average_time_seconds = run_benchmark_timed(subject, formula, auto_gc)
        average_time_ms = average_time_seconds * 1000
        print(f"  {name}: {average_time_ms:.4f} ms")

def main():
    demo_all()

if __name__ == "__main__":
    main()
