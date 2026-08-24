"""Erlang KISS Rule (excessive pattern matching clauses)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class KissRule(BasePatternRule):
    """Detects KISS violations (functions with excessive pattern match clauses >= 10)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.KISS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                if len(fn.clauses) >= 10:
                    evidences = [
                        Evidence(
                            description=f"KISS Violation (High Complexity): Function '{fn.id_str}' in '{mod.name}' defines {len(fn.clauses)} pattern-matching clauses; consider decomposing",
                            weight=0.75,
                            rule_code="KISS_EXCESSIVE_CLAUSES",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="complex_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
