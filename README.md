## nocktensors

### emulated processing-in-memory stack-based Nock interpreter using tensor operations

see [this paper](https://arxiv.org/html/2308.14007v2) for an explanation of the pypim framework; tldr we use it to emulate a memristor isa with cuda to work with nouns as tensors built with bitwise operations. this is just for fun

##### Requirements:

- nvcc
- gcc10

(both of these are for the [PyPIM](https://github.com/oleitersdorf/PyPIM) dependency)

##### Installation

- `git clone https://github.com/Native-Planet/nocktensors`
- `cd nocktensors && git submodule update --remote PyPIM`
- `sudo python3 setup.py install`