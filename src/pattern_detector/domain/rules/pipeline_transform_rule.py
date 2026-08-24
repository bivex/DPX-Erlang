"""Erlang Pipeline Transformation Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PipelineTransformRule(BasePatternRule):
    """Detects functional data pipelines using lists:foldl/map."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PIPELINE_TRANSFORM

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                body = fn.full_body
                if "lists:foldl(" in body and ("pipeline" in fn.name.lower() or "step" in body or "fun" in body):
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' implements functional data pipeline transformation using lists:foldl",
                            weight=0.75,
                            rule_code="PIPELINE_FUNCTIONAL_FOLD",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="pipeline_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
