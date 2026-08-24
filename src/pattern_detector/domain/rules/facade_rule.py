"""Erlang Facade Module Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FacadeModuleRule(BasePatternRule):
    """Detects Facade modules in Erlang providing clean public API over internal gen_servers."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACADE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            # Module has no -behaviour, but has public exports that call gen_server:call or cast to internal servers
            if not mod.behaviours and len(mod.exports) >= 4:
                gen_calls = [
                    fn for fn in mod.functions.values()
                    if any(c[0] == "gen_server" and c[1] in ("call", "cast") for c in fn.calls)
                ]
                if len(gen_calls) >= 3:
                    evidences = [
                        Evidence(
                            description=f"Module '{mod.name}' serves as a Facade API wrapping {len(gen_calls)} internal gen_server calls behind unified functional interface",
                            weight=0.75,
                            rule_code="FACADE_GEN_SERVER_CLIENT_API",
                            location=mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=mod.name,
                        target_kind="facade_module",
                        evidences=evidences,
                        location=mod.location,
                    )
                    detections.append(det)

        return detections
