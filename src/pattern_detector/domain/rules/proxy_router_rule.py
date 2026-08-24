"""Erlang Proxy / Router Process Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ProxyRouterRule(BasePatternRule):
    """Detects Process Proxy / Router patterns in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROXY_ROUTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "router" in mod.name.lower() or "proxy" in mod.name.lower() or "dispatcher" in mod.name.lower():
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements Process Proxy / Message Router routing requests between client and worker pids",
                        weight=0.75,
                        rule_code="PROXY_ROUTER_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="proxy_router_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
