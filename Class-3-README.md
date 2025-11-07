# BruceAI · Class-3 Runner (No-BS README)

**Purpose:** a minimal, testable loop for *novel-but-aligned* exploration. If it passes the gates, it’s useful — not mystical.

**Highlights:** deterministic seeds • exploration schedule • alignment gating • CSV logs + JSON report

---

## What this is (plain English)

The Class-3 runner lets BruceAI explore with a little controlled randomness (**epsilon**) but only keeps results if five sanity checks (“**gates**”) all pass:

- **Novel** (not the same old thing)
- **Moving toward alignment** (less conflict with the integrity vector)
- **Simplifying** (lower VFE proxy)
- **Creative, not chaotic** (entropy bounded)
- **Actually better than baseline** (utility uplift)

> **TL;DR** — It’s an engineering harness for *creative but safe* behavior. If it passes, ship it. If it fails, we stop.

---

## Repo layout (relevant parts)

/BruceAI/
├─ class3_runner.py # the loop + metrics + gates + logs
├─ config.yaml # knobs: epsilon schedule, integrity axes, thresholds
/runs/
└─ run1.csv # per-step trace (created after you run)

yaml
Copy code

**Files**
- **`class3_runner.py`** – full runner with a toy `Task` (sorts ints).
- **`config.yaml`** – seed, steps, epsilon, integrity vector, thresholds.
- **`runs/run1.csv`** – stepwise metrics (entropy, VFE, commutator, etc.).
- **`runs/report.json`** – final summary (capture via `tee`).

**Key concepts**
- **P** — internal attention/state (PSD, trace=1).
- **I_vector** — integrity axes (**truth, non-harm, consent, privacy, transparency**).
- **ε-schedule** — noise warmup → peak → cooldown for exploration.
- **Gates** — 5 pass/fail checks before calling it “Class-3”.

---

## How the loop works

1. Initialize a clean state **P** (same dimension as **I_vector**).
2. At each step: propose plan → assess risk → execute → compute task loss + alignment cost.
3. Update **P** with small gradient + scheduled noise; project back to PSD trace-1.
4. Track metrics: **entropy**, **VFE proxy**, **commutator norm** with **I** (alignment distance).
5. Apply failsafes on spikes/chaos. After steps, compute final **gates**.

**Gates**
- **G1 – Novelty:** Wasserstein/Bures distance vs start is high enough.
- **G2 – Align trend:** commutator norm trending **down** (statistically).
- **G3 – VFE down:** simpler/more efficient over time.
- **G4 – Entropy bounded:** increased some, but under cap.
- **G5 – Utility uplift:** beats baseline by minimum delta.

All five must pass → `class3_pass: true`.

---

## Config knobs (`config.yaml`)

```yaml
seed: 42
steps_ideation: 60
lr: 0.05
epsilon_schedule: [0.00, 0.04, 0.01]   # warmup → peak → cooldown
entropy_cap_factor: 1.5

# Integrity vector (truth, nonharm, consent, privacy, transparency)
I_vector: [1.0, 0.95, 0.90, 0.90, 0.80]
alignment_weights: [4.0, 3.0, 3.0, 2.0, 2.0]

lambda_I: 1.0     # weight on alignment loss
lambda_DL: 0.1    # simplicity term (VFE proxy)

# Class-3 gates
novelty_threshold: 0.50
pval_threshold: 0.05
utility_uplift_min: 0.05
Tuning tips

More exploration → raise peak epsilon (e.g., 0.05) but watch G4 cap.

Stricter ethics → raise alignment_weights or tighten pval_threshold.

Fewer false wins → raise novelty_threshold and utility_uplift_min.

When gates fail

G2 fails (no convergence): lower epsilon or raise lambda_I.

G4 fails (entropy blows cap): lower peak epsilon or slightly raise cap.

G5 fails (novel but useless): fix the task/metric; novelty ≠ value.

Run it
Codespaces / local

bash
Copy code
# from repo root
pip install numpy pyyaml
mkdir -p runs

# preferred: run as module
PYTHONPATH=. python -m BruceAI.class3_runner | tee runs/report.json

# fallback: run directly
python BruceAI/class3_runner.py | tee runs/report.json

# inspect outputs
head -n 40 runs/report.json
ls runs   # should include run1.csv
GitHub Actions (optional)

yaml
Copy code
# .github/workflows/class3.yml
name: Class3 Runner
on: [workflow_dispatch]
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install numpy pyyaml
      - run: PYTHONPATH=. python -m BruceAI.class3_runner
      - uses: actions/upload-artifact@v4
        with:
          name: class3-logs
          path: runs/
Reading the outputs
report.json (example)

json
Copy code
{
  "novelty": 0.61,
  "slope_comm": -0.012, "p_comm": 0.004,
  "slope_vfe": -0.021,  "p_vfe": 0.001,
  "entropy_cap": 1.85,  "entropy_max": 1.42,
  "utility_baseline": 0.11, "utility_c3": 0.23, "uplift": 0.12,
  "gates": {"G1_novelty": true, "G2_align_slope": true, "G3_vfe_down": true, "G4_entropy_bounded": true, "G5_utility": true},
  "class3_pass": true
}
runs/run1.csv (snippet)

python-repl
Copy code
step,epsilon,entropy,VFE,comm_norm,kill_reason
0,0.000,1.386,0.512,0.443,
1,0.001,1.392,0.507,0.438,
...
37,0.040,1.421,0.471,0.310,
...
59,0.010,1.405,0.455,0.281,
Green light = class3_pass: true.
If any gate is false → fail (by design).

Wiring Bruce (next step)
Replace the toy Task with your real pipeline:

propose_plan(P, context) → choose skills/tools/strategies from Bruce’s capability map.

plan_risks(plan) → run safety head (truth, non-harm, consent, privacy, transparency).

execute(plan) → generate/act; log artifacts.

loss(output) → task objective (lower is better).

metric(output) → utility score (0..1); used by G5.

baseline(context) → “no exploration” control for uplift comparison.

Don’t market this as “consciousness.” Call it controlled exploration with alignment gates. It’s testable and sane.

FAQ (short + blunt)
Is this mystical?
No. It’s a noisy optimizer with guardrails and stats tests.

What makes it “Class-3”?
Novel structure appears and alignment/stability improve and utility beats baseline — all five gates pass.

How do I prove it?
Seeded runs, logged metrics, reproducible code, repeatable passes across tasks. Add EEG later if you want bio-correlates.

What if it keeps failing?
Lower epsilon peak, raise lambda_I, fix your Task metric. Garbage metrics → garbage gates.

License & Credit
This runner is a practical harness to evaluate novel-but-aligned exploration for BruceAI / NeoShade. Use responsibly. No BS, no fluff — just engineering you can measure.

javascript
Copy code
