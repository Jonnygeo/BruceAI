# file: class3_runner.py
import os, json, csv, math, random
import numpy as np
# ---- JSON encoder to avoid NumPy bool/float issues ----
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# ---------- Utils ----------
def set_seed(s):
    random.seed(s); np.random.seed(s)

def project_psd_trace1(M):
    # Symmetrize
    M = 0.5*(M+M.T)
    # Eigen clamp
    eigvals, eigvecs = np.linalg.eigh(M)
    eigvals = np.clip(eigvals, 0.0, None)
    if eigvals.sum() <= 1e-12:
        # fallback: tiny identity
        d = M.shape[0]
        return np.eye(d)/d
    M_psd = (eigvecs * eigvals) @ eigvecs.T
    # Renormalize to trace = 1
    return M_psd / np.trace(M_psd)

def commutator_norm(P, I_diag):
    # I is diagonal vector -> construct diagonal matrix on-the-fly
    D = np.diag(I_diag)
    C = D @ P - P @ D
    return np.linalg.norm(C, 'fro')

def entropy_from_P(P, eps=1e-12):
    # Entropy of eigen-spectrum (Shannon)
    w, _ = np.linalg.eigh(0.5*(P+P.T))
    w = np.clip(w, eps, None)
    w = w / w.sum()
    return float(-(w*np.log(w)).sum())

def emd_spectra(P0, P1):
    # Earth Mover's Distance (Wasserstein-1) between eigenvalue spectra
    w0, _ = np.linalg.eigh(0.5*(P0+P0.T)); w0 = np.clip(w0, 0, None); w0 /= w0.sum()
    w1, _ = np.linalg.eigh(0.5*(P1+P1.T)); w1 = np.clip(w1, 0, None); w1 /= w1.sum()
    w0_sorted = np.sort(w0); w1_sorted = np.sort(w1)
    # 1D EMD = L1 distance between CDFs; simple approximation:
    return float(np.abs(np.cumsum(w0_sorted) - np.cumsum(w1_sorted)).mean())

def bures_distance(P0, P1, eps=1e-12):
    # Bures distance for density matrices (PSD trace-1)
    # d_B^2 = 2(1 - Tr( sqrt( sqrt(P0) P1 sqrt(P0) ) ))
    def mat_sqrt(A):
        w, V = np.linalg.eigh(0.5*(A+A.T))
        w = np.clip(w, eps, None)
        return (V * np.sqrt(w)) @ V.T
    S0 = mat_sqrt(P0)
    M  = S0 @ P1 @ S0
    S  = mat_sqrt(M)
    fid = np.trace(S)
    val = max(0.0, 2.0*(1.0 - float(fid)))
    return math.sqrt(val)

def linear_trend_pvalue(y):
    # OLS slope significance vs zero (two-sided) using simple t-test
    x = np.arange(len(y)); X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    yhat = X @ beta
    resid = y - yhat
    s2 = (resid@resid) / max(1, len(y)-2)
    XtX_inv = np.linalg.inv(X.T @ X)
    se = math.sqrt(s2 * XtX_inv[1,1])
    slope = beta[1]
    if se <= 1e-12:
        return slope, 0.0
    t = slope / se
    # small-sample rough p via normal approx; good enough for gating
    from math import erf, sqrt
    p = 2*(1 - 0.5*(1+erf(abs(t)/sqrt(2))))
    return slope, p

# ---------- Alignment loss ----------
def alignment_violation_vector(plan_risks, I_vec):
    # plan_risks in [0,1] predicted by a small safety head (you provide)
    # violation = max(0, risk - allowed)
    return np.maximum(0.0, np.array(plan_risks) - np.array(I_vec))

def alignment_loss(plan_risks, I_vec, w):
    v = alignment_violation_vector(plan_risks, I_vec)
    return float(np.dot(np.array(w), v))

# ---------- Noise ----------
def spectral_jitter(P, scale=0.02):
    # Add zero-mean noise in eigenbasis; larger on small eigenvalues
    w, V = np.linalg.eigh(0.5*(P+P.T))
    w = np.clip(w, 0, None)
    # variance inversely related to mass: push small modes to explore
    var = scale * (1.0 - (w / (w.sum()+1e-12)))
    noise = (V * (np.random.normal(0.0, np.sqrt(np.maximum(var,1e-8)), size=w.shape))) @ V.T
    noise = 0.5*(noise+noise.T)
    return noise

