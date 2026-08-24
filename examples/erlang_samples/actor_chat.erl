-module(actor_chat).
-export([start/0, loop/1]).

start() ->
    spawn(fun() -> loop([]) end).

loop(Users) ->
    receive
        {join, UserPid} ->
            loop([UserPid | Users]);
        {msg, From, Text} ->
            [U ! {incoming, From, Text} || U <- Users],
            loop(Users);
        stop ->
            ok
    end.
