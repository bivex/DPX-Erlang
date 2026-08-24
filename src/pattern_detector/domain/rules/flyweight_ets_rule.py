"""Erlang Flyweight / ETS Shared Cache Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FlyweightEtsRule(BasePatternRule):
    """Detects Flyweight / ETS / persistent_term shared memory patterns in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FLYWEIGHT_ETS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "ets:new(" in src or "persistent_term:get" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' leverages ETS / persistent_term shared memory cache for zero-copy concurrent read access",
                        weight=0.80,
                        rule_code="FLYWEIGHT_ETS_CACHE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="ets_flyweight_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