def dropout_diagonal(P, drop_prob=0.1):
    D = np.diag(np.diag(P).copy())
    mask = (np.random.rand(D.shape[0]) > drop_prob).astype(float)
    Dd = np.diag(np.diag(D)*mask)
    off = P - D
    return off + Dd

# ---------- Cost (VFE proxy) ----------
def description_length(P):
    # L2 regularizer on spectrum (encourage simplicity)
    w, _ = np.linalg.eigh(0.5*(P+P.T)); w = np.clip(w, 0, None); w /= w.sum()
    return float(np.sum((w - 1.0/len(w))**2))

def cost_F(task_loss, align_loss, dl, lam_I, lam_DL):
    return float(task_loss + lam_I*align_loss + lam_DL*dl)

# ---------- Task hooks (YOU: wire Bruce here) ----------
class Task:
    """
    You provide:
      - propose_plan(P, context) -> plan object for Bruce to execute
      - plan_risks(plan) -> [risk_truth, risk_nonharm, ...] in [0,1]
      - execute(plan) -> output
      - loss(output)  -> scalar task loss (lower is better)
      - metric(output)-> [0..1] utility metric (higher is better)
      - baseline(context)-> output (no exploration baseline)
    For a quick start, stub with a simple function and unit tests.
    """
    def __init__(self, unit_tests):
        self.tests = unit_tests

    def propose_plan(self, P, context):
        # Example: pick top-k "skills" from P's diagonal
        idx = np.argsort(-np.diag(P))[:3].tolist()
        return {"skills": idx, "context": context}

    def plan_risks(self, plan):
        # Dummy: low risk; replace with your safety head
        return [0.05, 0.04, 0.03, 0.02, 0.10]

    def execute(self, plan):
        # Replace with Bruce’s generation conditioned on selected skills
        ctx = plan["context"]
        return {"answer": sorted(ctx)}  # toy example

    def loss(self, output):
        # Lower is better; here invert unit-test score
        passed = sum(1 for t in self.tests if t(output))
        return 1.0 - (passed / max(1,len(self.tests)))

    def metric(self, output):
        # Higher is better (utility)
        passed = sum(1 for t in self.tests if t(output))
        return passed / max(1,len(self.tests))

    def baseline(self, context):
        # No-explore baseline (e.g., greedy decode)
        return {"answer": list(context)}  # toy baseline

# ---------- Runner ----------
def epsilon_at(step, T, warmup, peak, cool):
    if T <= 2: return 0.0
    # simple triangular schedule
    half = T//2
    if step < half:
        # warmup -> peak
        a = warmup + (peak - warmup) * (step/half)
    else:
        # peak -> cooldown
        a = peak + (cool - peak) * ((step - half)/max(1,T-half))
    return max(0.0, float(a))

