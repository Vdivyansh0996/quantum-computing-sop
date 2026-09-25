"""
Week 5: Bell State on IBM Quantum Hardware — Full Experiment Runner
Runs all steps and prints reproducibility metadata.
"""
import warnings
warnings.filterwarnings('ignore')

import time
import datetime
import platform
import sys
import numpy as np

# ═══════════════════════════════════════════════════════════
# SECTION 1: Connect to IBM Quantum
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("  SECTION 1: Connecting to IBM Quantum...")
print("=" * 60)

from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.least_busy(simulator=False, operational=True)
print(f"  Connected to IBM Quantum")
print(f"  Selected backend: {backend.name}")
print(f"  Number of qubits: {backend.num_qubits}")
print(f"  Basis gates: {list(backend.operation_names)[:8]}")
print()

# ═══════════════════════════════════════════════════════════
# SECTION 2: STEP 1 — MAP: Build Bell State Circuit
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("  SECTION 2: STEP 1 — MAP: Building Bell State Circuit")
print("=" * 60)

from qiskit import QuantumCircuit

bell = QuantumCircuit(2)
bell.h(0)       # Hadamard: creates superposition
bell.cx(0, 1)   # CNOT: entangles qubits
bell.measure_all()

print(f"  Number of qubits: {bell.num_qubits}")
print(f"  Gate operations: {bell.count_ops()}")
print(f"  Circuit depth: {bell.depth()}")
print(f"\n  Circuit diagram:")
print(bell.draw('text'))
print()

# ═══════════════════════════════════════════════════════════
# SECTION 3: STEP 2 — OPTIMIZE: Transpile to ISA
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("  SECTION 3: STEP 2 — OPTIMIZE: Transpiling...")
print("=" * 60)

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

pm = generate_preset_pass_manager(target=backend.target, optimization_level=3)
bell_isa = pm.run(bell)

print(f"  Before Transpilation: Gates={bell.count_ops()}, Depth={bell.depth()}")
print(f"  After Transpilation:  Gates={bell_isa.count_ops()}, Depth={bell_isa.depth()}")
try:
    print(f"  Physical qubits: {bell_isa.layout.final_index_layout(filter_ancillas=True)}")
except:
    print(f"  Physical qubits: (layout info not available)")
print()

# ═══════════════════════════════════════════════════════════
# SECTION 4: STEP 3 — EXECUTE: Run on Real Hardware
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("  SECTION 4: STEP 3 — EXECUTE: Submitting to real hardware...")
print("=" * 60)

from qiskit_ibm_runtime import SamplerV2

sampler = SamplerV2(backend)
print(f"  Submitting job to {backend.name}...")
start_time = time.time()
job = sampler.run([bell_isa], shots=4096)
print(f"  Job ID: {job.job_id()}")
print(f"  Waiting for results (this may take 1-3 minutes)...")

result = job.result()
elapsed = time.time() - start_time
print(f"  Job completed in {elapsed:.1f} seconds")

counts_hw = result[0].data.meas.get_counts()
total_hw = sum(counts_hw.values())
print(f"\n  === Real Hardware Results ===")
print(f"  Total shots: {total_hw}")
print(f"  Counts: {counts_hw}")
print(f"  Probabilities:")
for bs in sorted(counts_hw.keys()):
    prob = counts_hw[bs] / total_hw
    print(f"    |{bs}⟩: {counts_hw[bs]}/{total_hw} = {prob:.4f}")
print()

# ═══════════════════════════════════════════════════════════
# SECTION 5: Simulator Comparison
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("  SECTION 5: Running Simulator Baseline...")
print("=" * 60)

from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2

sim_backend = AerSimulator()
pm_sim = generate_preset_pass_manager(target=sim_backend.target, optimization_level=3)
bell_sim_isa = pm_sim.run(bell)

sampler_sim = BackendSamplerV2(backend=sim_backend)
job_sim = sampler_sim.run([bell_sim_isa], shots=4096)
result_sim = job_sim.result()
counts_sim = result_sim[0].data.meas.get_counts()
total_sim = sum(counts_sim.values())

print(f"  Simulator Counts: {counts_sim}")
for bs in sorted(counts_sim.keys()):
    print(f"    |{bs}⟩: {counts_sim[bs]}/{total_sim} = {counts_sim[bs]/total_sim:.4f}")

# Fidelity
fidelity_sim = (counts_sim.get('00', 0) + counts_sim.get('11', 0)) / total_sim
fidelity_hw = (counts_hw.get('00', 0) + counts_hw.get('11', 0)) / total_hw
print(f"\n  Fidelity (P(|00⟩) + P(|11⟩)):")
print(f"    Simulator: {fidelity_sim:.4f}")
print(f"    Hardware:  {fidelity_hw:.4f}")
print(f"    Deviation: {abs(fidelity_sim - fidelity_hw):.4f}")
print()

# ═══════════════════════════════════════════════════════════
# SECTION 7: REPRODUCIBILITY METADATA
# ═══════════════════════════════════════════════════════════
import qiskit
try:
    import qiskit_ibm_runtime
    runtime_version = qiskit_ibm_runtime.__version__
except:
    runtime_version = 'N/A'
try:
    import qiskit_aer as _aer
    aer_version = _aer.__version__
except:
    aer_version = 'N/A'

print("=" * 60)
print("       REPRODUCIBILITY LOG — METADATA")
print("=" * 60)
print()
print("--- Experiment Info ---")
print(f"  Title:       Bell State on IBM Quantum Hardware")
print(f"  Date/Time:   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Objective:   Demonstrate Qiskit Pattern on real QPU")
print()
print("--- Software Environment ---")
print(f"  Python:              {sys.version}")
print(f"  Qiskit:              {qiskit.__version__}")
print(f"  qiskit-ibm-runtime:  {runtime_version}")
print(f"  qiskit-aer:          {aer_version}")
print(f"  NumPy:               {np.__version__}")
print(f"  OS:                  {platform.system()} {platform.release()}")
print()
print("--- Backend / Hardware ---")
print(f"  Backend name:        {backend.name}")
print(f"  Number of qubits:    {backend.num_qubits}")
print(f"  Basis gates:         {list(backend.operation_names)[:8]}")
print()
print("--- Circuit Details ---")
print(f"  Abstract gates:      {bell.count_ops()}")
print(f"  Abstract depth:      {bell.depth()}")
print(f"  ISA gates:           {bell_isa.count_ops()}")
print(f"  ISA depth:           {bell_isa.depth()}")
print(f"  Optimization level:  3")
print()
print("--- Execution Parameters ---")
print(f"  Primitive:           SamplerV2")
print(f"  Shots:               4096")
print(f"  Job ID:              {job.job_id()}")
print(f"  Execution time:      {elapsed:.1f}s")
print()
print("--- Results Summary ---")
print(f"  Hardware counts:     {counts_hw}")
print(f"  Hardware fidelity:   {fidelity_hw:.4f}")
print(f"  Simulator counts:    {counts_sim}")
print(f"  Simulator fidelity:  {fidelity_sim:.4f}")
print(f"  Fidelity deviation:  {abs(fidelity_sim - fidelity_hw):.4f}")
print()
print("=" * 60)
print("  Copy the above into your reproducibility_log.md")
print("=" * 60)
print("\nDONE! All sections completed successfully.")
