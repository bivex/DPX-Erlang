"""Erlang Composite Supervision Tree Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CompositeSupervisorTreeRule(BasePatternRule):
    """Detects Composite Supervision Trees in Erlang (supervisors supervising sub-supervisors)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMPOSITE_SUPERVISOR_TREE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "supervisor" in mod.behaviours:
                init_fn = mod.find_function("init", 1)
                if init_fn:
                    body = init_fn.full_body
                    if "type => supervisor" in body or ", supervisor," in body or "{supervisor," in body:
                        evidences = [
                            Evidence(
                                description=f"Supervisor '{mod.name}' implements Composite Supervision Tree by orchestrating child sub-supervisors",
                                weight=0.85,
                                rule_code="COMPOSITE_SUPERVISOR_SUBTREE",
                                location=init_fn.location or mod.location,
                            )
                        ]
                        det = self._create_detection(
                            target_name=mod.name,
                            target_kind="composite_supervisor",
                            evidences=evidences,
                            location=mod.location,
                        )
                        detections.append(det)

        return detections
