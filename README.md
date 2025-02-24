## nocktensors

### emulated processing-in-memory stack-based Nock interpreter using tensor operations

##### Requirements:

- nvcc
- gcc10

(both of these are for the [PyPIM](https://github.com/oleitersdorf/PyPIM) dependency)

##### Installation

- `git clone https://github.com/Native-Planet/nocktensors`
- `cd nocktensors && git submodule update --remote PyPIM`
- `sudo python3 setup.py install`