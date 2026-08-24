"""Erlang Publish/Subscribe (pg / pg2) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PublishSubscribePgRule(BasePatternRule):
    """Detects Publish/Subscribe process group patterns via pg or pg2."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PUBLISH_SUBSCRIBE_PG

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "pg:join" in src or "pg:get_members" in src or "pg2:join" in src or "pg2:get_members" in src or "gproc:reg" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements Publish/Subscribe process groups broadcasting via pg / pg2 / gproc",
                        weight=0.80,
                        rule_code="PUBSUB_PROCESS_GROUPS",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="pubsub_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
