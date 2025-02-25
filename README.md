## nocktensors

### Emulated Processing-in-Memory Stack-Based Nock Interpreter Using Tensor Operations

This project implements [Nock](https://docs.urbit.org/language/nock/reference/definition), a minimal Turing-complete functional combinator, using tensor operations through the PyPIM framework (see [this paper](https://arxiv.org/html/2308.14007v2) for details). In essence, we emulate a memristor instruction set architecture (ISA) with CUDA to work with [nouns](https://docs.urbit.org/courses/hoon-school/B-syntax#nouns) represented as tensors and create a stack-based interpreter with operations executed in VRAM.

This project is primarily for educational and experimental purposes, demonstrating how a functional combinator can be implemented using tensor operations.

### Requirements

- nvcc (NVIDIA CUDA Compiler)
- gcc10

(both of these are for the [PyPIM](https://github.com/oleitersdorf/PyPIM) dependency)

### Installation

```bash
git clone https://github.com/Native-Planet/nocktensors
cd nocktensors && git submodule update --remote PyPIM
pip3 install -e . --user
python3 -m unittest discover tests
python3 examples/demo.py
```

### Architecture

The interpreter is built around three main components:

1. **Heap Memory Manager**: Manages a contiguous block of memory for storing nouns (atoms and cells)
2. **Stack Machine**: Maintains a stack for execution of Nock operations
3. **Operation Handlers**: Implements the 12 core Nock operations (0-11)

The key data structures:
- **Heap Tensor**: A 2D tensor of shape `[HEAP_SIZE, 3]` where each row contains `[tag, value/head, tail]`. Tag is 0 for atoms, 1 for cells.
- **Stack Tensor**: A 2D tensor of shape `[STACK_SIZE, 6]` where each row contains `[task_type, arg1, arg2, arg3, arg4, arg5]`.
- **Free/Top Indices**: Track the next available heap address and the top of the stack.

The interpreter uses a continuation-passing style to avoid recursion depths that could exceed Python's limits, enabling it to handle complex Nock expressions.

### Examples

The demo script demonstrates:
- Basic Nock operations (0-9)
- Complex nested expressions
- Logical operations (AND, OR, NOT)
- Conditional branching
- Recursive computations (like sum of numbers)

### Memory Management

The interpreter now includes a garbage collector to efficiently manage memory. Key features:

- **Mark-and-Sweep Algorithm**: Identifies and reclaims unreachable heap cells
- **Automatic Collection**: Triggered when heap usage exceeds a configurable threshold
- **Manual Control**: Can be triggered manually or disabled for performance testing
- **Statistics Tracking**: Monitors collection frequency, freed cells, and execution time

The GC API provides:
```python
from nocktensors.interface import nock, gc_status, run_gc, configure_gc

# Enable/disable GC during Nock execution
result = nock(subject, formula, auto_gc=True)

# Get current GC status
stats = gc_status() 
print(f"Heap usage: {stats['heap_usage']}/{stats['heap_capacity']} ({stats['usage_percentage']:.1f}%)")
print(f"Collections performed: {stats['collections']}")

# Run GC manually
run_gc()

# Configure GC parameters
configure_gc(enable=True, threshold=0.8, debug=False)
```

### Limitations and Future Work

Current limitations:
- Limited error handling for malformed Nock expressions
- Non-negative integers only (no direct support for negative numbers)
- Relatively simple GC implementation (could be optimized further)
- Limited optimization for tensor operations 

Potential improvements:
- JIT compilation of common Nock patterns
- Incremental or generational garbage collection
- Better error handling and debugging tools
- Optimization of tensor operations for better performance
- Support for running standard Nock/Hoon benchmarks
- Direct integration with Urbit's Vere runtime

### References

- [Nock Specification](https://docs.urbit.org/language/nock/reference/definition)
- [PyPIM Framework](https://github.com/oleitersdorf/PyPIM)
- [Processing-in-Memory Paper](https://arxiv.org/html/2308.14007v2)