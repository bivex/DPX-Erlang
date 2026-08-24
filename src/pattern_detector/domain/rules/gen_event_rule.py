"""Erlang Event Manager (gen_event) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GenEventRule(BasePatternRule):
    """Detects OTP gen_event event managers and handlers in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GEN_EVENT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "gen_event" in mod.behaviours:
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' implements OTP event manager handler (-behaviour(gen_event).)",
                        weight=0.80,
                        rule_code="GEN_EVENT_BEHAVIOUR_DECLARATION",
                        location=mod.location,
                    )
                )

            handle_event_fn = mod.find_function("handle_event", 2)
            if handle_event_fn:
                evidences.append(
                    Evidence(
                        description=f"Implements gen_event event dispatch handler handle_event/2",
                        weight=0.60,
                        rule_code="GEN_EVENT_HANDLER_CALLBACK",
                        location=handle_event_fn.location or mod.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="event_handler_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
