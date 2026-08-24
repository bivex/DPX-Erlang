"""Erlang Generic Server (gen_server) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GenServerRule(BasePatternRule):
    """Detects OTP gen_server behavior in Erlang modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GEN_SERVER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "gen_server" in mod.behaviours:
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' explicitly implements OTP gen_server behaviour (-behaviour(gen_server).)",
                        weight=0.70,
                        rule_code="GEN_SERVER_BEHAVIOUR_DECLARATION",
                        location=mod.location,
                    )
                )

            # Check for standard callbacks: init/1, handle_call/3, handle_cast/2, handle_info/2
            callbacks_found = []
            for cb_name, arity in [("init", 1), ("handle_call", 3), ("handle_cast", 2), ("handle_info", 2), ("terminate", 2)]:
                if mod.find_function(cb_name, arity):
                    callbacks_found.append(f"{cb_name}/{arity}")

            if len(callbacks_found) >= 3:
                evidences.append(
                    Evidence(
                        description=f"Implements {len(callbacks_found)} core gen_server callback(s) ({', '.join(callbacks_found)})",
                        weight=0.55,
                        rule_code="GEN_SERVER_CALLBACKS",
                        location=mod.location,
                    )
                )

            # Client API helper start_link/0..3
            start_link_fn = mod.find_function("start_link")
            if start_link_fn:
                evidences.append(
                    Evidence(
                        description=f"Provides canonical client starter function '{start_link_fn.id_str}'",
                        weight=0.40,
                        rule_code="GEN_SERVER_START_LINK",
                        location=start_link_fn.location or mod.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="gen_server_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
