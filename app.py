"""Streamlit web UI for the quantum circuit simulator."""
import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator


st.set_page_config(page_title="Quantum Simulator", page_icon="⚛️", layout="wide")


def build_bell() -> QuantumCircuit:
    c = QuantumCircuit(2)
    c.hadamard(0).cnot(0, 1)
    return c


def build_ghz() -> QuantumCircuit:
    c = QuantumCircuit(3)
    c.hadamard(0).cnot(0, 1).cnot(1, 2)
    return c


def build_superposition(n: int) -> QuantumCircuit:
    c = QuantumCircuit(n)
    for i in range(n):
        c.hadamard(i)
    return c


def build_custom(num_qubits: int, ops: list) -> QuantumCircuit:
    c = QuantumCircuit(num_qubits)
    for op in ops:
        name = op["gate"]
        if name == "H":
            c.hadamard(op["q"])
        elif name == "X":
            c.pauli_x(op["q"])
        elif name == "Y":
            c.pauli_y(op["q"])
        elif name == "Z":
            c.pauli_z(op["q"])
        elif name == "P":
            c.phase(op["q"], op["theta"])
        elif name == "CNOT":
            c.cnot(op["control"], op["target"])
    return c


EXAMPLES = {
    "Bell state (|00⟩+|11⟩)/√2": ("bell", None),
    "GHZ state (|000⟩+|111⟩)/√2": ("ghz", None),
    "Superposição uniforme (N qubits)": ("super", None),
    "Circuito custom": ("custom", None),
}


EXPLANATIONS = {
    "bell": (
        "**Bell state** é o exemplo canônico de **emaranhamento**. "
        "Aplicando `H` no qubit 0 cria-se superposição `(|0⟩+|1⟩)/√2`; o `CNOT(0,1)` "
        "amarra os dois qubits. Resultado: só `|00⟩` ou `|11⟩` aparecem nas medições — "
        "nunca `|01⟩` ou `|10⟩`. Os qubits estão **correlacionados**: medir um determina o outro, "
        "mesmo distantes."
    ),
    "ghz": (
        "**GHZ state** estende o Bell para 3 qubits: `(|000⟩+|111⟩)/√2`. "
        "Toda a tripla está emaranhada — medir qualquer qubit colapsa os outros dois. "
        "Usado em testes de não-localidade (desigualdades de Bell/Mermin) e como recurso em protocolos quânticos."
    ),
    "super": (
        "**Superposição uniforme** aplica `H` em cada qubit. Cada estado de base "
        "(`|00⟩`, `|01⟩`, `|10⟩`, `|11⟩` para 2 qubits) tem probabilidade idêntica `1/2^N`. "
        "Sem emaranhamento — cada qubit é independente. Base de algoritmos como Grover e Deutsch-Jozsa, "
        "que partem de superposição uniforme antes de aplicar oráculos."
    ),
    "custom": (
        "**Circuito custom** — você define a sequência. As portas atuam no vetor de estado conjunto "
        "como matrizes unitárias. Experimente: dois `H` em sequência cancelam (`H·H = I`); "
        "`X` antes de `H` muda a fase relativa; `CNOT` entre qubits em superposição cria emaranhamento."
    ),
}


GLOSSARY = """
- **Vetor de estado** — descrição completa do sistema. Para `N` qubits tem `2^N` amplitudes complexas.
  Cada amplitude `α` está associada a um estado de base; `|α|²` é a probabilidade de medir aquele estado.
- **Probabilidade teórica** — `|α|²` calculado direto do vetor de estado. É o valor exato (ideal).
- **Shots / medições** — cada shot recria o circuito, mede e colapsa o estado. Mais shots = estatística empírica
  mais próxima da teórica (lei dos grandes números).
- **Empírico vs teórico** — para 1000 shots, ruído estatístico é ~3%. Ideal: empírico converge à probabilidade
  teórica conforme `shots → ∞`.
- **Portas (`H`, `X`, `Y`, `Z`, `P`, `CNOT`)** — operações unitárias. `H` cria superposição, Paulis são rotações,
  `P(θ)` aplica fase em `|1⟩`, `CNOT` emaranha control e target.
"""


st.title("⚛️ Quantum Circuit Simulator")
st.caption("Simulador de circuitos quânticos em Python puro — NumPy + Matplotlib.")

with st.sidebar:
    st.header("Configuração")
    choice = st.selectbox("Exemplo", list(EXAMPLES.keys()))
    kind, _ = EXAMPLES[choice]

    if kind == "super":
        num_qubits = st.slider("Número de qubits", 1, 6, 2)
    elif kind == "custom":
        num_qubits = st.slider("Número de qubits", 1, 6, 2)
    else:
        num_qubits = None

    shots = st.slider("Shots (medições)", 100, 5000, 1000, step=100)
    seed = st.number_input("Seed (0 = aleatório)", min_value=0, value=0, step=1)

    st.divider()
    st.markdown("### Sobre")
    st.markdown(
        "[Repo no GitHub](https://github.com/EduardoMartins-Dev/Quantum-Simulator)"
    )

