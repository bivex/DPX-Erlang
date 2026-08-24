"""Erlang Supervisor Restart Storm Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SupervisorRestartStormRule(BasePatternRule):
    """Detects dangerous supervisor intensity/period thresholds risking node termination storms."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SUPERVISOR_RESTART_STORM

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "supervisor" in mod.behaviours:
                init_fn = mod.find_function("init", 1)
                if init_fn:
                    body = init_fn.full_body
                    # Matches #{intensity => N, period => M}
                    intensity_match = re.search(r"intensity\s*=>\s*([0-9]+)", body)
                    period_match = re.search(r"period\s*=>\s*([0-9]+)", body)
                    if intensity_match and period_match:
                        intensity = int(intensity_match.group(1))
                        period = int(period_match.group(1))
                        if intensity >= 100 and period <= 1:
                            evidences = [
                                Evidence(
                                    description=f"Resilience Risk: Supervisor '{mod.name}' configured with high intensity ({intensity}) in short period ({period}s) risking restart storms",
                                    weight=0.80,
                                    rule_code="SUPERVISOR_RESTART_STORM_THRESHOLDS",
                                    location=init_fn.location or mod.location,
                                )
                            ]
                            det = self._create_detection(
                                target_name=mod.name,
                                target_kind="supervisor_module",
                                evidences=evidences,
                                location=mod.location,
                            )
                            detections.append(det)

        return detections
