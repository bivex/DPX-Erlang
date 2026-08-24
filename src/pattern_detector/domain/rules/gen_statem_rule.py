"""Erlang State Machine (gen_statem / gen_fsm) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GenStatemRule(BasePatternRule):
    """Detects OTP gen_statem / gen_fsm finite state machines in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GEN_STATEM

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "gen_statem" in mod.behaviours or "gen_fsm" in mod.behaviours:
                beh = "gen_statem" if "gen_statem" in mod.behaviours else "gen_fsm"
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' implements OTP state machine behaviour (-behaviour({beh}).)",
                        weight=0.80,
                        rule_code="GEN_STATEM_BEHAVIOUR_DECLARATION",
                        location=mod.location,
                    )
                )

            cb_mode = mod.find_function("callback_mode", 0)
            if cb_mode:
                evidences.append(
                    Evidence(
                        description=f"Defines gen_statem callback mode via callback_mode/0",
                        weight=0.60,
                        rule_code="GEN_STATEM_CALLBACK_MODE",
                        location=cb_mode.location or mod.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="state_machine_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
