#!/usr/bin/env python3
"""
A11yRatchet Deterministic Engine (Ativo Experimental Real para EXP-H3).

Converte resultados automatizados (`axe-core` / Lighthouse JSON) para cláusulas técnicas
da WCAG 2.2 Nível AA e da Norma Europeia EN 301 549 V3.2.1 (Capítulo 9 — Web),
e executa o comparador de Baseline/Ratchet para bloquear Pull Requests somente
quando há introdução de novas violações líquidas.

Inclui obrigatoriamente o aviso legal de não-certificação exigido pela governança.
"""

import hashlib
from typing import Any, Dict, List, Set

LEGAL_TECHNICAL_DISCLAIMER = (
    "TECHNICAL ENGINEERING TOOL DISCLAIMER: A11yRatchet performs automated static/DOM rule checks "
    "(covering ~30%-40% of WCAG criteria). Automated testing cannot verify full accessibility and "
    "must be combined with manual keyboard and screen-reader testing. This report is for software "
    "engineering regression control only and DOES NOT constitute legal advice, a VPAT, or official "
    "EAA / EN 301 549 / ADA legal certification."
)

AXE_TO_WCAG_EN301549_MAP: Dict[str, Dict[str, str]] = {
    "color-contrast": {
        "wcag_sc": "1.4.3 Contrast (Minimum) (Level AA)",
        "en_301_549_clause": "9.1.4.3 Contrast (minimum)",
        "impact_default": "serious",
    },
    "image-alt": {
        "wcag_sc": "1.1.1 Non-text Content (Level A)",
        "en_301_549_clause": "9.1.1.1 Non-text content",
        "impact_default": "critical",
    },
    "label": {
        "wcag_sc": "1.3.1 Info and Relationships / 4.1.2 Name, Role, Value",
        "en_301_549_clause": "9.1.3.1 Info and relationships / 9.4.1.2 Name, role, value",
        "impact_default": "critical",
    },
    "button-name": {
        "wcag_sc": "4.1.2 Name, Role, Value (Level A)",
        "en_301_549_clause": "9.4.1.2 Name, role, value",
        "impact_default": "critical",
    },
    "link-name": {
        "wcag_sc": "2.4.4 Link Purpose (In Context) (Level A)",
        "en_301_549_clause": "9.2.4.4 Link purpose (in context)",
        "impact_default": "serious",
    },
    "html-has-lang": {
        "wcag_sc": "3.1.1 Language of Page (Level A)",
        "en_301_549_clause": "9.3.1.1 Language of page",
        "impact_default": "serious",
    },
    "aria-required-attr": {
        "wcag_sc": "4.1.2 Name, Role, Value (Level A)",
        "en_301_549_clause": "9.4.1.2 Name, role, value",
        "impact_default": "critical",
    },
    "target-size": {
        "wcag_sc": "2.5.8 Target Size (Minimum) (WCAG 2.2 Level AA)",
        "en_301_549_clause": "9.2.5.8 Target size (minimum) (WCAG 2.2 AA alignment)",
        "impact_default": "serious",
    },
}


class A11yRatchetEngine:
    @staticmethod
    def _fingerprint(rule_id: str, selector: str) -> str:
        raw = f"{rule_id.strip().lower()}::{selector.strip()}"
        return "A11Y-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12].upper()

    def evaluate_ratchet(
        self,
        baseline_violations: List[Dict[str, Any]],
        current_violations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        base_fps: Set[str] = set()
        for v in baseline_violations:
            rule_id = v.get("id", "unknown-rule")
            for node in v.get("nodes", [{"target": [v.get("selector", "body")]}]):
                selector = ",".join(node.get("target", ["body"]))
                base_fps.add(self._fingerprint(rule_id, selector))

        mapped_current: List[Dict[str, Any]] = []
        new_regressions: List[Dict[str, Any]] = []
        current_fps: Set[str] = set()

        for v in current_violations:
            rule_id = v.get("id", "unknown-rule")
            clause_info = AXE_TO_WCAG_EN301549_MAP.get(
                rule_id,
                {
                    "wcag_sc": "WCAG 2.1/2.2 General Technical Criterion",
                    "en_301_549_clause": "Section 9 (Web Technical Requirement)",
                    "impact_default": v.get("impact", "moderate"),
                },
            )
            nodes = v.get("nodes", [{"target": [v.get("selector", "body")]}])
            for node in nodes:
                selector = ",".join(node.get("target", ["body"]))
                fp = self._fingerprint(rule_id, selector)
                current_fps.add(fp)
                item = {
                    "fingerprint": fp,
                    "rule_id": rule_id,
                    "selector": selector,
                    "impact": v.get("impact", clause_info["impact_default"]),
                    "wcag_criterion": clause_info["wcag_sc"],
                    "en_301_549_clause": clause_info["en_301_549_clause"],
                    "is_new_regression": fp not in base_fps,
                }
                mapped_current.append(item)
                if fp not in base_fps:
                    new_regressions.append(item)

        fixed_legacy_count = len(base_fps - current_fps)

        return {
            "ratchet_gate_passed": len(new_regressions) == 0,
            "baseline_violations_count": len(base_fps),
            "current_violations_count": len(current_fps),
            "new_regressions_count": len(new_regressions),
            "fixed_legacy_violations_count": fixed_legacy_count,
            "new_regressions": new_regressions,
            "mapped_report": mapped_current,
            "legal_disclaimer": LEGAL_TECHNICAL_DISCLAIMER,
        }
