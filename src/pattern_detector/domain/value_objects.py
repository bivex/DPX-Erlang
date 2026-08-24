"""Domain value objects for the Erlang/OTP Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad classification of Erlang design patterns, OTP behaviours, and safety rules."""

    OTP_BEHAVIOUR = "otp_behaviour"
    ACTOR_CONCURRENCY = "actor_concurrency"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"
    SAFETY = "safety"


class PatternType(str, Enum):
    """Specific Erlang/OTP design pattern, behaviour, and architecture smell identifiers."""

    # OTP Behaviours
    GEN_SERVER = "gen_server"
    SUPERVISOR = "supervisor"
    GEN_STATEM = "gen_statem"
    GEN_EVENT = "gen_event"
    APPLICATION = "application"
    SPECIAL_PROCESS = "special_process"

    # Actor & Concurrency
    ACTOR_MODEL = "actor_model"
    PUBLISH_SUBSCRIBE_PG = "publish_subscribe_pg"
    WORKER_POOL_OTP = "worker_pool_otp"
    CIRCUIT_BREAKER = "circuit_breaker"
    MONITOR_LINK_OBSERVER = "monitor_link_observer"

    # Structural
    ADAPTER = "adapter"
    DECORATOR_WRAPPER = "decorator_wrapper"
    FACADE = "facade"
    PROXY_ROUTER = "proxy_router"
    FLYWEIGHT_ETS = "flyweight_ets"
    COMPOSITE_SUPERVISOR_TREE = "composite_supervisor_tree"

    # Behavioral
    COMMAND_MESSAGE = "command_message"
    STRATEGY_CALLBACK = "strategy_callback"
    TEMPLATE_METHOD_BEHAVIOUR = "template_method_behaviour"
    MEMENTO_ETS_DET = "memento_ets_det"
    CHAIN_OF_RESPONSIBILITY = "chain_of_responsibility"
    PIPELINE_TRANSFORM = "pipeline_transform"

    # Resilience, SOLID & Safety Audits
    LET_IT_CRASH_DEFENSIVE_SMELL = "let_it_crash_defensive_smell"
    SELECTIVE_RECEIVE_LEAK = "selective_receive_leak"
    BLOCKED_GEN_SERVER_CALL = "blocked_gen_server_call"
    SUPERVISOR_RESTART_STORM = "supervisor_restart_storm"
    SINGLE_RESPONSIBILITY_MODULE = "single_responsibility_module"
    BEHAVIOUR_CALLBACK_COMPLIANCE = "behaviour_callback_compliance"
    CIRCULAR_MODULE_DEPENDENCY = "circular_module_dependency"
    KISS = "kiss"
    DRY = "dry"
    ATOM_EXHAUSTION_RISK = "atom_exhaustion_risk"


class ConfidenceLevel(str, Enum):
    """Categorical confidence rating for a pattern detection."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @classmethod
    def from_score(cls, score: float) -> ConfidenceLevel:
        if score >= 0.85:
            return cls.VERY_HIGH
        if score >= 0.70:
            return cls.HIGH
        if score >= 0.50:
            return cls.MEDIUM
        return cls.LOW


@dataclass(frozen=True)
class SourceLocation:
    """Represents a precise location in an Erlang source code file (.erl / .hrl)."""

    file_path: str
    line: int = 1
    column: int = 1
    end_line: int | None = None
    end_column: int | None = None

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Evidence:
    """A single piece of heuristic evidence supporting a pattern detection."""

    description: str
    weight: float
    rule_code: str
    location: SourceLocation | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Evidence weight must be between 0.0 and 1.0, got {self.weight}")


@dataclass(frozen=True)
class Confidence:
    """Aggregated confidence score computed from multiple pieces of evidence."""

    score: float
    level: ConfidenceLevel = field(init=False)

    def __post_init__(self) -> None:
        clamped = max(0.0, min(1.0, self.score))
        object.__setattr__(self, "score", clamped)
        object.__setattr__(self, "level", ConfidenceLevel.from_score(clamped))

    @classmethod
    def from_evidences(cls, evidences: list[Evidence]) -> Confidence:
        if not evidences:
            return cls(0.0)
        complement_product = 1.0
        for ev in evidences:
            complement_product *= (1.0 - ev.weight)
        return cls(1.0 - complement_product)

    @property
    def percentage_str(self) -> str:
        return f"{int(self.score * 100)}%"
