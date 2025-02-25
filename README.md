![image](https://github.com/user-attachments/assets/dd851d45-608f-4be1-bf95-36177088a0b1)

## nocktensors

### emulated processing-in-memory stack-based Nock interpreter using tensor operations

see [this paper](https://arxiv.org/html/2308.14007v2) for an explanation of the pypim framework; tldr we use it to emulate a memristor isa with cuda to work with [nouns](https://docs.urbit.org/courses/hoon-school/B-syntax#nouns) represented as tensors and create a stack-based interpreter for [nock](https://docs.urbit.org/language/nock/reference/definition), a minimal turing-complete functional combinator, with bitwise operations in VRAM. this is just for fun!

##### Requirements:

- nvcc
- gcc10

(both of these are for the [PyPIM](https://github.com/oleitersdorf/PyPIM) dependency)

##### Installation

- `git clone https://github.com/Native-Planet/nocktensors`
- `cd nocktensors && git submodule update --remote PyPIM`
- `pip3 install -e . --user`
- `python3 -m unittest discover tests`
- `python3 examples/demo.py`
