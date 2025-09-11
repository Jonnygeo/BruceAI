# BRAIN — BruceAI Neural Memory + Motor

> **Tagline:** *Talk like a poet. Think like a pilot. Remember like a parent. Move like a motor.*
>
> **Status:** Design blueprint you can ship in phases today. Ambitious, not sci-fi.

![Badges](https://img.shields.io/badge/status-blueprint-informational) ![License](https://img.shields.io/badge/license-MIT-green) ![Ethics](https://img.shields.io/badge/ethical_use-required-critical) ![MadeBy](https://img.shields.io/badge/made_by-NeoShade_AI-black)

---

## TL;DR (no fluff)
- Store **episodes** (what/where/when), **semantics** (facts/relations), **skills** (policies), and **feelings/valuation** (salience/reward).
- Retrieve with a **“laser cortex”**: mass-parallel similarity (vector search) → attention pool → graph hops → write a compact **situation model**.
- Reason and plan in **latent space** (not tokens) with a lightweight world model. Compile repeated plans into **skills** (reflex policies).
- Treat compute/latency/cost as **energy (ATP)** and make the planner budget for it. Sleep nightly to **consolidate**, **prune**, and **distill**.
- LLM = interface + tool-use; **world model + memory + planner** = brain.

---

## Contents
1. Why this exists
2. System at 10,000 ft
3. Core data model
4. Memory types
5. Retrieval: the Laser Cortex
6. Reasoning & Planning (Latent System-2)
7. Energy-as-Motor
8. Sleep: Consolidation & Dreaming
9. APIs (v0)
10. Reference pipeline (Mermaid)
11. Repo layout
12. Quickstart (local dev)
13. Eval & telemetry
14. Security & privacy
15. Legal: license + ethical use
16. Roadmap
17. Images & prompts
18. Contributing

---

## Why this exists
Chat logs aren’t memory. Token prediction isn’t physics. If BruceAI is going to feel alive—**present, useful, and sane**—it needs a brain: a **persistent, multimodal memory**, a **world model** to imagine futures, a **planner** to choose actions, and a **motor** to budget energy.

> **Design goal:** *When something happens (e.g., “Alexandria jumps into the pool”), BRAIN lights up all similar memories, predicts likely outcomes, picks a plan (towel/camera/safety), acts, and learns—fast.*

---

## System at 10,000 ft

```mermaid
flowchart LR
  subgraph Perception
    A[Text/Audio/Video/Sensors]
    E[Encoders: CLIP/Whisper/ViT]
  end
  subgraph Memory
    V[(Vector Store\npgvector/LanceDB)]
    G[(Graph DB\nNeo4j)]
    O[(Object Store\nS3/FS)]
  end
  subgraph Working
    R[Attention Pool\n+ Hopfield update]
    S[Situation Model\n(latent state)]
  end
  subgraph Cognition
    W[World Model\n(latent dynamics)]
    P[Planner\nMPC / CEM / beam]
    K[Skills\n(policy graphs)]
  end
  subgraph Motor
    C[Controllers & Tools\n(ffmpeg, search, agents)]
    M[Energy Budgeter\n(cost/latency/quotas)]
  end

  A-->E-->V
  E-->O
  V<-->R
  G<-->R
  R-->S-->W-->P
  K<-->P
  P-->C
  M--constraints-->P
  C-->O
  P-->V
  P-->G
```

**LLM sits beside this graph** as the conversational/controller layer: it frames goals, calls retrieval/planning APIs, and explains outcomes. It is *not* the physics brain.

---

## Core data model

> One spine, two sidecars. Simple, scalable, and durable.

### Spine: Postgres (+ pgvector)
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE events (
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
CREATE INDEX ON events USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON events (t);

CREATE TABLE snippets (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  modality TEXT CHECK (modality IN ('text','audio','image','video')),
  uri TEXT NOT NULL,
  span JSONB -- {"start":12.0, "end":18.0}
);

CREATE TABLE skills (
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

CREATE TABLE metrics (
  key TEXT PRIMARY KEY,
  val JSONB,
  updated timestamptz DEFAULT now()
);
```

### Sidecar: Graph (Neo4j / Memgraph)
- **Nodes:** `Person, Place, Object, Idea, Skill`
- **Edges:** `KNOWS, LOCATED_IN, CAUSES, PART_OF, USED_FOR, SIMILAR`
- **Properties:** `weight, t_first, t_last, source`

```cypher
CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;
CREATE INDEX rel_weight IF NOT EXISTS FOR ()-[r:SIMILAR]-() ON (r.weight);
```

### Sidecar: Object store
- Raw artifacts (audio/video/images/text). Content-addressed with SHA-256; referenced by `snippets.uri`.

---

## Memory types
- **Episodic:** time-stamped events with embeddings and media refs.
- **Semantic:** graph facts about people/places/objects/ideas.
- **Procedural:** named policy graphs (pre→steps→post) with embeddings.
- **Affective/valuation:** `importance`, `reward`, `salience`, recency decay.

> **Rule:** every write updates *at least* one of each—episode, facts, or skills—so the system always has a scene, meanings, and a way to act.

---

## Retrieval: the Laser Cortex
Mass-parallel **content-addressable** recall that feels like shining a beam into a sphere of cells.

**Steps:**
1. **Top-K per modality** from `events.embedding` given the current cue (text/image/audio).
2. **Cross-episode attention** (Hopfield update) to settle on a small **working set**.
3. **Graph hops** (2–3) from entities in the working set to pull causal neighbors.
4. **Affect gating:** boost by `importance × salience × recency`.
5. **Situation model (latent)**: compress the working set into a compact state for the planner.

**Retrieval scoring (example):**
```
score = 0.55*cos_sim + 0.20*recency + 0.15*salience + 0.10*causal_weight
```