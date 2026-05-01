"""Bell State: o exemplo classico de emaranhamento.

H aplicado a q0 cria a superposicao (|0>+|1>)/sqrt(2). O CNOT(0,1)
correlaciona q1 com q0, produzindo |Phi+> = (|00>+|11>)/sqrt(2).
Medindo, vemos apenas '00' ou '11' - nunca '01' nem '10'.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator
from visualizer.plotter import ResultsPlotter


def main() -> None:
    circuit = QuantumCircuit(2)
    circuit.hadamard(0).cnot(0, 1)

    print(f"Circuito: {circuit}")
    print(f"Estado:   {circuit.get_state_vector()}\n")

    results = QuantumSimulator.run(circuit, shots=1000)
    for state in sorted(results.keys()):
        print(f"  |{state}>: {results[state]}")

    ResultsPlotter.plot_results(results, title="Bell State (1000 shots)", output_path="bell_state.png")
    print("\nGrafico salvo em bell_state.png")


if __name__ == "__main__":
    main()
