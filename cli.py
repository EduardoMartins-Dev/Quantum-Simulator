import argparse
import sys

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator
from visualizer.plotter import ResultsPlotter


def create_bell_state() -> QuantumCircuit:
    """Bell State |Phi+> = (|00> + |11>) / sqrt(2)."""
    circuit = QuantumCircuit(2)
    circuit.hadamard(0)
    circuit.cnot(0, 1)
    return circuit


def create_ghz_state() -> QuantumCircuit:
    """GHZ State (3 qubits emaranhados): (|000> + |111>) / sqrt(2)."""
    circuit = QuantumCircuit(3)
    circuit.hadamard(0)
    circuit.cnot(0, 1)
    circuit.cnot(1, 2)
    return circuit


def create_superposition() -> QuantumCircuit:
    """Superposicao completa em 2 qubits via H em cada um."""
    circuit = QuantumCircuit(2)
    circuit.hadamard(0)
    circuit.hadamard(1)
    return circuit


EXAMPLES = {
    "bell": create_bell_state,
    "ghz": create_ghz_state,
    "super": create_superposition,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Quantum Circuit Simulator MVP")
    parser.add_argument("--qubits", type=int, default=2, help="Numero de qubits (circuito padrao)")
    parser.add_argument("--shots", type=int, default=1000, help="Numero de execucoes")
    parser.add_argument(
        "--example",
        type=str,
        choices=sorted(EXAMPLES.keys()),
        help="Executar um exemplo pronto (bell, ghz, super)",
    )
    parser.add_argument("--output", type=str, default="quantum_results.png", help="PNG de saida")
    parser.add_argument("--no-plot", action="store_true", help="Nao gerar grafico")

    args = parser.parse_args()

    if args.example:
        circuit = EXAMPLES[args.example]()
    else:
        if args.qubits < 2:
            print("Aviso: circuito padrao requer >=2 qubits para o CNOT.", file=sys.stderr)
            return 2
        circuit = QuantumCircuit(args.qubits)
        circuit.hadamard(0)
        circuit.cnot(0, 1)

    print(f"Circuito: {circuit}")
    print(f"Estado:   {circuit.get_state_vector()}\n")

    results = QuantumSimulator.run(circuit, shots=args.shots)
    probs = QuantumSimulator.get_probabilities(results)

    print(f"Resultados ({args.shots} shots):")
    for state in sorted(results.keys()):
        count = results[state]
        print(f"  |{state}>: {count:5d} ({probs[state] * 100:5.1f}%)")

    if not args.no_plot:
        path = ResultsPlotter.plot_results(
            results,
            title=f"Quantum Circuit ({args.shots} shots)",
            output_path=args.output,
        )
        print(f"\nGrafico salvo em: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
