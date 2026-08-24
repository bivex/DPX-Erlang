"""Erlang Single Responsibility (God Module) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SingleResponsibilityModuleRule(BasePatternRule):
    """Detects God Modules in Erlang (excessive exports ≥25 functions)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLE_RESPONSIBILITY_MODULE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            exports_count = len(mod.exports)
            funcs_count = len(mod.functions)

            if exports_count >= 25 or funcs_count >= 35:
                evidences = [
                    Evidence(
                        description=f"SRP Violation (God Module): Module '{mod.name}' exports {exports_count} functions and defines {funcs_count} routines, indicating mixed domain responsibilities",
                        weight=0.85,
                        rule_code="SRP_GOD_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="god_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
