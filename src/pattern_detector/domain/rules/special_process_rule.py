"""Erlang Special Process (proc_lib / sys) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SpecialProcessRule(BasePatternRule):
    """Detects OTP-compliant special processes using proc_lib and sys."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SPECIAL_PROCESS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if ("proc_lib:spawn" in src or "proc_lib:start" in src) and ("sys:init_ack" in src or "sys:handle_system_msg" in src):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements OTP special process protocol complying with sys / proc_lib system messages",
                        weight=0.80,
                        rule_code="SPECIAL_PROCESS_OTP_COMPLIANT",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="special_process_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
