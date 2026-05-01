from typing import Dict, List, Tuple, Any

from core.circuit import QuantumCircuit


class QuantumSimulator:
    """Executa um circuito quantico multiplas vezes (shots) e agrega resultados."""

    @staticmethod
    def _replay(num_qubits: int, ops: List[Tuple[Any, ...]]) -> QuantumCircuit:
        """Reconstroi o circuito aplicando as operacoes registradas."""
        circuit = QuantumCircuit(num_qubits)
        for op in ops:
            name = op[0]
            args = op[1:]
            if name == "H":
                circuit.hadamard(*args)
            elif name == "X":
                circuit.pauli_x(*args)
            elif name == "Y":
                circuit.pauli_y(*args)
            elif name == "Z":
                circuit.pauli_z(*args)
            elif name == "P":
                circuit.phase(*args)
            elif name == "CNOT":
                circuit.cnot(*args)
            else:
                raise ValueError(f"Operacao desconhecida: {name}")
        return circuit

    @staticmethod
    def run(circuit: QuantumCircuit, shots: int = 1000) -> Dict[str, int]:
        """Executa o circuito `shots` vezes e retorna a contagem de cada medicao."""
        if shots <= 0:
            raise ValueError("shots deve ser > 0")
        ops = list(circuit.operations)
        num_qubits = circuit.num_qubits

        results: Dict[str, int] = {}
        for _ in range(shots):
            fresh = QuantumSimulator._replay(num_qubits, ops)
            measurements = fresh.measure_all()
            bitstring = "".join(map(str, measurements))
            results[bitstring] = results.get(bitstring, 0) + 1
        return results

    @staticmethod
    def get_probabilities(results: Dict[str, int]) -> Dict[str, float]:
        """Converte contagens em probabilidades empiricas."""
        total = sum(results.values()) or 1
        return {k: v / total for k, v in results.items()}
