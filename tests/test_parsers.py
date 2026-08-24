from pattern_detector.adapters.outbound.parsers.native_erlang_parser_adapter import NativeErlangParserAdapter

def test_parse_erlang_module():
    src = """
    -module(test_server).
    -behaviour(gen_server).
    -export([start_link/0, get/1]).
    -export([init/1, handle_call/3, handle_cast/2]).
    -record(state, {count = 0}).
    -callback custom_hook(Req :: term()) -> ok.

    start_link() ->
        gen_server:start_link(?MODULE, [], []).

    get(Key) ->
        gen_server:call(?MODULE, {get, Key}).

    init([]) ->
        {ok, #state{}}.

    handle_call({get, Key}, _From, State) ->
        {reply, Key, State}.

    handle_cast(stop, State) ->
        {stop, normal, State}.
    """
    parser = NativeErlangParserAdapter()
    mod = parser.parse_file("test_server.erl", src)

    assert mod.name == "test_server"
    assert "gen_server" in mod.behaviours
    assert ("start_link", 0) in mod.exports
    assert ("get", 1) in mod.exports
    assert "state" in mod.records
    assert "custom_hook/1" in mod.callbacks
    assert "start_link/0" in mod.functions
    assert "handle_call/3" in mod.functions
    assert "handle_cast/2" in mod.functions
