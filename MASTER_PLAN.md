# MASTER PLAN — Build Tonight (Semantic Group Chat Search)

Everything gets done tonight. No "tomorrow" phase. Work top to bottom, phase by phase. **After finishing each phase, stop and fill in the matching section of `PROGRESS_LOG.md` before moving on** — that's your insurance policy if you get tired, switch tools, or something breaks and you need another AI to pick up exactly where you left off.

Reference `PROJECT_BRIEF.md` for the full spec/contract — this file is just the sequence and timing.

---

## Phase 1 — Corpus generation (~30–40 min)
- [ ] Ask Antigravity to write a Python script generating 5,000–6,000 messages matching the data model (8 participants, 6 months, Hinglish/typos/emojis/short replies/forwards, 3 named decision threads: trip, college event, group purchase)
- [ ] Run it, save output to `/data/messages.json`
- [ ] Spot-check ~30 random messages — reject and regenerate if it reads too clean/robotic
- [ ] **→ Update PROGRESS_LOG.md: Phase 1**

## Phase 2 — Eval set generation (~20–30 min)
- [ ] Feed the real generated corpus back to the AI, ask it to produce 40 ground-truth queries (12 semantic / 10 attributed / 8 temporal / 10 mixed), each with a real `expected_message_id` pulled from the actual corpus
- [ ] Manually verify at least 10 of these have zero word overlap with their answer message (this is a required, graded criterion — don't skip verifying it)
- [ ] Save to `/data/eval_set.json`
- [ ] **→ Update PROGRESS_LOG.md: Phase 2**

## Phase 3 — Repo skeleton + embeddings (~30 min)
- [ ] `/backend`, `/frontend`, `/data` folders, git init, first commit
- [ ] Install sentence-transformers, embed all messages with a small local model (e.g. `all-MiniLM-L6-v2`)
- [ ] Save vectors to `.npy`, don't re-embed on every run
- [ ] Sanity check: two known-similar messages → high cosine similarity
- [ ] **→ Update PROGRESS_LOG.md: Phase 3**

## Phase 4 — Search core (~40 min)
- [ ] `embed_query()`, `cosine_similarity_search()`
- [ ] `parse_query()` — rule-based speaker detection (match against the 8 names) + date-phrase parsing relative to fixed reference date **Sept 1, 2026**
- [ ] Apply speaker/date filters alongside similarity ranking
- [ ] `expand_context()` — ±3 messages around each hit
- [ ] **→ Update PROGRESS_LOG.md: Phase 4**

## Phase 5 — API (~25 min)
- [ ] `POST /search` wiring everything together per the contract in PROJECT_BRIEF.md
- [ ] Manually test one query of each type (semantic / attributed / temporal)
- [ ] **→ Update PROGRESS_LOG.md: Phase 5**

## Phase 6 — Frontend (~25 min)
- [ ] One plain page: search box → results with sender/timestamp/text/similarity/context
- [ ] Wire to `/search`. Minimal styling only.
- [ ] **→ Update PROGRESS_LOG.md: Phase 6**

## Phase 7 — Eval run (~20 min)
- [ ] Script runs all 40 eval queries through search, checks expected_message_id in top-1/3/5/10
- [ ] Print Recall@1/3/5/10
- [ ] If zero-overlap queries score badly, tweak (e.g. try a slightly larger embedding model, or adjust top_k) — but don't rabbit-hole this
- [ ] **→ Update PROGRESS_LOG.md: Phase 7**

## Phase 8 — README + wrap (~15 min)
- [ ] README: what it does, architecture diagram, how to run, eval results table
- [ ] Push to GitHub, confirm public
- [ ] Run the strongest zero-overlap demo query live once more, confirm it works
- [ ] **→ Update PROGRESS_LOG.md: Phase 8 — mark FULLY DONE**

---

## Cut list if you run low on time (in order of what to sacrifice)
1. Frontend styling
2. Fancy quantity/weighted logic anywhere ambiguous — keep equal-split
3. Eval set size (25 solid > 40 rushed) — but never drop below the 10 zero-overlap queries
4. Never cut: the 3 required query types, context expansion, one working zero-overlap demo
