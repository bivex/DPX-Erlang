"""Erlang Memento State Store Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MementoEtsDetRule(BasePatternRule):
    """Detects Memento state snapshot persistence in terminate/2 or disk dumps."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEMENTO_ETS_DET

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            term_fn = mod.find_function("terminate", 2)
            if term_fn:
                body = term_fn.full_body
                if "dets:insert" in body or "mnesia:write" in body or "file:write_file" in body:
                    evidences = [
                        Evidence(
                            description=f"Function terminate/2 in '{mod.name}' captures and externalizes process Memento state to persistent storage on shutdown",
                            weight=0.80,
                            rule_code="MEMENTO_STATE_PERSISTENCE",
                            location=term_fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:terminate/2",
                        target_kind="memento_store_function",
                        evidences=evidences,
                        location=term_fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
