from nocktensors.interface import nock, print_noun
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

def benchmark_constant_0():
    subject = [0, 0]
    formula = 0
    return nock(subject, formula)

def benchmark_constant_1():
    subject = [0, 0]
    formula = 1
    return nock(subject, formula)

def benchmark_increment_5():
    subject = [0, 0]
    formula = [4, 5]
    return nock(subject, formula)

def benchmark_op9_invoke_slot1_subject_0_1():
    subject = [0, [0, 1]]
    formula = [9, 2, [0, 1]]
    return nock(subject, formula)

def run_benchmark_timed(benchmark_func, num_runs=10):
    """Run a benchmark function multiple times and measure average time."""
    times = timeit.repeat(benchmark_func, repeat=num_runs, number=1) # number=1 means run once per repeat
    average_time = min(times) / 1.0
    return average_time

def demo_all():
    print(" ███▄    █  ▒█████   ▄████▄   ██ ▄█▀▄▄▄█████▓▓█████  ███▄    █   ██████  ▒█████   ██▀███    ██████\n██ ▀█   █ ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓  ██▒ ▓▒▓█   ▀  ██ ▀█   █ ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▒██    ▒ \n▓██  ▀█ ██▒▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒ ▓██░ ▒░▒███   ▓██  ▀█ ██▒░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒░ ▓██▄   \n▓██▒  ▐▌██▒▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ░ ▓██▓ ░ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒▒██   ██░▒██▀▀█▄    ▒   ██▒\n▒██░   ▓██░░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄  ▒██▒ ░ ░▒████▒▒██░   ▓██░▒██████▒▒░ ████▓▒░░██▓ ▒██▒▒██████▒▒\n░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒  ▒ ░░   ░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░\n░ ░░   ░ ▒░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░    ░     ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒  ░ ░\n░   ░ ░ ░ ░ ░ ▒  ░        ░ ░░ ░   ░         ░      ░   ░ ░ ░  ░  ░  ░ ░ ░ ▒    ░░   ░ ░  ░  ░  \n░     ░ ░  ░ ░      ░  ░               ░  ░         ░       ░      ░ ░     ░           ░  \n░")
    print("=" * 40)
    demo_op0_slot()
    demo_op1_constant()
    demo_op2_compose()
    demo_op3_is_cell()
    demo_op4_increment()
    benchmarks = [
        benchmark_constant_0,
        benchmark_constant_1,
        benchmark_increment_5,
        benchmark_op9_invoke_slot1_subject_0_1,
    ]

    print("Benchmarking Nock Interpreter:")
    for benchmark_func in benchmarks:
        benchmark_name = benchmark_func.__name__
        average_time_seconds = run_benchmark_timed(benchmark_func)
        average_time_ms = average_time_seconds * 1000
        print(f"  {benchmark_name}: {average_time_ms:.4f} ms")

def main():
    demo_all()

if __name__ == "__main__":
    main()
