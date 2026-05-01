import numpy as np


class QuantumGates:
    """Biblioteca de portas quanticas (matrizes unitarias)."""

    @staticmethod
    def identity() -> np.ndarray:
        return np.eye(2, dtype=complex)

    @staticmethod
    def hadamard() -> np.ndarray:
        """Porta Hadamard (cria superposicao)."""
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    @staticmethod
    def pauli_x() -> np.ndarray:
        """Porta X (NOT quantico)."""
        return np.array([[0, 1], [1, 0]], dtype=complex)

    @staticmethod
    def pauli_y() -> np.ndarray:
        """Porta Y."""
        return np.array([[0, -1j], [1j, 0]], dtype=complex)

    @staticmethod
    def pauli_z() -> np.ndarray:
        """Porta Z."""
        return np.array([[1, 0], [0, -1]], dtype=complex)

    @staticmethod
    def phase_gate(theta: float) -> np.ndarray:
        """Porta de fase arbitraria."""
        return np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)

    @staticmethod
    def s_gate() -> np.ndarray:
        """Porta S = Phase(pi/2)."""
        return QuantumGates.phase_gate(np.pi / 2)

    @staticmethod
    def t_gate() -> np.ndarray:
        """Porta T = Phase(pi/4)."""
        return QuantumGates.phase_gate(np.pi / 4)
