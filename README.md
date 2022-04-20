![OS](https://img.shields.io/badge/os-linux%20%7C%20macos%20%7C%20windows-blue?style=flat-square)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
<!--- [![Bindings](https://img.shields.io/github/workflow/status/cda-tum/ddsim/Deploy%20to%20PyPI?style=flat-square&logo=github&label=python)]()
<!--- [![Documentation](https://img.shields.io/readthedocs/ddsim?logo=readthedocs&style=flat-square)]() 
<!---  [![codecov](https://img.shields.io/codecov/c/github/cda-tum/)]() -->

# MQT Qudits - Adaptive Compilation of Multi-Level Quantum Operations

A tool for the compilation of arbitrary d-dimensional single qudit unitaries into error-efficient sequences of two-level operations by [Chair for Design Automation](https://www.cda.cit.tum.de/).


If you have any questions, feel free to contact us via [quantum.cda@xcit.tum.de](mailto:iic-quantum@jku.at) or by creating an [issue](https://github.com/cda-tum/qudit-compilation/issues) on GitHub.

## Getting Started

The compiler demands only for the resolution of dependencies, to solve run in terminal.
```
python setup.py
```
In order to proceed just import the main class 'QuantumCircuit' in the QuantumCircuit folder.


The following code gives an example on the usage:

```python3
from binq import *
from Pauli import H


dimension = 3


edges = [
        (1, 0, {"delta_m": 0, "sensitivity": 3}),
        (0, 2, {"delta_m": 0, "sensitivity": 3}),
        ]
nodes = [0, 1, 2]
nmap = [0, 1, 2]

graph = level_Graph(edges, nodes, nmap, [1])



QC = binq.QuantumCircuit(1, 0, dimension, graph, verify = True)


QC.custom_unitary(0, H(dimension).matrix)

QC.DFS_decompose()
QC.Z_prop(back = True)

QC.draw()
QC.to_json("path")


```

## System Requirements and Building

The implementation is compatible with a minimimum version of Python 3.8.

Building (and running) is continuously tested under Linux, macOS, and Windows using the [latest available system versions for GitHub Actions](https://github.com/actions/virtual-environments).

## References

No References.
