# Reproducibility Log — Bell State on IBM Quantum Hardware

> **Assignment:** Create your first Qiskit program, run on real IBM hardware, and document reproducibility.
> **Course:** Quantum Computing SOP — Week 6
> **Reference:** [IBM Quantum Computing in Practice](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice) | `lecture2.pdf`

---

## 1. Experiment Information

| Field | Value |
|-------|-------|
| **Title** | Bell State Experiment on Real IBM Quantum Hardware |
| **Date/Time** | 2026-09-25 15:31:13 |
| **Researcher** | Divyansh Vyas |
| **Objective** | Demonstrate the Qiskit Pattern (Map → Optimize → Execute → Post-process) on a real quantum processor and compare with simulator results |
| **Tutorial Used** | Bell State — Hadamard + CNOT entanglement circuit |

---

## 2. Software Environment

| Component | Version |
|-----------|---------|
| **Python** | 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] |
| **Qiskit** | 2.5.2 |
| **qiskit-ibm-runtime** | 0.49.0 |
| **qiskit-aer** | 0.17.2 |
| **NumPy** | 2.5.2 |
| **Matplotlib** | 3.11.1 |
| **Operating System** | Windows 11 |
| **Execution Environment** | Local Python script (run_experiment.py) |

---

## 3. Hardware / Backend Details

| Field | Value |
|-------|-------|
| **Backend Name** | ibm_fez |
| **Number of Qubits** | 156 |
| **Basis Gates** | xslow, reset_2, measure_2, id, rz, sx, measure, measure_reset_2 |
| **Physical Qubits Used** | [142, 143] |
| **Calibration Date** | (Calibration snapshot at time of execution) |

---

## 4. Circuit Details

### 4.1 Abstract Circuit

```
     ┌───┐      ░ ┌─┐   
q_0: ┤ H ├──■───░─┤M├───
     └───┘┌─┴─┐ ░ └╥┘┌─┐
q_1: ────┤ X ├─░──╫─┤M├
          └───┘ ░  ║ └╥┘
c: 2/══════════════╩══╩═
                   0  1
```

| Metric | Value |
|--------|-------|
| **Qubits** | 2 |
| **Gates** | H(1), CX(1), Measure(2), Barrier(1) |
| **Circuit Depth** | 3 |

### 4.2 ISA (Transpiled) Circuit

| Metric | Before Transpilation | After Transpilation |
|--------|---------------------|---------------------|
| **Gate Count** | H(1), CX(1), Measure(2), Barrier(1) | RZ(5), SX(3), CZ(1), Measure(2), Barrier(1) |
| **Circuit Depth** | 3 | 7 |
| **Basis Gates Used** | H, CX, Measure | rz, sx, cz, measure |
| **Optimization Level** | — | 3 |
| **Physical Qubits** | — | [142, 143] |

---

## 5. Execution Parameters

| Parameter | Value |
|-----------|-------|
| **Primitive** | SamplerV2 (qiskit-ibm-runtime) |
| **Number of Shots** | 4096 |
| **Execution Mode** | Single job |
| **Error Mitigation** | Default (none explicitly configured) |
| **Job ID** | dar4co3ojkfs738njskg |
| **Job Submission Time** | 2026-09-25 15:31:03 (approx.) |
| **Job Completion Time** | 2026-09-25 15:31:13 |
| **Total Execution Time** | 9.3s |

---

## 6. Results

### 6.1 Real Hardware Results (ibm_fez)

| Bitstring | Counts | Probability |
|-----------|--------|-------------|
| \|00⟩ | 2075 | 0.5066 |
| \|01⟩ | 26 | 0.0063 |
| \|10⟩ | 35 | 0.0085 |
| \|11⟩ | 1960 | 0.4785 |
| **Total** | **4096** | **1.0000** |

**Fidelity (P(\|00⟩) + P(\|11⟩)): 0.9851**

### 6.2 Simulator Results (AerSimulator Baseline)

