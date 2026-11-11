# A11yRatchet — WCAG 2.2 AA & EN 301 549 CI Baseline Ratchet for `axe-core`

[![A11yRatchet Edge Gate](https://img.shields.io/badge/Live_Gate-A11yRatchet_Edge-purple)](https://specgate.profalexandrezamboni.workers.dev/tools/wcag-2-2-en-301-549-ci-gate)

**A11yRatchet** freezes legacy accessibility debt in brownfield web apps using a monotonic per-rule baseline ratchet while blocking net-new `axe-core` regressions mapped deterministically to **WCAG 2.2 AA** and **European Accessibility Act (`EN 301 549 V3.2.1` Chapter 9)** clauses.

- **Interactive WCAG 2.2 & EN 301 549 Evaluator:** https://specgate.profalexandrezamboni.workers.dev/tools/wcag-2-2-en-301-549-ci-gate
- **Comparison: A11yRatchet vs. axe-linter vs. pa11y-ci:** https://specgate.profalexandrezamboni.workers.dev/compare/a11yratchet-vs-axe-linter-vs-pa11y-ci
- **Full Technical Reference (`llms-full.txt`):** https://specgate.profalexandrezamboni.workers.dev/llms-full.txt

## Direct Engineering Comparison

| Capability | `axe-linter` | `pa11y-ci` | **A11yRatchet** |
| :--- | :--- | :--- | :--- |
| **Rendered CSS Contrast & Target Size** | No (static AST) | Yes | **Yes (ingests rendered `axe-core` JSON)** |
| **Legacy Adoption** | Changed lines | Coarse global `--threshold` | **Zero-noise per-rule monotonic ratchet** |
| **EN 301 549 `9.x.y.z` Clause Table** | WCAG tags | WCAG codes | **Native WCAG 2.2 AA + EN 301 549 Mapper** |

> *Compliance Scope Note:* Automated DOM checks detect ~30–40% of WCAG 2.2 / EN 301 549 criteria and complement manual assistive-technology testing.
