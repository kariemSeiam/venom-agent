# NVIDIA NemoClaw

**Description:** Reference stack for running OpenClaw in OpenShell (NVIDIA Agent Toolkit).
**Key Features:**
- **Sandbox Hardening:** Uses Landlock + seccomp + netns to run agents safely.
- **Model Router:** Uses a lightweight encoder (PrefillRouter v3) to predict and route to the most cost-efficient model for each query.
- Guided onboarding and pre-configured blueprint for OpenClaw agents.
