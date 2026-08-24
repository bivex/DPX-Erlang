-module(door_statem).
-behaviour(gen_statem).

-export([start_link/0, open/0, close/0, lock/1, unlock/1]).
-export([init/1, callback_mode/0, terminate/3, code_change/4]).
-export([locked/3, open/3, closed/3]).

start_link() ->
    gen_statem:start_link({local, ?MODULE}, ?MODULE, [], []).

callback_mode() ->
    state_functions.

open() ->
    gen_statem:call(?MODULE, open_door).

close() ->
    gen_statem:call(?MODULE, close_door).

lock(Code) ->
    gen_statem:call(?MODULE, {lock_door, Code}).

unlock(Code) ->
    gen_statem:call(?MODULE, {unlock_door, Code}).

init([]) ->
    {ok, locked, #{code => 1234}}.

locked({call, From}, {unlock_door, Code}, Data = #{code := Code}) ->
    {next_state, closed, Data, [{reply, From, ok}]};
locked({call, From}, _Msg, Data) ->
    {keep_state, Data, [{reply, From, {error, wrong_code}}]}.

closed({call, From}, open_door, Data) ->
    {next_state, open, Data, [{reply, From, ok}]};
closed({call, From}, {lock_door, Code}, Data) ->
    {next_state, locked, Data#{code => Code}, [{reply, From, ok}]}.

open({call, From}, close_door, Data) ->
    {next_state, closed, Data, [{reply, From, ok}]}.

terminate(_Reason, _State, _Data) ->
    ok.

code_change(_OldVsn, State, Data, _Extra) ->
    {ok, State, Data}.
