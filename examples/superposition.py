"""Superposicao uniforme: H em cada qubit produz (|00>+|01>+|10>+|11>)/2.

Os 4 estados devem aparecer com frequencias aproximadamente iguais (~25%).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator
from visualizer.plotter import ResultsPlotter


def main() -> None:
    circuit = QuantumCircuit(2)
    circuit.hadamard(0).hadamard(1)

    print(f"Circuito: {circuit}")
    print(f"Estado:   {circuit.get_state_vector()}\n")

    results = QuantumSimulator.run(circuit, shots=1000)
    for state in sorted(results.keys()):
        print(f"  |{state}>: {results[state]}")

    ResultsPlotter.plot_results(
        results, title="Superposicao Uniforme 2 Qubits (1000 shots)", output_path="superposition.png"
    )
    print("\nGrafico salvo em superposition.png")


if __name__ == "__main__":
    main()
