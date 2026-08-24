from pattern_detector.adapters.outbound.parsers.native_erlang_parser_adapter import NativeErlangParserAdapter
from pattern_detector.domain.rules.gen_server_rule import GenServerRule
from pattern_detector.domain.rules.supervisor_rule import SupervisorRule
from pattern_detector.domain.rules.let_it_crash_rule import LetItCrashRule
from pattern_detector.domain.rules.atom_exhaustion_rule import AtomExhaustionRule

def test_detect_gen_server_and_supervisor():
    parser = NativeErlangParserAdapter()
    src_server = """
    -module(my_srv).
    -behaviour(gen_server).
    -export([start_link/0, init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).
    start_link() -> gen_server:start_link(?MODULE, [], []).
    init([]) -> {ok, []}.
    handle_call(_Req, _From, State) -> {reply, ok, State}.
    handle_cast(_Msg, State) -> {noreply, State}.
    handle_info(_Info, State) -> {noreply, State}.
    terminate(_Reason, _State) -> ok.
    """
    src_sup = """
    -module(my_sup).
    -behaviour(supervisor).
    -export([start_link/0, init/1]).
    start_link() -> supervisor:start_link(?MODULE, []).
    init([]) ->
        {ok, {#{strategy => one_for_one, intensity => 3, period => 5}, []}}.
    """
    model = parser.parse_sources({"my_srv.erl": src_server, "my_sup.erl": src_sup})

    gs_rule = GenServerRule()
    gs_dets = gs_rule.detect(model)
    assert len(gs_dets) == 1
    assert gs_dets[0].target_name == "my_srv"

    sup_rule = SupervisorRule()
    sup_dets = sup_rule.detect(model)
    assert len(sup_dets) == 1
    assert sup_dets[0].target_name == "my_sup"

def test_detect_let_it_crash_and_atom_exhaustion():
    parser = NativeErlangParserAdapter()
    src = """
    -module(bad_mod).
    -export([unsafe_call/1]).
    unsafe_call(Str) ->
        try
            list_to_atom(Str)
        catch
            _:_ -> ok
        end.
    """
    model = parser.parse_sources({"bad_mod.erl": src})

    lic_rule = LetItCrashRule()
    lic_dets = lic_rule.detect(model)
    assert len(lic_dets) == 1

    atom_rule = AtomExhaustionRule()
    atom_dets = atom_rule.detect(model)
    assert len(atom_dets) == 1
