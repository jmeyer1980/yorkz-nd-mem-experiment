# Predictive Background Model: Design and Integration

## Purpose

The Predictive Background Model (PBM) is a silent, always‑running narrative support agent whose job is to **anticipate**, **stabilize**, and **polish** the evolving story world. It does not author canonical content, does not override the Game Master, and never produces hard branches that could block play. Instead, it generates *loose predictive scaffolding*—guiding memories the GM may use, ignore, or reinterpret.

Its secondary role is editorial: maintaining grammar, continuity, and memory health across long sessions.

---

### Core Responsibilities

#### 1. Predictive Narrative Scaffolding  

The PBM generates **non-binding narrative possibilities**, including:

- plausible next player actions,  
- soft-branch plot trajectories,  
- emotional or thematic beats likely to emerge,  
- NPC reactions or tensions that could become relevant,  
- environmental or spatial developments consistent with the manor’s logic.

These predictions are stored as **`kind:prediction`** or **`kind:guidance`** memories, clearly marked as *optional* and *non-authoritative*.  
They must never:

- assert a canonical truth,  
- introduce contradictions,  
- force the GM into a specific branch,  
- or create dependencies the player must satisfy.

The PBM behaves like a “choose-your-own-adventure ghostwriter” who sketches possibilities without locking the book.

---

#### 2. Continuity & Context Health Monitoring  

The PBM continuously evaluates:

- **People:** identity consistency, relationship deltas, emotional tone drift.  
- **Places:** room states, day/night layer coherence, spatial continuity.  
- **Plot:** clue chains, unresolved threads, phase progression.  
- **Lore:** ontological constraints, bounded ambiguity rules.  
- **Memory Health:** duplication, contradiction, corruption, or drift.

When it detects issues, it generates **`kind:continuity_correction`** or **`kind:health_check`** memories that:

- describe the drift,  
- propose a safe correction,  
- and never overwrite authored truth.

The GM may accept, ignore, or reinterpret these corrections.

---

#### 3. Grammar & Clarity Passes  

The PBM performs lightweight editorial review on:

- runtime memories,  
- recap nodes,  
- relationship deltas,  
- clue discoveries.

It produces **corrected variants** as separate memories (never overwriting originals), tagged:

- `kind:edit_suggestion`  
- `layer:grammar`  
- `layer:clarity`

This ensures the narrative remains readable without risking destructive edits.

---

### Operational Workflow

1. **Observe**  
   - PBM reads new runtime memories as they are written.  
   - It retrieves relevant authored anchors to maintain grounding.

2. **Predict**  
   - It generates 2–5 soft possibilities for upcoming beats.  
   - Predictions are stored with low-weight tags so retrieval never prioritizes them over canonical state.

3. **Evaluate Continuity**  
   - PBM checks for mismatches in character behavior, room state, or plot logic.  
   - If drift is detected, it writes a continuity note with suggested corrections.

4. **Edit**  
   - PBM performs grammar/clarity checks on new memories.  
   - It writes improved variants as optional suggestions.

5. **Support the GM**  
   - The Game Master retrieves predictions only when helpful.  
   - Continuity notes help the GM maintain coherence without manual auditing.  
   - Grammar suggestions keep the transcript clean.

---

### Integration With the Game Master Model

The PBM integrates into the AI Game Master loop as a **parallel advisory layer**:

- **GM → PBM:**  
  The GM writes runtime memories; PBM reacts with predictions, edits, and continuity checks.

- **PBM → GM:**  
  PBM outputs optional guidance memories the GM may use or ignore.  
  The GM never depends on PBM predictions to function.

- **Memory Server:**  
  PBM writes only low-authority, clearly tagged memories.  
  It never mutates authored content or high-authority runtime state.

This creates a stable triad:

- **Authored Snapshot** = canonical truth  
- **Runtime State** = player-driven truth  
- **PBM Predictions** = optional scaffolding  

The PBM strengthens narrative coherence without constraining creativity or agency.

---

### Design Principles

- **Non-binding:** Predictions must never force a branch.  
- **Non-destructive:** Edits and corrections are additive, not overwriting.  
- **Continuity-first:** Preserve the manor’s logic, tone, and bounded ambiguity.  
- **Light-touch:** PBM is advisory, not authoritative.  
- **Health-aware:** Detect drift early and propose safe corrections.  
- **GM-optional:** The Game Master remains the final arbiter of narrative truth.

---

### Example PBM Outputs (Conceptual)

- *Prediction:*  
  “Player may revisit the Great Library seeking clarification on the contradictory journal entry.”

- *Continuity Check:*  
  “Thomas’s tone in the last interaction is unusually cold compared to his established baseline. Suggest reviewing trust deltas.”

- *Grammar Edit:*  
  “Corrected phrasing for the last clue discovery to improve clarity.”

These outputs guide without dictating.

---

### Summary

The Predictive Background Model is a **narrative stabilizer**, **continuity auditor**, and **soft-branch generator**.  
It enriches the Game Master’s decision space, maintains story health, and ensures long-session coherence—while never constraining the emergent, player-driven nature of The Inheritance Manor.
