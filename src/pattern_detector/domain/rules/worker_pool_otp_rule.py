"""Erlang Worker Pool (Poolboy / Pool) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class WorkerPoolOtpRule(BasePatternRule):
    """Detects Worker Pool patterns via Poolboy or custom worker pools in Erlang."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.WORKER_POOL_OTP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "poolboy:transaction" in src or "poolboy:checkout" in src or "worker_pool:call" in src or ("pool" in mod.name.lower() and "worker" in src):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' manages bounded worker process concurrency pool (poolboy / worker pool)",
                        weight=0.80,
                        rule_code="WORKER_POOL_OTP_MANAGEMENT",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="worker_pool_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
