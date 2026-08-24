"""Erlang Strategy Callback Dispatch Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StrategyCallbackRule(BasePatternRule):
    """Detects dynamic module Strategy dispatch (Module:Function(Args))."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRATEGY_CALLBACK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                # Look for dynamic module call: Variable:Function(
                dyn_calls = re.findall(r"\b([A-Z][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z0-9_]+)\s*\(", fn.full_body)
                if dyn_calls:
                    var_name, func_name = dyn_calls[0]
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' implements dynamic Strategy dispatch calling {var_name}:{func_name}(...)",
                            weight=0.80,
                            rule_code="STRATEGY_DYNAMIC_MODULE_DISPATCH",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="strategy_dispatch_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
