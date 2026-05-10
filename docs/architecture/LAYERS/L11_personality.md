# L11 — Portable Conditioning Bundle

## Current Rating: 22

_Voice/pact YAML encode conditioning text for prompts, but hedging removal / conditioning enforcement is **not** automated beyond supplying instructions to upstream LLMs._

## Spec Rating (STATE.yaml): 22

## Delta: 0 post calibration.

## Shipped Components

- Shares artifacts with **L1 Mantle** (`mantle/*.yaml`, docs/soul prose). No standalone personality runtime.

## Spec Claims

| Claim | Evidence | Verdict |
|-------|----------|---------|
| Personality grown vs prompted | Still prompt-mediated | BUILD_INCOMPLETE |
| Hedging removal | Guidance only | BUILD_INCOMPLETE |

## Gap Analysis

Treat L11 advances jointly with Mantle + SIPHON memory until dedicated conditioning validators ship.
