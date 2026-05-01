# Quantum Circuit Simulator (MVP)

Simulador de circuitos quanticos em Python puro, com NumPy + Matplotlib.
Suporta criacao de qubits, portas Hadamard / Pauli-X / Y / Z / Phase / CNOT,
medicao com colapso de estado, execucao em N shots e visualizacao.

## Instalacao

```bash
pip install -r requirements.txt
```

Requer Python 3.8+.

## Uso pela CLI

```bash
# Bell state (emaranhamento): apenas |00> e |11> aparecem
python cli.py --example bell --shots 1000

# GHZ state em 3 qubits: apenas |000> e |111>
python cli.py --example ghz --shots 1000

# Superposicao uniforme em 2 qubits: ~25% para cada estado
python cli.py --example super --shots 500

# Circuito padrao (H em q0, CNOT(0,1)) com N qubits
python cli.py --qubits 2 --shots 2000

# Sem grafico (so saida em texto)
python cli.py --example bell --no-plot
```

A CLI imprime as contagens por estado e salva um PNG (default: `quantum_results.png`).

## Uso programatico

```python
from core.circuit import QuantumCircuit
from simulator.runner import QuantumSimulator

circuit = QuantumCircuit(2)
circuit.hadamard(0).cnot(0, 1)  # Bell state

results = QuantumSimulator.run(circuit, shots=1000)
for state, count in sorted(results.items()):
    print(f"|{state}>: {count}")
```

## Exemplos prontos

```bash
python examples/bell_state.py
python examples/ghz_state.py
python examples/superposition.py
python examples/grover_preview.py
```

## Conceitos

- **Qubit**: vetor complexo de dimensao 2; estado `[a, b]` com |a|^2 + |b|^2 = 1.
- **Hadamard (H)**: cria superposicao. H|0> = (|0>+|1>)/sqrt(2).
- **Pauli-X**: NOT quantico. X|0> = |1>.
- **Pauli-Y / Pauli-Z**: rotacoes em torno dos eixos Y e Z da esfera de Bloch.
- **Phase(theta)**: aplica fase e^(i*theta) em |1>.
- **CNOT(c, t)**: inverte o qubit `t` se `c` = |1>. Cria emaranhamento.
- **Medicao**: amostra do estado conjunto e colapsa para um estado de base.

## Arquitetura

```
core/
  qubit.py     # Qubit isolado (dim 2)
  gates.py     # Matrizes das portas
  circuit.py   # QuantumCircuit com vetor de estado conjunto (dim 2^N)
simulator/
  runner.py    # Replica o circuito N vezes e agrega medicoes
visualizer/
  plotter.py   # Grafico de barras com matplotlib
examples/      # Bell, GHZ, superposicao, preview Grover
cli.py         # CLI com argparse
```

Nota tecnica: o `QuantumCircuit` mantem um vetor de estado de dimensao 2^N,
o que e necessario para representar emaranhamento corretamente. Tentar
guardar um estado por qubit isolado nao captura correlacoes entre qubits
(p.ex. um Bell state nao e fatoravel em estados individuais).

## Proximos passos (v2.0 / v3.0)

- Web interface (React)
- Portas de rotacao Rx, Ry, Rz e CCNOT (Toffoli)
- Algoritmos de Grover e Deutsch-Jozsa
- Visualizacao 3D (esfera de Bloch)
