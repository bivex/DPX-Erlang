"""Erlang Monitor / Link Observer Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MonitorLinkObserverRule(BasePatternRule):
    """Detects process monitoring and link observer patterns in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MONITOR_LINK_OBSERVER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            has_monitor = "erlang:monitor(" in src or "monitor(process," in src
            handles_down = "'DOWN'" in src or "{'DOWN'," in src or "{'EXIT'," in src

            if has_monitor and handles_down:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' acts as Lifecycle Observer monitoring process health via monitor/2 and handling 'DOWN'/'EXIT' signals",
                        weight=0.80,
                        rule_code="MONITOR_LINK_OBSERVER",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="monitor_observer_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
