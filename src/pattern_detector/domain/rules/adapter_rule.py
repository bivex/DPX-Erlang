"""Erlang Adapter Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AdapterPatternRule(BasePatternRule):
    """Detects Adapter pattern in Erlang modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ADAPTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if mod.name.endswith("_adapter") or "adapter" in mod.name.lower():
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' adapts underlying subsystem or protocol to standard Erlang/OTP module interface",
                        weight=0.75,
                        rule_code="ADAPTER_NAMING_AND_CONVERSION",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="adapter_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
