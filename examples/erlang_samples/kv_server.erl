-module(kv_server).
-behaviour(gen_server).

-export([start_link/0, get/1, put/2, delete/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).

-record(state, {
    store = #{}
}).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

get(Key) ->
    gen_server:call(?MODULE, {get, Key}).

put(Key, Val) ->
    gen_server:call(?MODULE, {put, Key, Val}).

delete(Key) ->
    gen_server:cast(?MODULE, {delete, Key}).

init([]) ->
    {ok, #state{store = maps:new()}}.

handle_call({get, Key}, _From, State = #state{store = Store}) ->
    Reply = maps:get(Key, Store, undefined),
    {reply, Reply, State};

handle_call({put, Key, Val}, _From, State = #state{store = Store}) ->
    NewStore = maps:put(Key, Val, Store),
    {reply, ok, State#state{store = NewStore}}.

handle_cast({delete, Key}, State = #state{store = Store}) ->
    NewStore = maps:remove(Key, Store),
    {noreply, State#state{store = NewStore}}.

handle_info({'DOWN', _Ref, process, _Pid, _Reason}, State) ->
    {noreply, State};

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
