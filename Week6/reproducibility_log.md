# Reproducibility Log — Bell State on IBM Quantum Hardware

> **Assignment:** Create your first Qiskit program, run on real IBM hardware, and document reproducibility.
> **Course:** Quantum Computing SOP — Week 5
> **Reference:** [IBM Quantum Computing in Practice](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice) | `lecture2.pdf`

---

## 1. Experiment Information

| Field | Value |
|-------|-------|
| **Title** | Bell State Experiment on Real IBM Quantum Hardware |
| **Date/Time** | 2026-09-19 16:33:28 |
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
| **Basis Gates** | if_else, reset_2, rz, sx, reset, id, measure_2, measure_reset_2 |
| **Physical Qubits Used** | [22, 23] |
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
| **Physical Qubits** | — | [22, 23] |

---

## 5. Execution Parameters

| Parameter | Value |
|-----------|-------|
| **Primitive** | SamplerV2 (qiskit-ibm-runtime) |
| **Number of Shots** | 4096 |
| **Execution Mode** | Single job |
| **Error Mitigation** | Default (none explicitly configured) |
| **Job ID** | dan6np5r85ps73fdmg90 |
| **Job Submission Time** | 2026-09-19 16:33:00 (approx.) |
| **Job Completion Time** | 2026-09-19 16:33:28 |
| **Total Execution Time** | 27.9s |

---

## 6. Results

### 6.1 Real Hardware Results (ibm_fez)

| Bitstring | Counts | Probability |
|-----------|--------|-------------|
| \|00⟩ | 2048 | 0.5000 |
| \|01⟩ | 55 | 0.0134 |
| \|10⟩ | 32 | 0.0078 |
| \|11⟩ | 1961 | 0.4788 |
| **Total** | **4096** | **1.0000** |

**Fidelity (P(\|00⟩) + P(\|11⟩)): 0.9788**

### 6.2 Simulator Results (AerSimulator Baseline)

| Bitstring | Counts | Probability |
|-----------|--------|-------------|
| \|00⟩ | 2100 | 0.5127 |
| \|01⟩ | 0 | 0.0000 |
| \|10⟩ | 0 | 0.0000 |
| \|11⟩ | 1996 | 0.4873 |
| **Total** | **4096** | **1.0000** |

**Fidelity (P(\|00⟩) + P(\|11⟩)): 1.0000**

### 6.3 Comparison

| Metric | Simulator | Real Hardware | Deviation |
|--------|-----------|---------------|-----------|
| P(\|00⟩) | 0.5127 | 0.5000 | 0.0127 |
| P(\|11⟩) | 0.4873 | 0.4788 | 0.0085 |
| P(\|01⟩) | 0.0000 | 0.0134 | 0.0134 |
| P(\|10⟩) | 0.0000 | 0.0078 | 0.0078 |
| **Fidelity** | **1.0000** | **0.9788** | **0.0212** |

---

## 7. Observations & Analysis

### 7.1 Key Observations
- The real hardware (ibm_fez) achieves a fidelity of **97.88%**, confirming successful quantum entanglement on a 156-qubit processor.
- The dominant outcomes are |00⟩ (50.00%) and |11⟩ (47.88%), consistent with a Bell state where both qubits are maximally correlated.
- Small but non-zero probabilities appear for |01⟩ (1.34%) and |10⟩ (0.78%), which are **forbidden** in an ideal Bell state. These arise entirely from hardware noise.
- The |01⟩ error rate (1.34%) is slightly higher than |10⟩ (0.78%), suggesting asymmetric readout or gate errors between the two physical qubits (22 and 23).
- The simulator produces **perfect** fidelity (1.0000) with zero counts for |01⟩ and |10⟩, confirming these errors are hardware-specific, not algorithmic.

### 7.2 Sources of Error
1. **Gate errors:** The transpiled circuit uses 5 RZ gates, 3 SX gates, and 1 CZ gate. Each gate introduces small errors due to imperfect microwave control pulses.
2. **Decoherence:** Qubit states decay during the 7-depth ISA circuit execution (T1 relaxation and T2 dephasing).
3. **Readout errors:** The measurement apparatus occasionally misidentifies |0⟩ as |1⟩ and vice versa, explaining the asymmetric |01⟩ vs |10⟩ error rates.
4. **Crosstalk:** Physical qubits 22 and 23 on ibm_fez may experience interference from neighboring qubits on the chip.

### 7.3 Lessons Learned
- Real quantum hardware introduces noise that is absent in simulation — the 2.12% fidelity deviation quantifies this gap.
- Even with noise, the Bell state entanglement signal is overwhelmingly clear: 97.88% of measurements show the expected correlated outcomes.
- The Qiskit Pattern (Map → Optimize → Execute → Post-process) works identically for both simulator and real hardware — only the backend object changes.
- Reproducibility logging is essential because quantum hardware is re-calibrated regularly, meaning the same circuit could yield different error rates on a different day.

---

## 8. References

| # | Reference |
|---|-----------|
| 1 | [IBM Quantum Computing in Practice (Course)](https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice) |
| 2 | `lecture2.pdf` — Course lecture slides |
| 3 | [Qiskit SDK Documentation](https://docs.quantum.ibm.com/) |
| 4 | [IBM Quantum Platform](https://quantum.ibm.com/) |
| 5 | [Qiskit Patterns / Development Workflow](https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns) |

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
jupyter notebook week5_bell_state_ibm_hardware.ipynb
```



---

*Log generated on 2026-09-19 — Quantum Computing SOP, Week 5*
