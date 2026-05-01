from typing import Dict, Optional

import matplotlib

# Backend nao-interativo: o CLI roda em terminal por padrao
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


class ResultsPlotter:
    """Gera graficos dos resultados de medicao."""

    @staticmethod
    def plot_results(
        results: Dict[str, int],
        title: str = "Quantum Circuit Results",
        output_path: Optional[str] = "quantum_results.png",
        show: bool = False,
    ) -> str:
        """Plota um grafico de barras das contagens.

        Returns:
            O caminho do arquivo salvo (PNG).
        """
        if not results:
            raise ValueError("results esta vazio - nada para plotar")

        # Ordena bitstrings lexicograficamente para um eixo X estavel
        items = sorted(results.items())
        states = [k for k, _ in items]
        counts = [v for _, v in items]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(states, counts, color="#2E75B6", edgecolor="black")
        ax.set_xlabel("Estados de base computacional", fontsize=12)
        ax.set_ylabel("Contagens", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        total = sum(counts)
        for i, count in enumerate(counts):
            pct = 100.0 * count / total
            ax.text(i, count, f"{pct:.1f}%", ha="center", va="bottom", fontsize=10)

        plt.tight_layout()
        if output_path:
            plt.savefig(output_path, dpi=150)
        if show:
            plt.show()
        plt.close(fig)
        return output_path or ""