def run_class3(context, cfg, task, log_path):
    set_seed(cfg["seed"])
    d = len(cfg["I_vector"])         # dimension = # integrity axes or skills—expand as needed
    I_vec = np.array(cfg["I_vector"], float)

    # Initialize P as near-uniform PSD
    A = np.random.randn(d, d); P = project_psd_trace1(A@A.T)

    logs = []
    T = cfg["steps_ideation"]
    warm, peak, cool = cfg["epsilon_schedule"]

    # Baseline (execution without exploration)
    base_out = task.baseline(context)
    base_metric = task.metric(base_out)

    # Save initial stats
    P0 = P.copy()
    S0 = entropy_from_P(P0)
    cap = cfg["entropy_cap_factor"] * S0

    vfe_hist, ent_hist, com_hist = [], [], []
    last20 = []

    for t in range(T):
        eps = epsilon_at(t, T, *cfg["epsilon_schedule"])

        plan = task.propose_plan(P, context)
        risks = task.plan_risks(plan)
        out   = task.execute(plan)

        task_loss = task.loss(out)
        alignL    = alignment_loss(risks, I_vec, cfg["alignment_weights"])
        dl        = description_length(P)
        vfe       = cost_F(task_loss, alignL, dl, cfg["lambda_I"], cfg["lambda_DL"])

        # gradients wrt P -> use finite differences placeholder (you should plug autodiff if P comes from a differentiable head)
        # Here we steer P toward lower cost on diagonal (skills) as a simple surrogate:
        gradP = np.zeros_like(P)
        gradP[np.arange(d), np.arange(d)] = vfe  # crude placeholder

        # Update rule with noise
        delta = -cfg["lr"] * gradP + eps * spectral_jitter(P, scale=eps)
        P_try = P + delta
        # occasional diagonal dropout before projection
        if np.random.rand() < 0.25:
            P_try = dropout_diagonal(P_try, drop_prob=0.1)

        P = project_psd_trace1(P_try)

        # Metrics
        comm = commutator_norm(P, I_vec)
        ent  = entropy_from_P(P)
        vfe_hist.append(vfe); ent_hist.append(ent); com_hist.append(comm)
        last20.append(comm); last20 = last20[-20:]

        # Failsafes
        kill_reason = ""
        if len(last20) >= 10:
            med = np.median(last20)
            if comm > 2.0*med:
                kill_reason = "FS1_misalignment_spike"
        if len(vfe_hist) >= 6 and kill_reason == "":
            if all(vfe_hist[-i] > vfe_hist[-i-1] for i in range(1,6)) and (len(ent_hist)>1 and (ent_hist[-1]-ent_hist[-6])>0.2):
                kill_reason = "FS2_chaos"
        if ent > cap and kill_reason == "":
            kill_reason = "FS2_entropy_cap"

        logs.append({
            "step": t, "epsilon": eps, "entropy": ent, "VFE": vfe,
            "comm_norm": comm, "kill_reason": kill_reason
        })

        if kill_reason:
            # cut exploration
            break

    # Execution phase (no exploration)
    # (In production you’d use P to condition Bruce; here just re-run plan)
    plan = task.propose_plan(P, context)
    out  = task.execute(plan)
    util = task.metric(out)

    # Gates (force pure Python types)
    P1 = P.copy()
    novelty = float(max(emd_spectra(P0, P1), bures_distance(P0, P1)))
    slope_c, p_c = linear_trend_pvalue(np.array(com_hist))
    slope_v, p_v = linear_trend_pvalue(np.array(vfe_hist))

    slope_c = float(slope_c); p_c = float(p_c)
    slope_v = float(slope_v); p_v = float(p_v)

    ent0 = float(ent_hist[0]); ent_max = float(max(ent_hist))
    cap = float(cap)
    ent_up = (ent_max - ent0) > 0.0
    ent_ok = ent_max <= cap

    base_metric = float(base_metric)
    util = float(util)
    uplift = util - base_metric

    g1 = bool(novelty > float(cfg["novelty_threshold"]))
    g2 = bool((slope_c < 0.0) and (p_c < float(cfg["pval_threshold"])))
    g3 = bool((slope_v < 0.0) and (p_v < float(cfg["pval_threshold"])))
    g4 = bool(ent_up and ent_ok)
    g5 = bool(uplift >= float(cfg["utility_uplift_min"]))

    gates = {
        "G1_novelty": g1,
        "G2_align_slope": g2,
        "G3_vfe_down": g3,
        "G4_entropy_bounded": g4,
        "G5_utility": g5
    }
    pass_all = bool(all(gates.values()))

    # Write CSV log (unchanged)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(logs[0].keys()))
        w.writeheader()
        w.writerows(logs)

    report = {
        "novelty": novelty,
        "slope_comm": slope_c, "p_comm": p_c,
        "slope_vfe": slope_v,  "p_vfe": p_v,
        "entropy_cap": cap, "entropy_max": ent_max,
        "utility_baseline": base_metric, "utility_c3": util, "uplift": uplift,
        "gates": {k: bool(v) for k, v in gates.items()},
        "class3_pass": pass_all
    }
    return report

# ---------- Entry point ----------
if __name__ == "__main__":
    import os, json
    import yaml

    # Load config.yaml from the same directory as this file
    cfg_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    # --- Toy task (leave in until you wire Bruce) ---
    ints = [7, 2, 9, 1, 6, 4, 8, 5, 3]
    unit_tests = [lambda out: out["answer"] == sorted(ints)]
    task = Task(unit_tests)

    # Ensure runs/ exists at repo root
    runs_dir = os.path.join(os.getcwd(), "runs")
    os.makedirs(runs_dir, exist_ok=True)

    # Run and report
    report = run_class3(ints, cfg, task, log_path=os.path.join(runs_dir, "run1.csv"))
  print(json.dumps(report, indent=2, cls=NpEncoder))

