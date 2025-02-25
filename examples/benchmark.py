import timeit
from nocktensors.interface import nock

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

if __name__ == "__main__":
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