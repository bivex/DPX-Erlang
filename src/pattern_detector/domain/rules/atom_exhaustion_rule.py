"""Erlang Atom Table Exhaustion Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AtomExhaustionRule(BasePatternRule):
    """Detects unsafe dynamic atom creation (list_to_atom / binary_to_atom)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ATOM_EXHAUSTION_RISK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                body = fn.full_body
                if "list_to_atom(" in body or "binary_to_atom(" in body:
                    evidences = [
                        Evidence(
                            description=f"Safety Audit (Atom Exhaustion Risk): Function '{fn.id_str}' in '{mod.name}' calls list_to_atom / binary_to_atom on dynamic input; use list_to_existing_atom to prevent VM crash",
                            weight=0.80,
                            rule_code="UNSAFE_DYNAMIC_ATOM_CREATION",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}:{fn.id_str}",
                        target_kind="unsafe_atom_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
