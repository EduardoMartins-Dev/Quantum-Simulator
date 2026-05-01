import numpy as np
from typing import List, Tuple, Any

from .qubit import Qubit
from .gates import QuantumGates


class QuantumCircuit:
    """Circuito quantico com N qubits.

    Usa um vetor de estado conjunto de dimensao 2^N, que e a forma correta
    de representar estados emaranhados (como o Bell state). A convencao e
    que o qubit 0 corresponde ao bit mais significativo: o indice de base
    `b` representa o estado |q0 q1 ... q_{N-1}> onde q_i = (b >> (N-1-i)) & 1.
    """

    def __init__(self, num_qubits: int):
        if num_qubits < 1:
            raise ValueError("num_qubits deve ser >= 1")
        self.num_qubits = num_qubits
        self.state: np.ndarray = np.zeros(2 ** num_qubits, dtype=complex)
        self.state[0] = 1.0  # |00...0>
        self.qubits: List[Qubit] = [Qubit(0) for _ in range(num_qubits)]
        self.operations: List[Tuple[Any, ...]] = []

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _apply_single_qubit_gate(self, gate: np.ndarray, qubit_idx: int) -> None:
        if not (0 <= qubit_idx < self.num_qubits):
            raise ValueError(f"Indice de qubit {qubit_idx} fora do intervalo")
        op = np.array([[1.0]], dtype=complex)
        identity = np.eye(2, dtype=complex)
        for i in range(self.num_qubits):
            op = np.kron(op, gate if i == qubit_idx else identity)
        self.state = op @ self.state
        # Atualiza a representacao individual (util quando o qubit nao esta emaranhado)
        self.qubits[qubit_idx].apply_gate(gate)

    def _check_index(self, idx: int) -> None:
        if not (0 <= idx < self.num_qubits):
            raise ValueError(f"Indice {idx} fora do intervalo [0, {self.num_qubits - 1}]")

    # ------------------------------------------------------------------
    # Portas de 1 qubit
    # ------------------------------------------------------------------
    def hadamard(self, qubit_idx: int) -> "QuantumCircuit":
        self._apply_single_qubit_gate(QuantumGates.hadamard(), qubit_idx)
        self.operations.append(("H", qubit_idx))
        return self

    def pauli_x(self, qubit_idx: int) -> "QuantumCircuit":
        self._apply_single_qubit_gate(QuantumGates.pauli_x(), qubit_idx)
        self.operations.append(("X", qubit_idx))
        return self

    def pauli_y(self, qubit_idx: int) -> "QuantumCircuit":
        self._apply_single_qubit_gate(QuantumGates.pauli_y(), qubit_idx)
        self.operations.append(("Y", qubit_idx))
        return self

    def pauli_z(self, qubit_idx: int) -> "QuantumCircuit":
        self._apply_single_qubit_gate(QuantumGates.pauli_z(), qubit_idx)
        self.operations.append(("Z", qubit_idx))
        return self

    def phase(self, qubit_idx: int, theta: float) -> "QuantumCircuit":
        self._apply_single_qubit_gate(QuantumGates.phase_gate(theta), qubit_idx)
        self.operations.append(("P", qubit_idx, theta))
        return self

    # ------------------------------------------------------------------
    # CNOT generalizado para N qubits
    # ------------------------------------------------------------------
    def cnot(self, control: int, target: int) -> "QuantumCircuit":
        """Aplica CNOT(control, target). Funciona para N qubits."""
        self._check_index(control)
        self._check_index(target)
        if control == target:
            raise ValueError("control e target devem ser diferentes")

        n = self.num_qubits
        size = 2 ** n
        new_state = np.zeros_like(self.state)
        ctrl_mask = 1 << (n - 1 - control)
        tgt_mask = 1 << (n - 1 - target)
        for basis in range(size):
            if basis & ctrl_mask:
                new_basis = basis ^ tgt_mask
            else:
                new_basis = basis
            new_state[new_basis] += self.state[basis]
        self.state = new_state
        self.operations.append(("CNOT", control, target))
        return self

    # ------------------------------------------------------------------
    # Medicao
    # ------------------------------------------------------------------
    def measure_all(self) -> List[int]:
        """Mede todos os qubits do estado conjunto, colapsando o estado."""
        probs = np.abs(self.state) ** 2
        total = probs.sum()
        if total <= 0:
            raise RuntimeError("Estado com norma zero - circuito invalido")
        probs = probs / total
        outcome = int(np.random.choice(len(probs), p=probs))

        # Decodifica em bits (qubit 0 = bit mais significativo)
        results = [(outcome >> (self.num_qubits - 1 - i)) & 1 for i in range(self.num_qubits)]

        # Colapsa o estado conjunto
        new_state = np.zeros_like(self.state)
        new_state[outcome] = 1.0
        self.state = new_state
        # Sincroniza qubits individuais
        for i, bit in enumerate(results):
            self.qubits[i] = Qubit(bit)
        return results

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def get_state_vector(self) -> str:
        """Representacao textual do estado conjunto em base computacional."""
        n = self.num_qubits
        terms = []
        for basis, amp in enumerate(self.state):
            if abs(amp) < 1e-10:
                continue
            ket = format(basis, f"0{n}b")
            if abs(amp.imag) < 1e-10:
                coef = f"{amp.real:+.3f}"
            else:
                coef = f"({amp.real:+.3f}{amp.imag:+.3f}j)"
            terms.append(f"{coef}|{ket}>")
        return " ".join(terms) if terms else "0"

    def get_probabilities(self) -> dict:
        """Retorna {bitstring: probabilidade} para todos os estados de base."""
        n = self.num_qubits
        probs = np.abs(self.state) ** 2
        total = probs.sum() or 1.0
        probs = probs / total
        return {format(i, f"0{n}b"): float(p) for i, p in enumerate(probs) if p > 1e-12}

    def reset(self) -> "QuantumCircuit":
        """Reseta o circuito para |00...0> e limpa o log de operacoes."""
        self.state = np.zeros(2 ** self.num_qubits, dtype=complex)
        self.state[0] = 1.0
        self.qubits = [Qubit(0) for _ in range(self.num_qubits)]
        self.operations = []
        return self

    def _format_op(self, op: Tuple[Any, ...]) -> str:
        name = op[0]
        if name == "P":
            return f"P({op[1]}, {op[2]:.3f})"
        return f"{name}({', '.join(str(a) for a in op[1:])})"

    def __str__(self) -> str:
        ops = " -> ".join(self._format_op(o) for o in self.operations) if self.operations else "vazio"
        return f"Circuit({self.num_qubits} qubits): {ops}"
