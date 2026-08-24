"""Erlang Supervisor Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SupervisorRule(BasePatternRule):
    """Detects OTP supervisor behavior and restart strategies in Erlang modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SUPERVISOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "supervisor" in mod.behaviours:
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' explicitly implements OTP supervisor behaviour (-behaviour(supervisor).)",
                        weight=0.70,
                        rule_code="SUPERVISOR_BEHAVIOUR_DECLARATION",
                        location=mod.location,
                    )
                )

            init_fn = mod.find_function("init", 1)
            if init_fn:
                body = init_fn.full_body
                if "one_for_one" in body or "one_for_all" in body or "rest_for_one" in body or "simple_one_for_one" in body:
                    strat = "one_for_one"
                    for s in ["one_for_all", "rest_for_one", "simple_one_for_one", "one_for_one"]:
                        if s in body:
                            strat = s
                            break
                    evidences.append(
                        Evidence(
                            description=f"Defines supervisor restart strategy '{strat}' in init/1",
                            weight=0.60,
                            rule_code="SUPERVISOR_RESTART_STRATEGY",
                            location=init_fn.location or mod.location,
                        )
                    )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="supervisor_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