custom_ops: list = []
if kind == "custom":
    st.subheader("Construtor de circuito")
    if "ops" not in st.session_state:
        st.session_state.ops = []

    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        gate = st.selectbox("Porta", ["H", "X", "Y", "Z", "P", "CNOT"])
    with col2:
        if gate == "CNOT":
            control = st.number_input("Control", 0, num_qubits - 1, 0, step=1)
        else:
            qbit = st.number_input("Qubit", 0, num_qubits - 1, 0, step=1)
    with col3:
        if gate == "CNOT":
            target = st.number_input("Target", 0, num_qubits - 1, min(1, num_qubits - 1), step=1)
        elif gate == "P":
            theta = st.number_input("θ (rad)", value=float(np.pi / 2), step=0.1, format="%.4f")
        else:
            st.empty()
    with col4:
        st.write("")
        st.write("")
        if st.button("Adicionar"):
            if gate == "CNOT":
                if control != target:
                    st.session_state.ops.append({"gate": "CNOT", "control": int(control), "target": int(target)})
            elif gate == "P":
                st.session_state.ops.append({"gate": "P", "q": int(qbit), "theta": float(theta)})
            else:
                st.session_state.ops.append({"gate": gate, "q": int(qbit)})

    if st.session_state.ops:
        st.write("**Operações:**")
        for i, op in enumerate(st.session_state.ops):
            cols = st.columns([6, 1])
            cols[0].code(
                f"{op['gate']}("
                + (f"{op['control']}, {op['target']}" if op["gate"] == "CNOT"
                   else f"{op['q']}, θ={op['theta']:.3f}" if op["gate"] == "P"
                   else str(op["q"]))
                + ")"
            )
            if cols[1].button("🗑", key=f"del_{i}"):
                st.session_state.ops.pop(i)
                st.rerun()
        if st.button("Limpar tudo"):
            st.session_state.ops = []
            st.rerun()

    custom_ops = st.session_state.ops

run = st.button("▶️ Executar circuito", type="primary", use_container_width=True)

if run:
    if seed:
        np.random.seed(int(seed))

    if kind == "bell":
        circuit = build_bell()
    elif kind == "ghz":
        circuit = build_ghz()
    elif kind == "super":
        circuit = build_superposition(num_qubits)
    else:
        if not custom_ops:
            st.warning("Adicione pelo menos uma porta antes de executar.")
            st.stop()
        circuit = build_custom(num_qubits, custom_ops)

    st.markdown("### 📖 O que esse circuito faz")
    st.markdown(EXPLANATIONS[kind])

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Circuito")
        st.code(str(circuit))
        st.subheader("Vetor de estado")
        st.code(circuit.get_state_vector())
        st.subheader("Probabilidades teóricas")
        theoretical = circuit.get_probabilities()
        st.dataframe(
            {"Estado": [f"|{k}⟩" for k in sorted(theoretical)],
             "Probabilidade": [f"{theoretical[k] * 100:.2f}%" for k in sorted(theoretical)]},
            hide_index=True,
            use_container_width=True,
        )

    with col_right:
        st.subheader(f"Medições ({shots} shots)")
        results = QuantumSimulator.run(circuit, shots=shots)
        probs = QuantumSimulator.get_probabilities(results)

        items = sorted(results.items())
        states = [k for k, _ in items]
        counts = [v for _, v in items]

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0E1117")
        ax.set_facecolor("#0E1117")
        ax.bar(states, counts, color="#4FA3E0", edgecolor="#FAFAFA")
        ax.set_xlabel("Estado", color="#FAFAFA")
        ax.set_ylabel("Contagens", color="#FAFAFA")
        ax.tick_params(colors="#FAFAFA")
        for spine in ax.spines.values():
            spine.set_color("#FAFAFA")
        ax.grid(axis="y", alpha=0.2)
        total = sum(counts)
        for i, c in enumerate(counts):
            ax.text(i, c, f"{100 * c / total:.1f}%", ha="center", va="bottom", color="#FAFAFA")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(
            {"Estado": [f"|{s}⟩" for s in states],
             "Contagem": counts,
             "Empírico": [f"{probs[s] * 100:.2f}%" for s in states]},
            hide_index=True,
            use_container_width=True,
        )

    with st.expander("📚 Glossário rápido"):
        st.markdown(GLOSSARY)
else:
    st.info("👈 Escolha um exemplo na barra lateral e clique em **Executar circuito**.")
