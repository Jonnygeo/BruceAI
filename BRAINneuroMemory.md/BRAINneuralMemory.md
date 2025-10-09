<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>BRAIN — BruceAI Neural Memory + Motor</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net" />
<style>
  :root {
    --bg: #0b0f14;
    --panel: #10151c;
    --text: #e6eef8;
    --muted: #a7b3c2;
    --accent: #69b3ff;
    --accent-2: #75f7c0;
    --code-bg: #0e141b;
    --border: #1e2a38;
  }
  html, body { background: var(--bg); color: var(--text); font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; line-height: 1.6; }
  .wrap { max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }
  h1,h2,h3 { line-height: 1.2; }
  h1 { font-size: 2.1rem; margin: 1rem 0; }
  h2 { font-size: 1.5rem; margin-top: 2rem; border-bottom: 1px solid var(--border); padding-bottom: .4rem; }
  h3 { font-size: 1.15rem; margin-top: 1.25rem; }
  p.lead { color: var(--muted); font-size: 1.05rem; margin-top: .25rem; }
  .tagline { color: var(--accent-2); font-weight: 600; }
  .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.2rem; margin: 1rem 0; }
  .muted { color: var(--muted); }
  code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
  pre { background: var(--code-bg); color: #d7e7ff; border: 1px solid var(--border); border-radius: 10px; padding: 1rem; overflow: auto; }
  code { background: #0c1219; padding: .15rem .35rem; border-radius: 6px; border: 1px solid var(--border); }
  table { width: 100%; border-collapse: collapse; margin: .75rem 0 1.25rem; }
  th, td { border: 1px solid var(--border); padding: .6rem .7rem; vertical-align: top; }
  th { background: #0e141b; text-align: left; }
  .kicker { text-transform: uppercase; letter-spacing: .08em; color: var(--muted); font-size: .82rem; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .footnote { font-size: .9rem; color: var(--muted); }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .badge { display: inline-block; padding: .25rem .5rem; border: 1px solid var(--border); border-radius: 999px; margin-right: .4rem; color: var(--muted); }
  .note { border-left: 3px solid var(--accent); padding-left: .8rem; }
</style>

<!-- Mermaid for diagrams -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
</head>

<body>
  <div class="wrap">
    <h1>🧠 BRAIN — BruceAI Neural Memory + Motor</h1>
    <p class="lead"><span class="tagline">Tagline:</span> Talk like a poet. Think like a pilot. Remember like a parent. Move like a motor.</p>

    <div class="panel">
      <span class="badge">Status: Fully deployable blueprint — ambitious, practical</span>
      <span class="badge">License: MIT</span>
      <span class="badge">Ethics: <code>ETHICAL_USE.md</code></span>
      <span class="badge">Author: Jonny G (Joker Jonny / Hackpen)</span>
    </div>

    <h2>TL;DR — No Fluff</h2>
    <ul>
      <li><strong>Store:</strong> <em>Episodes</em> (what / where / when) · <em>Semantics</em> (facts / relations) · <em>Skills</em> (policies) · <em>Valuation</em> (salience / reward)</li>
      <li><strong>Retrieve:</strong> “Laser Cortex” → vector search → attention pool → graph hops → situation model</li>
      <li><strong>Reason / Plan:</strong> in latent space (not tokens) with a lightweight world model; repeated plans → skills (reflex policies)</li>
      <li><strong>Energy:</strong> treat compute + latency + cost as ATP; planner budgets for it</li>
      <li><strong>Sleep:</strong> nightly consolidation, pruning, and distillation</li>
      <li><strong>LLM = Interface + Tool-Use</strong> · <strong>World Model + Memory + Planner = Brain</strong></li>
    </ul>

    <h2>Why This Exists</h2>
    <p>Chat logs aren’t memory. Token prediction isn’t physics.</p>
    <p>If BruceAI is going to <em>feel alive—present, useful, and sane</em>, it needs a real brain: a persistent multimodal memory, a latent-world model to imagine futures, a planner to choose actions, and a motor that budgets energy.</p>
    <p><strong>Design goal:</strong> when something happens — “child jumps into the pool” — BRAIN lights up similar memories, predicts likely outcomes, chooses a plan (towel / camera / safety), acts, and learns — fast.</p>

    <h2>System at 10,000 ft</h2>
    <div class="panel">
      <div class="mermaid">
flowchart LR
  subgraph Perception
    A[Text · Audio · Video · Sensors]
    E[Encoders<br/>CLIP · Whisper · ViT]
  end

  subgraph Memory
    V[(Vector Store<br/>pgvector · LanceDB)]
    G[(Graph DB<br/>Neo4j)]
    O[(Object Store<br/>S3 / FS)]
  end

  subgraph Working
    R[Attention Pool<br/>+ Hopfield Update]
    S[Situation Model<br/>(Latent State)]
  end

  subgraph Cognition
    W[World Model<br/>(Latent Dynamics)]
    P[Planner<br/>MPC · CEM · Beam]
    K[Skills<br/>(Policy Graphs)]
  end

  subgraph Motor
    C[Controllers & Tools<br/>(ffmpeg · search · agents)]
    M[Energy Budgeter<br/>(cost · latency · quotas)]
  end

  A --> E --> V
  E --> O
  V <--> R
  G <--> R
  R --> S --> W --> P
  K <--> P
  P --> C
  M -- constraints --> P
  C --> O
  P --> V
  P --> G
      </div>
      <p class="note footnote"><strong>Note:</strong> The LLM sits <em>beside</em> this graph as the conversational/controller layer. It frames goals, calls retrieval + planning APIs, and explains outcomes. It is <strong>not</strong> the physics brain.</p>
    </div>

    <h2>Core Data Model</h2>
    <p class="kicker">One spine, two sidecars — simple, scalable, durable.</p>

    <h3>Spine: Postgres (+ pgvector ≥ 0.5)</h3>
    <pre><code class="language-sql">CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS events (
  id UUID PRIMARY KEY,
  t timestamptz NOT NULL,
  who TEXT[],
  what TEXT[],
  where_ TEXT[],
  context JSONB,
  importance REAL DEFAULT 0.0,
  reward REAL DEFAULT 0.0,
  outcome TEXT,
  embedding vector(1024)
);

CREATE INDEX IF NOT EXISTS events_embedding_hnsw
  ON events USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS events_t_idx ON events (t);

CREATE TABLE IF NOT EXISTS snippets (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  modality TEXT CHECK (modality IN ('text','audio','image','video')),
  uri TEXT NOT NULL,
  span JSONB
);

CREATE TABLE IF NOT EXISTS skills (
  id UUID PRIMARY KEY,
  name TEXT UNIQUE,
  description TEXT,
  pre JSONB,
  steps JSONB,
  post JSONB,
  embedding vector(768),
  uses INT DEFAULT 0,
  success REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS metrics (
  key TEXT PRIMARY KEY,
  val JSONB,
  updated timestamptz DEFAULT now()
);</code></pre>

    <div class="panel footnote">
      <strong>Tip:</strong> After bulk loads → <code>ANALYZE events;</code><br />
      For queries → <code>SET hnsw.ef_search = 80;</code> (tune recall / latency)
    </div>

    <h3>Sidecar A: Graph (Neo4j / Memgraph)</h3>
    <pre><code class="language-cypher">CREATE CONSTRAINT person_name IF NOT EXISTS
FOR (p:Person) REQUIRE p.name IS UNIQUE;

CREATE INDEX idea_name IF NOT EXISTS
FOR (i:Idea) ON (i.name);

CREATE INDEX rel_similar_weight IF NOT EXISTS
FOR ()-[r:SIMILAR]-() ON (r.weight);</code></pre>

    <p><strong>Nodes:</strong> Person, Place, Object, Idea, Skill<br />
       <strong>Edges:</strong> KNOWS, LOCATED_IN, CAUSES, PART_OF, USED_FOR, SIMILAR<br />
       <strong>Properties:</strong> weight, t_first, t_last, source</p>

    <h3>Sidecar B: Object Store</h3>
    <ul>
      <li>Raw artifacts (audio / video / images / text)</li>
      <li>Content-addressed via SHA-256</li>
      <li>Referenced by <code>snippets.uri</code></li>
    </ul>

    <h2>Memory Types</h2>
    <table>
      <thead><tr><th>Type</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><strong>Episodic</strong></td><td>Time-stamped events with embeddings + media refs</td></tr>
        <tr><td><strong>Semantic</strong></td><td>Graph facts about people / places / objects / ideas</td></tr>
        <tr><td><strong>Procedural</strong></td><td>Named policy graphs (pre → steps → post) with embeddings</td></tr>
        <tr><td><strong>Affective / Valuation</strong></td><td>Importance · Reward · Salience · Recency Decay</td></tr>
      </tbody>
    </table>
    <p><strong>Rule:</strong> Every write must update ≥ 1 of each — episode, facts, or skills — so the system always has a scene, meaning, and a way to act.</p>

    <h2>Retrieval — The Laser Cortex</h2>
    <p>Mass-parallel content-addressable recall — like shining a beam into a sphere of cells.</p>
    <h3>Steps</h3>
    <ol>
      <li>Top-K per modality from <code>events.embedding</code> given the current cue (text / image / audio).</li>
      <li>Cross-episode attention (Hopfield update) → settle on a working set.</li>
      <li>Graph hops (2–3) from entities in the set → causal neighbors.</li>
      <li>Affect gating: boost by <code>importance × salience × recency</code>.</li>
      <li>Situation model (latent): compress the set → compact state for planner.</li>
    </ol>

    <h3>Retrieval Score (example)</h3>
    <pre><code class="language-sql">SELECT id,
  0.55*(1 - (embedding <=> :q)) +       -- cosine similarity
  0.20*GREATEST(0,1 - EXTRACT(EPOCH FROM (now()-t))/86400.0/30) +
  0.15*COALESCE(importance,0) +
  0.10*COALESCE(reward,0) AS score
FROM events
ORDER BY score DESC
LIMIT 50;</code></pre>

    <h2>Reasoning &amp; Planning (Latent System-2)</h2>
    <ul>
      <li>Use latent world model <code>W</code> for rollouts and hypothesis testing.</li>
      <li>Use planner <code>P</code> (MPC / CEM / beam) to evaluate cost vs reward.</li>
      <li>Compile repeated plans into <strong>Skills</strong> (policy graphs).</li>
      <li>Reasoning loop = retrieval → simulation → plan → action → feedback.</li>
    </ul>
    <p><em>All compute, latency, and API costs are treated as energy. Planner budgets like metabolism.</em></p>

    <h2>Energy-as-Motor</h2>
    <ul>
      <li><strong>Energy Budgeter (M):</strong> tracks compute time + token cost + latency.</li>
      <li><strong>Controllers (C):</strong> run plans via tools, agents, or external calls.</li>
      <li><strong>Motor Loop:</strong> plan → budget → execute → learn → refine.</li>
      <li>If budget violated → system backs off (“fatigue”).</li>
    </ul>

    <h2>Sleep / Dreaming / Consolidation</h2>
    <ol>
      <li><strong>Replay</strong> recent episodes by importance &amp; salience.</li>
      <li><strong>Cluster</strong> similar embeddings → compress memory.</li>
      <li><strong>Distill</strong> repeated plans into skills.</li>
      <li><strong>Prune</strong> low-reward / redundant entries.</li>
      <li><strong>Re-index</strong> vector / graph stores for speed.</li>
    </ol>
    <p>Sleep reduces entropy. Dreaming is compression.</p>

    <h2>APIs (v0)</h2>
    <table>
      <thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead>
      <tbody>
        <tr><td><code>POST</code></td><td><code>/retrieve</code></td><td>cue → episodes + graph expansion → situation model</td></tr>
        <tr><td><code>POST</code></td><td><code>/plan</code></td><td>situation model → plan steps (+ energy budget)</td></tr>
        <tr><td><code>POST</code></td><td><code>/execute</code></td><td>plan → controllers / tools → outcomes</td></tr>
        <tr><td><code>POST</code></td><td><code>/sleep</code></td><td>consolidate → prune → distill skills</td></tr>
      </tbody>
    </table>

    <h2>Reference Pipeline</h2>
    <div class="panel">
      <div class="mermaid">
sequenceDiagram
  participant User
  participant LLM
  participant Memory
  participant Planner
  participant Motor

  User->>LLM: Query / Event
  LLM->>Memory: Retrieve (context vector)
  Memory-->>LLM: Working set (episodes + graph)
  LLM->>Planner: Situation model
  Planner->>Motor: Plan with energy budget
  Motor->>LLM: Execute & report
  LLM-->>User: Response / Reflection
  Note over Memory,Planner: Nightly Sleep = Consolidate & Distill
      </div>
    </div>

    <h2>Repo Layout</h2>
    <pre><code>brain/
  api/
    server.py
    routes/
      retrieve.py
      plan.py
      sleep.py
  core/
    memory/
    planner/
    motor/
  data/
  tests/
docs/
  images/
  diagrams/</code></pre>

    <h2>Quickstart</h2>
    <pre><code class="language-bash">python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn brain.api.server:app --reload</code></pre>

    <h2>Eval &amp; Telemetry</h2>
    <ul>
      <li><strong>Metrics table</strong> logs usage / success / energy.</li>
      <li>Periodic self-tests: retrieval precision, plan success rate, energy per reward.</li>
      <li>Privacy: all telemetry local by default; remote opt-in only.</li>
    </ul>

    <h2>Security &amp; Privacy</h2>
    <ul>
      <li>AES-256 encrypted object store (offline optional).</li>
      <li>Role-based API keys for memory writes.</li>
      <li><code>ETHICAL_USE.md</code> enforced on startup.</li>
      <li>Nightly scrub for PII and token leakage.</li>
    </ul>

    <h2>Legal / Ethical Use</h2>
    <p>BruceAI must never be used to deceive, surveil, or exploit. All derivative systems must retain <code>ETHICAL_USE.md</code> and respect human agency.</p>

    <h2>Roadmap</h2>
    <table>
      <thead><tr><th>Phase</th><th>Goal</th><th>Deliverable</th></tr></thead>
      <tbody>
        <tr><td>1</td><td>Core Memory Spine + Vector Search</td><td>Working pgvector + Neo4j stack</td></tr>
        <tr><td>2</td><td>Laser Cortex Retrieval API</td><td>Attention pool + graph hops</td></tr>
        <tr><td>3</td><td>Latent Planner / Energy Motor</td><td>End-to-end loop (simulate → act → learn)</td></tr>
        <tr><td>4</td><td>Sleep + Dream Cycle</td><td>Consolidation + Skill Distillation</td></tr>
        <tr><td>5</td><td>Full Neural Memory Kernel</td><td>Continuous learning brain runtime</td></tr>
      </tbody>
    </table>

    <h2>Contributing</h2>
    <p>PRs welcome if you understand the ethic and the architecture. Read <code>ETHICAL_USE.md</code> first. Violations = ban. Style guide: clarity &gt; cleverness. Truth &gt; trend.</p>

    <div class="panel">
      <p><strong>Final Note:</strong> This document is not science fiction. It’s a map of how digital cognition can be built ethically, coherently, and consciously. The rest is just code.</p>
    </div>
  </div>
</body>
</html>
