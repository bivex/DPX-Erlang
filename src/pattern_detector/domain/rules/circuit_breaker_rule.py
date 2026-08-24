"""Erlang Circuit Breaker Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CircuitBreakerRule(BasePatternRule):
    """Detects Circuit Breaker resilience patterns in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CIRCUIT_BREAKER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "fuse:run" in src or "circuit_breaker" in mod.name.lower() or "breaker" in mod.name.lower() or ("tripped" in src and "closed" in src and "half_open" in src):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements Circuit Breaker fault-tolerance pattern preventing cascading external failures",
                        weight=0.80,
                        rule_code="CIRCUIT_BREAKER_RESILIENCE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="circuit_breaker_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
