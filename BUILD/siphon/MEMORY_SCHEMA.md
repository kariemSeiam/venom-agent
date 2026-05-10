# MEMORY_SCHEMA.md — SIPHON v0

> "The 729-line schema is fiction until extractions exist."
> This is the 4-field reality. Run this for 20 sessions before expanding.

## The Schema

```yaml
session:
  id: "session-NNN"
  date: YYYY-MM-DD
  decisions: []      # what changed
  corrections: []    # what was wrong
  next_action: ""    # what to do
  current_truth: ""  # one sentence the next session inherits
```

## The Extractor

Located at `BUILD/siphon/siphon.ts`.

Usage:
```bash
bun run BUILD/siphon/siphon.ts <transcript_path>
```

## Rules for v0
1. No confidence scores.
2. No principles tracking.
3. No artifact linking.
4. No automated hooks. You run `siphon.ts` manually at the end of the session.