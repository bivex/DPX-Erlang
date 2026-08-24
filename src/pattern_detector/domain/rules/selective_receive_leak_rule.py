"""Erlang Selective Receive Mailbox Leak Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SelectiveReceiveLeakRule(BasePatternRule):
    """Detects process receive loops without catch-all or timeout (mailbox leak risk)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SELECTIVE_RECEIVE_LEAK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                if fn.has_receive:
                    body = fn.full_body
                    # Check if receive has 'after' or catch-all '_'
                    has_after = "after" in body
                    has_catch_all = bool(re.search(r"(?:^|\n|\s)(?:_[a-zA-Z0-9_]*|[A-Z][a-zA-Z0-9_]*)\s*->", body))
                    if not has_after and not has_catch_all and "loop(" in body:
                        evidences = [
                            Evidence(
                                description=f"Safety Audit (Mailbox Leak Risk): Function '{fn.id_str}' uses selective receive without an 'after' timeout or catch-all clause, risking unbounded mailbox growth",
                                weight=0.80,
                                rule_code="SELECTIVE_RECEIVE_UNBOUNDED_MAILBOX",
                                location=fn.location or mod.location,
                            )
                        ]
                        det = self._create_detection(
                            target_name=f"{mod.name}:{fn.id_str}",
                            target_kind="receive_loop_function",
                            evidences=evidences,
                            location=fn.location or mod.location,
                        )
                        detections.append(det)

        return detections
