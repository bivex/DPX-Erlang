"""Erlang Chain of Responsibility / Middleware Pipeline Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ChainOfResponsibilityRule(BasePatternRule):
    """Detects Chain of Responsibility middleware pipeline traversal in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CHAIN_OF_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                # Looks for list traversal passing request to module head: [Mod | Rest] -> Mod:execute(...) -> loop(Rest)
                if re.search(r"\[\s*[A-Z][a-zA-Z0-9_]*\s*\|\s*[A-Z][a-zA-Z0-9_]*\s*\]", fn.full_body) and ":" in fn.full_body:
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' in '{mod.name}' implements Chain of Responsibility sequentially evaluating handler modules in a pipeline",
                            weight=0.80,
                            rule_code="CHAIN_OF_RESPONSIBILITY_MODULE_LIST",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="middleware_chain_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
