# INTAKE — Data Validation Protocol
## The Filter Between the World and VENOM

> Every piece of data that enters this folder either advances the architecture
> or gets logged to WIPED.md. There is no neutral.

---

## How Data Enters VENOM

**Step 1: Land in QUEUE.md**
All incoming data (papers, repos, ideas, audits, comparisons, conversations) goes to QUEUE.md first. Nothing goes directly into LAYERS/ or BUILD/.

**Step 2: Run the filter**
Apply the four questions below.

**Step 3: Route or wipe**
- PASSES → route to correct destination (see routing table)
- FAILS → log reason in WIPED.md, discard

---

## The Four Filter Questions

```
Q1. LAYER MAPPING
    Which layer does this data touch?
    → If it maps to a layer: which one, and what's that layer's rating?
    → If it maps to a layer > 90%: extra scrutiny required (don't polish what works)
    → If it maps to no layer: very strong justification needed

Q2. PRINCIPLE ALIGNMENT
    Does it strengthen or weaken the 8 Prime Principles?
    → P1: Does it distribute or centralize intelligence?
    → P2: Does it use constraints as forcing functions?
    → P3: Does it protect identity through depth?
    → P4: Does it optimize the interface cost?
    → P5: Does it enable clean death and real continuity?
    → P6: Does it prepare for visible futures?
    → P7: Does it enforce rather than request?
    → P8: Does it let personality emerge from work?
    If it violates P1, P3, or P5 → WIPE unless explicit Pigo override.

Q3. MEASUREMENT PRESENT?
    Does it include numbers, benchmarks, ratios, or implementation paths?
    → YES: score 2 points
    → NO: score 0 points, flag as "concept only"
    → Pure concept with no path: lean toward WIPE

Q4. SIPHON GATE
    Does this remove a BLOCKER or enable a BLOCKED layer?
    → If YES → PRIORITY intake, goes to top of queue
    → If NO → standard intake
```

**Score the data:**
- Passes Q2 (all principles intact): +2
- Maps to layer < 70%: +2
- Maps to THE BLOCKER (L8): +3
- Measurement present: +2
- Enables BLOCKED layer: +2
- Maps to layer > 90%: -2
- Violates any principle: -3
- Architecture intoxication (beautiful, no path): -4

**Score ≥ 3 → INTAKE**
**Score 0-2 → conditional (needs justification)**
**Score < 0 → WIPE**

---

## Architecture Intoxication Test
*(The most dangerous failure mode)*

Ask: "Does this make the architecture more beautiful without moving any rating number?"

If YES → WIPE. Log it.

Signs of architecture intoxication:
- New metaphor that maps elegantly to octopus biology
- Adds a new layer name without implementation path
- Describes a behavior VENOM should have without how to build it
- References to other systems' elegance without stealing their mechanics

**The antidote:** extract the principle behind the beauty. If the principle already exists in P1-P8, WIPE the data. If it's a genuinely new principle, add it carefully.

---

## Routing Table

| Data Type | Destination |
|-----------|-------------|
| Research paper / external audit | `COMPARE/` → extract steal to `COMPARE/_STEAL.md` |
| Open source repo analysis | `COMPARE/[tool].md` |
| New architecture idea | `INTAKE/QUEUE.md` → filter → LAYERS/ if passes |
| Implementation (code) | `BUILD/[component]/` |
| Session extraction | `MEMORY/MEMORY.md` (append-only) |
| Behavioral correction | `MEMORY/corrections.yaml` |
| New artifact / reusable output | `MEMORY/SACK.md` (index entry) |
| Layer rating update | `STATE.yaml` (layers section) |
| Rejected data | `INTAKE/WIPED.md` |

---

## QUEUE.md Format

When adding to queue, use this format:

```yaml
- id: Q001
  date: YYYY-MM-DD
  source: "description of where this came from"
  type: paper | repo | idea | audit | conversation | tool
  summary: "one sentence — what is this"
  maps_to_layer: L8 | L4 | null
  score: [calculated above]
  status: PENDING | APPROVED | WIPED
  routed_to: null | COMPARE/x.md | LAYERS/Lx.md | BUILD/x/
```

---

## WIPED.md Format

Nothing is truly gone — it's logged so we don't intake the same bad data twice.

```yaml
- id: W001
  date: YYYY-MM-DD
  source: "what was this"
  wipe_reason: "architecture_intoxication | duplicate | violates_principle | no_path | layer_too_complete"
  what_it_was: "brief description"
  recoverable: false | true (if principle survives, describe it)
```

---

## Priority Override

The following always go to top of queue regardless of score:

1. Anything that directly builds SIPHON (L8)
2. Anything that enables two-arm parallel execution (L4 MVP)
3. Behavioral corrections (always valuable, append immediately)
4. External validation of VENOM ratings (competing audit)

---

*The filter is not gatekeeping. It's metabolism.*
*The octopus doesn't eat everything in the ocean.*
*It eats what grows the arm.*
