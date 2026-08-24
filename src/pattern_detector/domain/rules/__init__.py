"""Rule catalog registration for Erlang / OTP pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.actor_model_rule import ActorModelRule
from pattern_detector.domain.rules.adapter_rule import AdapterPatternRule
from pattern_detector.domain.rules.application_rule import ApplicationRule
from pattern_detector.domain.rules.atom_exhaustion_rule import AtomExhaustionRule
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.behaviour_callback_compliance_rule import BehaviourCallbackComplianceRule
from pattern_detector.domain.rules.blocked_gen_server_call_rule import BlockedGenServerCallRule
from pattern_detector.domain.rules.chain_of_responsibility_rule import ChainOfResponsibilityRule
from pattern_detector.domain.rules.circular_dependency_rule import CircularDependencyRule
from pattern_detector.domain.rules.circuit_breaker_rule import CircuitBreakerRule
from pattern_detector.domain.rules.command_message_rule import CommandMessageRule
from pattern_detector.domain.rules.composite_supervisor_tree_rule import CompositeSupervisorTreeRule
from pattern_detector.domain.rules.decorator_wrapper_rule import DecoratorWrapperRule
from pattern_detector.domain.rules.dry_rule import DryRule
from pattern_detector.domain.rules.facade_rule import FacadeModuleRule
from pattern_detector.domain.rules.flyweight_ets_rule import FlyweightEtsRule
from pattern_detector.domain.rules.gen_event_rule import GenEventRule
from pattern_detector.domain.rules.gen_server_rule import GenServerRule
from pattern_detector.domain.rules.gen_statem_rule import GenStatemRule
from pattern_detector.domain.rules.kiss_rule import KissRule
from pattern_detector.domain.rules.let_it_crash_rule import LetItCrashRule
from pattern_detector.domain.rules.memento_ets_det_rule import MementoEtsDetRule
from pattern_detector.domain.rules.monitor_link_observer_rule import MonitorLinkObserverRule
from pattern_detector.domain.rules.pipeline_transform_rule import PipelineTransformRule
from pattern_detector.domain.rules.proxy_router_rule import ProxyRouterRule
from pattern_detector.domain.rules.publish_subscribe_pg_rule import PublishSubscribePgRule
from pattern_detector.domain.rules.selective_receive_leak_rule import SelectiveReceiveLeakRule
from pattern_detector.domain.rules.special_process_rule import SpecialProcessRule
from pattern_detector.domain.rules.srp_module_rule import SingleResponsibilityModuleRule
from pattern_detector.domain.rules.strategy_callback_rule import StrategyCallbackRule
from pattern_detector.domain.rules.supervisor_restart_storm_rule import SupervisorRestartStormRule
from pattern_detector.domain.rules.supervisor_rule import SupervisorRule
from pattern_detector.domain.rules.template_method_behaviour_rule import TemplateMethodBehaviourRule
from pattern_detector.domain.rules.worker_pool_otp_rule import WorkerPoolOtpRule

DEFAULT_RULES: list[PatternRule] = [
    # OTP Behaviours (6)
    GenServerRule(),
    SupervisorRule(),
    GenStatemRule(),
    GenEventRule(),
    ApplicationRule(),
    SpecialProcessRule(),

    # Actor Concurrency (5)
    ActorModelRule(),
    PublishSubscribePgRule(),
    WorkerPoolOtpRule(),
    CircuitBreakerRule(),
    MonitorLinkObserverRule(),

    # Structural (6)
    AdapterPatternRule(),
    DecoratorWrapperRule(),
    FacadeModuleRule(),
    ProxyRouterRule(),
    FlyweightEtsRule(),
    CompositeSupervisorTreeRule(),

    # Behavioral (6)
    CommandMessageRule(),
    StrategyCallbackRule(),
    TemplateMethodBehaviourRule(),
    MementoEtsDetRule(),
    ChainOfResponsibilityRule(),
    PipelineTransformRule(),

    # Resilience & Safety Audits (10)
    LetItCrashRule(),
    SelectiveReceiveLeakRule(),
    BlockedGenServerCallRule(),
    SupervisorRestartStormRule(),
    SingleResponsibilityModuleRule(),
    BehaviourCallbackComplianceRule(),
    CircularDependencyRule(),
    KissRule(),
    DryRule(),
    AtomExhaustionRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    "GenServerRule",
    "SupervisorRule",
    "GenStatemRule",
    "GenEventRule",
    "ApplicationRule",
    "SpecialProcessRule",
    "ActorModelRule",
    "PublishSubscribePgRule",
    "WorkerPoolOtpRule",
    "CircuitBreakerRule",
    "MonitorLinkObserverRule",
    "AdapterPatternRule",
    "DecoratorWrapperRule",
    "FacadeModuleRule",
    "ProxyRouterRule",
    "FlyweightEtsRule",
    "CompositeSupervisorTreeRule",
    "CommandMessageRule",
    "StrategyCallbackRule",
    "TemplateMethodBehaviourRule",
    "MementoEtsDetRule",
    "ChainOfResponsibilityRule",
    "PipelineTransformRule",
    "LetItCrashRule",
    "SelectiveReceiveLeakRule",
    "BlockedGenServerCallRule",
    "SupervisorRestartStormRule",
    "SingleResponsibilityModuleRule",
    "BehaviourCallbackComplianceRule",
    "CircularDependencyRule",
    "KissRule",
    "DryRule",
    "AtomExhaustionRule",
]
