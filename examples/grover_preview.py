"""Preview do algoritmo de Grover (esboco para v3.0).

Este exemplo executa apenas a parte de inicializacao (superposicao uniforme).
A iteracao de Grover (oraculo + difusor) sera implementada na v3.0, quando
matrizes multi-qubit arbitrarias estiverem disponiveis no circuito.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator


def main() -> None:
    n = 2
    circuit = QuantumCircuit(n)
    for i in range(n):
        circuit.hadamard(i)

    print("Estado inicial de Grover (superposicao uniforme):")
    print(f"  {circuit.get_state_vector()}\n")

    print("Distribuicao apos medir 500 shots:")
    results = QuantumSimulator.run(circuit, shots=500)
    for state in sorted(results.keys()):
        print(f"  |{state}>: {results[state]}")

    print("\n[TODO v3.0] Implementar oraculo + difusor para amplificar o estado alvo.")


if __name__ == "__main__":
    main()
