"""Erlang Behaviour Callback Compliance Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BehaviourCallbackComplianceRule(BasePatternRule):
    """Checks that modules declaring -behaviour(gen_server) implement all required callbacks."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BEHAVIOUR_CALLBACK_COMPLIANCE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "gen_server" in mod.behaviours:
                missing = []
                for req_fn, req_arity in [("init", 1), ("handle_call", 3), ("handle_cast", 2), ("handle_info", 2)]:
                    if not mod.find_function(req_fn, req_arity):
                        missing.append(f"{req_fn}/{req_arity}")

                if missing:
                    evidences = [
                        Evidence(
                            description=f"Behaviour Non-Compliance: Module '{mod.name}' declares -behaviour(gen_server) but is missing mandatory callback(s): {', '.join(missing)}",
                            weight=0.85,
                            rule_code="BEHAVIOUR_MISSING_CALLBACKS",
                            location=mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=mod.name,
                        target_kind="non_compliant_module",
                        evidences=evidences,
                        location=mod.location,
                    )
                    detections.append(det)

        return detections
