
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
<!--- [![Bindings](https://img.shields.io/github/workflow/status/cda-tum/ddsim/Deploy%20to%20PyPI?style=flat-square&logo=github&label=python)]()
 [![Documentation](https://img.shields.io/readthedocs/ddsim?logo=readthedocs&style=flat-square)]() 
 [![codecov](https://img.shields.io/codecov/c/github/cda-tum/)]() -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/qmap/main/docs/source/_static/mqt_light.png" width="60%">
    <img src="https://raw.githubusercontent.com/cda-tum/qmap/main/docs/source/_static/mqt_dark.png" width="60%">
  </picture>
</p>

# MQT Qudits - Adaptive Compilation of Multi-Level Quantum Operations

A tool for the compilation of arbitrary d-dimensional single qudit unitaries into error-efficient sequences of two-level operations by [Chair for Design Automation](https://www.cda.cit.tum.de/).


If you have any questions, feel free to contact us via [quantum.cda@xcit.tum.de](mailto:iic-quantum@jku.at) or by creating an [issue](https://github.com/cda-tum/qudit-compilation/issues) on GitHub.

## Getting Started

The compiler demands only for the resolution of dependencies, to solve run in terminal.
```
pip install -r requirements.txt
```
In order to proceed just import the main class 'QuantumCircuit' in the QuantumCircuit folder.


The following code gives an example on the usage:

```python3
from src.architecture_graph.level_Graph import level_Graph
from src.evaluation.Pauli import H
from src.circuit.QuantumCircuit import QuantumCircuit



dimension = 3 # select dimension of your single qudit .


# declare the edges on the energy level graph between logic states .
edges = [
        (1, 0, {"delta_m": 0, "sensitivity": 3}),
        (0, 2, {"delta_m": 0, "sensitivity": 3}),
        ]
        
# name explicitly the logic states .
nodes = [0, 1, 2]

# declare physical levels in order of maping of the logic states just declared .
# i.e. here we will have Logic 0 -> Phys. 0, have Logic 1 -> Phys. 1, have Logic 2 -> Phys. 2 .

nmap = [0, 1, 2]

# Construct the qudit energy level graph, the last field is the list of logic state that are used for the calibrations of the operations.
# note: only the first is one counts in our current cost fucntion.

graph = level_Graph(edges, nodes, nmap, [1])


# Construct quantum circuit with 1 qudit, 0 classical bit, dimension of the qudit, graph of the qudit, flag for compile with verification .
QC = QuantumCircuit(1, 0, dimension, graph, verify = True)


# add custom gate to qudit 0, the matrix field is a nump array .
QC.custom_unitary(0, H(dimension).matrix)

# Visualize initial circuit .
QC.draw()

# Compile .
QC.DFS_decompose()

# alternative : QR_decompose()

# Propagate Z gates backwards .
QC.Z_prop(back = True)

# Visualize the results
QC.draw()

# Save the results to json .
path = "./"
QC.to_json(path)



# NOTE: for customizing the cost functions access file ./src/utils/cost_functions.py

```

## System Requirements and Building

The implementation is compatible with a minimimum version of Python 3.8.

Building (and running) is continuously tested under Linux, macOS, and Windows using the [latest available system versions for GitHub Actions](https://github.com/actions/virtual-environments).

## References

K. Mato, M. Ringbauer, S. Hillmich and R. Wille, "[Adaptive Compilation of Multi-Level Quantum Operations](https://www.cda.cit.tum.de/files/eda/2022_qce_adaptive_compilation_of_multi_level_quantum_operations.pdf)," 2022 IEEE International Conference on Quantum Computing and Engineering (QCE), Broomfield, CO, USA, 2022, pp. 484-491, doi: 10.1109/QCE53715.2022.00070.
