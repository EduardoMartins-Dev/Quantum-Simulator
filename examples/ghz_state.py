"""GHZ State: emaranhamento entre 3 qubits.

H(q0) -> CNOT(0,1) -> CNOT(1,2) produz |GHZ> = (|000>+|111>)/sqrt(2).
A medicao deve render apenas '000' ou '111'.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator
from visualizer.plotter import ResultsPlotter


def main() -> None:
    circuit = QuantumCircuit(3)
    circuit.hadamard(0).cnot(0, 1).cnot(1, 2)

    print(f"Circuito: {circuit}")
    print(f"Estado:   {circuit.get_state_vector()}\n")

    results = QuantumSimulator.run(circuit, shots=1000)
    for state in sorted(results.keys()):
        print(f"  |{state}>: {results[state]}")

    ResultsPlotter.plot_results(results, title="GHZ State (1000 shots)", output_path="ghz_state.png")
    print("\nGrafico salvo em ghz_state.png")


if __name__ == "__main__":
    main()
