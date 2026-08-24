"""Erlang Application Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ApplicationRule(BasePatternRule):
    """Detects OTP application callbacks in Erlang modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.APPLICATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "application" in mod.behaviours or (mod.find_function("start", 2) and mod.find_function("stop", 1) and mod.name.endswith("_app")):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' encapsulates top-level OTP Application lifecycle via start/2 and stop/1",
                        weight=0.85,
                        rule_code="APPLICATION_OTP_LIFECYCLE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="application_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
