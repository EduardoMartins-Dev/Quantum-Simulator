import numpy as np
from typing import Tuple


class Qubit:
    """Representa um qubit isolado com estado vetorial complexo de dimensao 2."""

    def __init__(self, initial_state: int = 0):
        if initial_state not in (0, 1):
            raise ValueError("initial_state deve ser 0 ou 1")
        if initial_state == 0:
            self.state = np.array([1, 0], dtype=complex)
        else:
            self.state = np.array([0, 1], dtype=complex)

    def apply_gate(self, gate_matrix: np.ndarray) -> None:
        """Aplica uma porta quantica (matriz 2x2 unitaria)."""
        if gate_matrix.shape != (2, 2):
            raise ValueError("gate_matrix deve ser 2x2")
        self.state = gate_matrix @ self.state

    def get_probabilities(self) -> Tuple[float, float]:
        """Retorna (P(|0>), P(|1>))."""
        prob_0 = float(np.abs(self.state[0]) ** 2)
        prob_1 = float(np.abs(self.state[1]) ** 2)
        return prob_0, prob_1

    def measure(self) -> int:
        """Mede o qubit e colapsa o estado para |0> ou |1>."""
        prob_0, prob_1 = self.get_probabilities()
        total = prob_0 + prob_1
        prob_0, prob_1 = prob_0 / total, prob_1 / total
        result = int(np.random.choice([0, 1], p=[prob_0, prob_1]))
        if result == 0:
            self.state = np.array([1, 0], dtype=complex)
        else:
            self.state = np.array([0, 1], dtype=complex)
        return result

    def __str__(self) -> str:
        prob_0, prob_1 = self.get_probabilities()
        return f"|psi> = {prob_0:.3f}|0> + {prob_1:.3f}|1>"
