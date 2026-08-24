-module(root_sup).
-behaviour(supervisor).

-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{
        strategy => one_for_all,
        intensity => 3,
        period => 5
    },
    ChildSpecs = [
        #{
            id => kv_server,
            start => {kv_server, start_link, []},
            restart => permanent,
            shutdown => 5000,
            type => worker,
            modules => [kv_server]
        },
        #{
            id => sub_worker_sup,
            start => {sub_sup, start_link, []},
            restart => permanent,
            shutdown => infinity,
            type => supervisor,
            modules => [sub_sup]
        }
    ],
    {ok, {SupFlags, ChildSpecs}}.
