"""Erlang Defensive Catch-All (Let It Crash Violation) Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LetItCrashRule(BasePatternRule):
    """Detects excessive defensive catch-all blocks violating Erlang's 'Let It Crash' philosophy."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LET_IT_CRASH_DEFENSIVE_SMELL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                # Matches catch _:_ or catch _:Reason -> ignore/ok
                if re.search(r"catch\s+(_:[a-zA-Z0-9_]+|_:_)\s*->\s*(?:ok|ignore|undefined|\{\})", fn.full_body):
                    evidences = [
                        Evidence(
                            description=f"Let It Crash Violation: Function '{fn.id_str}' catches all errors defensively (catch _:_ -> ignore); let processes fail fast and restart via supervisor",
                            weight=0.85,
                            rule_code="DEFENSIVE_CATCH_ALL_SMELL",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="defensive_catch_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
