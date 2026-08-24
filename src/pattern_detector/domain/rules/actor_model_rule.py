"""Erlang Actor Model (Raw Process Loop) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ActorModelRule(BasePatternRule):
    """Detects raw actor process loops (receive ... -> loop(...) end)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ACTOR_MODEL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                # Loop function that has receive and calls itself recursively
                if (fn.name in ("loop", "server_loop", "worker_loop", "listen_loop") or fn.has_receive) and f"{fn.name}(" in fn.full_body:
                    if not mod.behaviours:  # Raw process actor, not standard gen_server
                        evidences = [
                            Evidence(
                                description=f"Function '{fn.id_str}' implements native Erlang Actor Model loop with tail-recursive message receive processing",
                                weight=0.75,
                                rule_code="ACTOR_PROCESS_LOOP",
                                location=fn.location,
                            )
                        ]
                        det = self._create_detection(
                            target_name=f"{mod.name}:{fn.id_str}",
                            target_kind="actor_loop_function",
                            evidences=evidences,
                            location=fn.location,
                        )
                        detections.append(det)

        return detections
