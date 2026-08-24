"""Erlang Decorator / Interceptor Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DecoratorWrapperRule(BasePatternRule):
    """Detects Decorator / Interceptor modules in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DECORATOR_WRAPPER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "middleware" in mod.name.lower() or "decorator" in mod.name.lower() or "interceptor" in mod.name.lower():
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' acts as Decorator / Interceptor layering behavior (telemetry, auth, logging) over callback handlers",
                        weight=0.75,
                        rule_code="DECORATOR_INTERCEPTOR_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="decorator_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
