# EVOLUTION LOOP
## How VENOM gets better over time

> Not a process you run once.
> A rhythm you run every session.

---

## The Loop (runs every session)

```
OBSERVE → MEASURE → COMPARE → STEAL → BUILD → VALIDATE → UPDATE
    ↑                                                          |
    └──────────────────────────────────────────────────────────┘
```

### OBSERVE
- Read MEMORY/MEMORY.md — what changed last session?
- Read STATE.yaml — what's the current lowest rating?
- Read INTAKE/QUEUE.md — what new data is waiting?

### MEASURE
- Pick one layer that's < 70%
- Ask: "Can I move this rating up this session, even by 5 points?"
- If yes → that's the target

### COMPARE
- Pick one open-source system from COMPARE/
- Run: "What does it do that VENOM doesn't?"
- Run: "What does VENOM do that it doesn't?"
- Log both in `COMPARE/_STEAL.md` and `EVOLUTION/gaps.md`

### STEAL
- Take one concrete mechanic from the comparison
- Run it through INTAKE/PROTOCOL.md filter
- If it passes → build it or design it

### BUILD
- Implement the target
- Update the layer file in LAYERS/
- Update BUILD/ if code was written

### VALIDATE
- Rate the layer honestly
- Compare to previous rating
- Ask: "Did this actually move the number, or just feel like progress?"

### UPDATE
- Update STATE.yaml
- Append to MEMORY/MEMORY.md
- Update EVOLUTION/ratings_history.yaml

---

## What "Better" Means

Not more features. Not more beautiful architecture.

Better = higher layer rating based on:
1. More of the layer's MISSING items checked off
2. Measurable improvement (compression ratio, response time, token cost)
3. A BLOCKER removed
4. A dependency resolved

**Architecture intoxication = feels like progress without moving a number.**
**Real progress = a number moved. Or a blocker removed.**

---

## Rating Change Protocol

When updating a rating:
1. Write what changed (what was built/implemented)
2. Write why the number moved (specific missing items addressed)
3. Write what's still missing
4. Append to `EVOLUTION/ratings_history.yaml`

```yaml
# ratings_history.yaml entry format
- date: YYYY-MM-DD
  layer: L8_siphon
  rating_before: 12
  rating_after: 25
  delta: +13
  what_changed: "MEMORY.md schema designed. 7 field types defined."
  still_missing: ["extraction prototype", "automation", "VENOCTIS hook"]
  session_ref: "session-003"
```

---

## Validation Questions (ask before claiming a rating increase)

1. "If someone read only the code/files I produced, would they agree the rating went up?"
2. "Did I move a MISSING item to DONE in STATE.yaml?"
3. "Is there a test or measurement that proves the improvement?"
4. "Would this survive the Architecture Intoxication test?"

All four YES → update the rating.
Any NO → rating stays. Note the gap.

---

## The Hard Rule

**Never increase a rating without a concrete artifact.**

Not a plan. Not a design. Not a description.
An artifact: code, schema, spec, protocol, measurement.

Plans are free. Artifacts cost something. Cost = real progress.