| Bitstring | Counts | Probability |
|-----------|--------|-------------|
| \|00⟩ | 2038 | 0.4976 |
| \|01⟩ | 0 | 0.0000 |
| \|10⟩ | 0 | 0.0000 |
| \|11⟩ | 2058 | 0.5024 |
| **Total** | **4096** | **1.0000** |

**Fidelity (P(\|00⟩) + P(\|11⟩)): 1.0000**

### 6.3 Comparison

| Metric | Simulator | Real Hardware | Deviation |
|--------|-----------|---------------|-----------|
| P(\|00⟩) | 0.4976 | 0.5066 | 0.0090 |
| P(\|11⟩) | 0.5024 | 0.4785 | 0.0239 |
| P(\|01⟩) | 0.0000 | 0.0063 | 0.0063 |
| P(\|10⟩) | 0.0000 | 0.0085 | 0.0085 |
| **Fidelity** | **1.0000** | **0.9851** | **0.0149** |

---

## 7. Observations & Analysis

### 7.1 Key Observations
- The real hardware (ibm_fez) achieves a fidelity of **98.51%**, confirming successful quantum entanglement on a 156-qubit processor.
- The dominant outcomes are |00⟩ (50.66%) and |11⟩ (47.85%), consistent with a Bell state where both qubits are maximally correlated.
- Small but non-zero probabilities appear for |01⟩ (0.63%) and |10⟩ (0.85%), which are **forbidden** in an ideal Bell state. These arise entirely from hardware noise.
- The |10⟩ error rate (0.85%) is slightly higher than |01⟩ (0.63%), suggesting asymmetric readout or gate errors between the two physical qubits (142 and 143).
- The simulator produces **perfect** fidelity (1.0000) with zero counts for |01⟩ and |10⟩, confirming these errors are hardware-specific, not algorithmic.
- Compared to the previous run (2026-09-19, qubits [22, 23], fidelity 0.9788), this run on qubits [142, 143] shows improved fidelity (0.9851), demonstrating that error rates vary across physical qubits on the same chip.

### 7.2 Sources of Error
1. **Gate errors:** The transpiled circuit uses 5 RZ gates, 3 SX gates, and 1 CZ gate. Each gate introduces small errors due to imperfect microwave control pulses.
2. **Decoherence:** Qubit states decay during the 7-depth ISA circuit execution (T1 relaxation and T2 dephasing).
3. **Readout errors:** The measurement apparatus occasionally misidentifies |0⟩ as |1⟩ and vice versa, explaining the asymmetric |01⟩ vs |10⟩ error rates.
4. **Crosstalk:** Physical qubits 142 and 143 on ibm_fez may experience interference from neighboring qubits on the chip.

### 7.3 Lessons Learned
- Real quantum hardware introduces noise that is absent in simulation — the 1.49% fidelity deviation quantifies this gap.
- Even with noise, the Bell state entanglement signal is overwhelmingly clear: 98.51% of measurements show the expected correlated outcomes.
- The Qiskit Pattern (Map → Optimize → Execute → Post-process) works identically for both simulator and real hardware — only the backend object changes.
- Reproducibility logging is essential because quantum hardware is re-calibrated regularly, meaning the same circuit could yield different error rates on a different day.

---

## 9. How to Reproduce This Experiment

```bash
# 1. Install dependencies
pip install qiskit qiskit-ibm-runtime qiskit-aer matplotlib numpy

# 2. Save your IBM Quantum API token (run once in Python)
# from qiskit_ibm_runtime import QiskitRuntimeService
# QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token="YOUR_TOKEN", overwrite=True)

# 3. Run the experiment script
python run_experiment.py

# 4. Or open the notebook
jupyter notebook week6_bell_state_ibm_hardware.ipynb
```

> **⚠️ Important:** Exact results will NOT be identical when re-running because:
> - Quantum measurements are inherently probabilistic
> - Hardware noise changes with each calibration cycle (ibm_fez is recalibrated daily)
> - Different backends have different error characteristics
> - Queue times vary based on system load
>
> However, the **qualitative behavior** (dominant |00⟩ and |11⟩ outcomes, fidelity ≥ 0.95) should be consistent.

---

*Log generated on 2026-09-25 — Quantum Computing SOP, Week 6*
