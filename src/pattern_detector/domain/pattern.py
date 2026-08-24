"""Pattern metadata, catalog definitions, and architectural descriptions for Erlang / OTP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternCatalogEntry:
    """Catalog entry describing an Erlang / OTP pattern or rule."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: Mapping[PatternType, PatternCatalogEntry] = {
    # OTP Behaviours
    PatternType.GEN_SERVER: PatternCatalogEntry(
        pattern_type=PatternType.GEN_SERVER,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Generic Server (gen_server)",
        description="Standard OTP client-server actor abstraction encapsulating state and synchronizing synchronous calls and asynchronous casts.",
        idiomatic_example="-behaviour(gen_server).\ninit(Args) -> {ok, #state{}}.\nhandle_call(Req, From, State) -> {reply, ok, State}.",
    ),
    PatternType.SUPERVISOR: PatternCatalogEntry(
        pattern_type=PatternType.SUPERVISOR,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Supervisor (supervisor)",
        description="OTP process tree supervisor responsible for monitoring, isolating failures, and restarting worker processes.",
        idiomatic_example="-behaviour(supervisor).\ninit([]) -> {ok, {#{strategy => one_for_all, intensity => 3, period => 5}, [ChildSpec]}}.",
    ),
    PatternType.GEN_STATEM: PatternCatalogEntry(
        pattern_type=PatternType.GEN_STATEM,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="State Machine (gen_statem / gen_fsm)",
        description="OTP finite state machine behavior with callback modes (state_functions or handle_event_function).",
        idiomatic_example="-behaviour(gen_statem).\ncallback_mode() -> state_functions.",
    ),
    PatternType.GEN_EVENT: PatternCatalogEntry(
        pattern_type=PatternType.GEN_EVENT,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Event Manager (gen_event)",
        description="OTP event manager allowing dynamic addition and removal of pluggable event handlers.",
        idiomatic_example="-behaviour(gen_event).\nhandle_event(Event, State) -> {ok, State}.",
    ),
    PatternType.APPLICATION: PatternCatalogEntry(
        pattern_type=PatternType.APPLICATION,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="OTP Application (application)",
        description="Top-level OTP component packaging supervisors, workers, and resources into a deployable release unit.",
        idiomatic_example="-behaviour(application).\nstart(_StartType, _StartArgs) -> my_top_sup:start_link().",
    ),
    PatternType.SPECIAL_PROCESS: PatternCatalogEntry(
        pattern_type=PatternType.SPECIAL_PROCESS,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Special Process (proc_lib / sys)",
        description="Non-standard process complying with OTP system messages (sys:init_ack, system_continue, system_terminate).",
        idiomatic_example="proc_lib:spawn_link(?MODULE, init, [Parent]).",
    ),

    # Actor & Concurrency
    PatternType.ACTOR_MODEL: PatternCatalogEntry(
        pattern_type=PatternType.ACTOR_MODEL,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Actor Model (Raw Process Loop)",
        description="Lightweight Erlang process running a tail-recursive loop with selective receive message processing.",
        idiomatic_example="loop(State) -> receive {msg, Msg} -> loop(update(State, Msg)) end.",
    ),
    PatternType.PUBLISH_SUBSCRIBE_PG: PatternCatalogEntry(
        pattern_type=PatternType.PUBLISH_SUBSCRIBE_PG,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Publish/Subscribe (pg / pg2)",
        description="Decentralized or process-group pub/sub broadcasting messages to clusters of subscriber processes.",
        idiomatic_example="pg:join(Scope, Group, self()), [Pid ! Msg || Pid <- pg:get_members(Scope, Group)].",
    ),
    PatternType.WORKER_POOL_OTP: PatternCatalogEntry(
        pattern_type=PatternType.WORKER_POOL_OTP,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Worker Pool (Poolboy / Pool)",
        description="Manages a bounded pool of pre-forked worker processes to limit resource usage and queue high loads.",
        idiomatic_example="poolboy:transaction(PoolName, fun(Worker) -> gen_server:call(Worker, Task) end).",
    ),
    PatternType.CIRCUIT_BREAKER: PatternCatalogEntry(
        pattern_type=PatternType.CIRCUIT_BREAKER,
        category=PatternCategory.RESILIENCE,
        name="Circuit Breaker Pattern",
        description="Monitors error rates and trips open to prevent cascading failures to struggling dependencies.",
        idiomatic_example="fuse:run(my_fuse, fun() -> call_remote_api() end).",
    ),
    PatternType.MONITOR_LINK_OBSERVER: PatternCatalogEntry(
        pattern_type=PatternType.MONITOR_LINK_OBSERVER,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Monitor / Link Observer",
        description="Observes process life cycles via erlang:monitor/2 or link/1, handling {'DOWN', ...} or {'EXIT', ...} signals.",
        idiomatic_example="erlang:monitor(process, Pid), receive {'DOWN', Ref, process, Pid, Reason} -> ... end.",
    ),

    # Structural
    PatternType.ADAPTER: PatternCatalogEntry(
        pattern_type=PatternType.ADAPTER,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Pattern",
        description="Adapts a non-OTP module or third-party C/NIF library interface to standard OTP conventions.",
        idiomatic_example="init(Args) -> {ok, legacy_driver:open(Args)}.",
    ),
    PatternType.DECORATOR_WRAPPER: PatternCatalogEntry(
        pattern_type=PatternType.DECORATOR_WRAPPER,
        category=PatternCategory.STRUCTURAL,
        name="Decorator / Callback Interceptor",
        description="Wraps gen_server/cowboy handlers to transparently inject logging, telemetry, or authorization.",
        idiomatic_example="execute(Req, Env) -> telemetry:span(...), NextModule:execute(Req, Env).",
    ),
    PatternType.FACADE: PatternCatalogEntry(
        pattern_type=PatternType.FACADE,
        category=PatternCategory.STRUCTURAL,
        name="Facade Module",
        description="Exposes a unified, high-level client API hiding internal gen_servers and process communication.",
        idiomatic_example="get_user(Id) -> gen_server:call(?SERVER, {get_user, Id}).",
    ),
    PatternType.PROXY_ROUTER: PatternCatalogEntry(
        pattern_type=PatternType.PROXY_ROUTER,
        category=PatternCategory.STRUCTURAL,
        name="Process Proxy / Router",
        description="Intermediate process routing and dispatching requests to target worker processes.",
        idiomatic_example="handle_call({route, Msg}, _From, State) -> Target ! Msg, {reply, ok, State}.",
    ),
    PatternType.FLYWEIGHT_ETS: PatternCatalogEntry(
        pattern_type=PatternType.FLYWEIGHT_ETS,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight / ETS Shared Cache",
        description="Shared memory concurrent reads via ETS (Erlang Term Storage) or persistent_term to avoid heap copying.",
        idiomatic_example="ets:new(cache, [set, public, read_concurrency, {keypos, 1}]).",
    ),
    PatternType.COMPOSITE_SUPERVISOR_TREE: PatternCatalogEntry(
        pattern_type=PatternType.COMPOSITE_SUPERVISOR_TREE,
        category=PatternCategory.STRUCTURAL,
        name="Composite Supervision Tree",
        description="Hierarchical composite tree structure where supervisors oversee sub-supervisors and leaf workers.",
        idiomatic_example="#{id => sub_sup, start => {sub_sup, start_link, []}, type => supervisor}.",
    ),

    # Behavioral
    PatternType.COMMAND_MESSAGE: PatternCatalogEntry(
        pattern_type=PatternType.COMMAND_MESSAGE,
        category=PatternCategory.BEHAVIORAL,
        name="Command Tagged Tuple",
        description="Encapsulates operations as tagged tuples ({Action, Arg1, Arg2}) dispatched in pattern matches.",
        idiomatic_example="handle_call({create_order, Items, CustomerId}, From, State) -> ...",
    ),
    PatternType.STRATEGY_CALLBACK: PatternCatalogEntry(
        pattern_type=PatternType.STRATEGY_CALLBACK,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Callback Dispatch",
        description="Dynamically selects and executes algorithm modules via Module:Function(Args) dispatch.",
        idiomatic_example="format_payload(FormatterMod, Data) -> FormatterMod:format(Data).",
    ),
    PatternType.TEMPLATE_METHOD_BEHAVIOUR: PatternCatalogEntry(
        pattern_type=PatternType.TEMPLATE_METHOD_BEHAVIOUR,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method (-callback)",
        description="Defines algorithm skeleton in library module, requiring client modules to implement -callback contracts.",
        idiomatic_example="-callback handle_request(Req :: term()) -> {ok, term()} | {error, term()}.",
    ),
    PatternType.MEMENTO_ETS_DET: PatternCatalogEntry(
        pattern_type=PatternType.MEMENTO_ETS_DET,
        category=PatternCategory.BEHAVIORAL,
        name="Memento State Store",
        description="Persists process state snapshots to ETS, DETS, or disk on shutdown for crash recovery.",
        idiomatic_example="terminate(_Reason, State) -> dets:insert(save_table, {saved_state, State}).",
    ),
    PatternType.CHAIN_OF_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY,
        category=PatternCategory.BEHAVIORAL,
        name="Middleware / Filter Chain",
        description="Sequentially passes requests through a chain of handler modules (e.g. Cowboy middleware).",
        idiomatic_example="execute(Req, [Mod | Rest]) -> case Mod:execute(Req) of {ok, Req2} -> execute(Req2, Rest) end.",
    ),
    PatternType.PIPELINE_TRANSFORM: PatternCatalogEntry(
        pattern_type=PatternType.PIPELINE_TRANSFORM,
        category=PatternCategory.BEHAVIORAL,
        name="Pipeline Transformation",
        description="Functional data transformations chaining lists:map, lists:filter, and lists:foldl.",
        idiomatic_example="lists:foldl(fun step/2, Initial, PipelineSteps).",
    ),

    # Resilience & Safety Audits
    PatternType.LET_IT_CRASH_DEFENSIVE_SMELL: PatternCatalogEntry(
        pattern_type=PatternType.LET_IT_CRASH_DEFENSIVE_SMELL,
        category=PatternCategory.SAFETY,
        name="Defensive Catch-All (Let It Crash Violation)",
        description="Catches _:_ or throws defensively instead of allowing the process to fail cleanly and restart via supervisor.",
        idiomatic_example="Avoid catch-all try ... catch _:_ -> ignore end that hides corrupted state.",
    ),
    PatternType.SELECTIVE_RECEIVE_LEAK: PatternCatalogEntry(
        pattern_type=PatternType.SELECTIVE_RECEIVE_LEAK,
        category=PatternCategory.SAFETY,
        name="Selective Receive Mailbox Leak",
        description="Receive loop matching only specific tags without timeout or catch-all, causing mailbox queue explosion.",
        idiomatic_example="Always include a timeout or catch-all unexpected message handler.",
    ),
    PatternType.BLOCKED_GEN_SERVER_CALL: PatternCatalogEntry(
        pattern_type=PatternType.BLOCKED_GEN_SERVER_CALL,
        category=PatternCategory.SAFETY,
        name="Blocked gen_server handle_call",
        description="Performing long synchronous I/O or nested gen_server:call in handle_call risking mailbox deadlocks.",
        idiomatic_example="Delegate heavy work to spawned worker processes or use gen_server:reply/2.",
    ),
    PatternType.SUPERVISOR_RESTART_STORM: PatternCatalogEntry(
        pattern_type=PatternType.SUPERVISOR_RESTART_STORM,
        category=PatternCategory.RESILIENCE,
        name="Supervisor Restart Storm Risk",
        description="Supervisor configured with high intensity (>10) and low period (<1s) risking cascading node termination.",
        idiomatic_example="Use reasonable restart thresholds (e.g., #{intensity => 3, period => 5}).",
    ),
    PatternType.SINGLE_RESPONSIBILITY_MODULE: PatternCatalogEntry(
        pattern_type=PatternType.SINGLE_RESPONSIBILITY_MODULE,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (God Module)",
        description="God Module with excessive exports (≥25 functions) mixing unrelated domains.",
        idiomatic_example="Decompose large modules into cohesive sub-modules.",
    ),
    PatternType.BEHAVIOUR_CALLBACK_COMPLIANCE: PatternCatalogEntry(
        pattern_type=PatternType.BEHAVIOUR_CALLBACK_COMPLIANCE,
        category=PatternCategory.PRINCIPLE,
        name="Behaviour Callback Compliance",
        description="Ensures modules implementing -behaviour(gen_server) implement all required callback functions.",
        idiomatic_example="Implement init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3.",
    ),
    PatternType.CIRCULAR_MODULE_DEPENDENCY: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_MODULE_DEPENDENCY,
        category=PatternCategory.PRINCIPLE,
        name="Circular Module Dependency",
        description="Detects cyclic cross-module function calls (ModuleA -> ModuleB -> ModuleA).",
        idiomatic_example="Refactor shared functions into a standalone utility module.",
    ),
    PatternType.KISS: PatternCatalogEntry(
        pattern_type=PatternType.KISS,
        category=PatternCategory.PRINCIPLE,
        name="Keep It Simple (KISS)",
        description="Functions with excessive pattern matching clauses (≥10) or deep case nesting.",
        idiomatic_example="Decompose complex multi-clause functions.",
    ),
    PatternType.DRY: PatternCatalogEntry(
        pattern_type=PatternType.DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Duplicate function clause implementations across modules.",
        idiomatic_example="Extract common clauses into reusable helper functions.",
    ),
    PatternType.ATOM_EXHAUSTION_RISK: PatternCatalogEntry(
        pattern_type=PatternType.ATOM_EXHAUSTION_RISK,
        category=PatternCategory.SAFETY,
        name="Atom Exhaustion Risk",
        description="Using list_to_atom or binary_to_atom on dynamic input, which can exhaust the Erlang VM atom table (1M limit).",
        idiomatic_example="Use list_to_existing_atom or binary_to_existing_atom instead.",
    ),
}
