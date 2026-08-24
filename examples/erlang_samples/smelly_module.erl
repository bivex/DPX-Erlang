-module(smelly_module).
-export([f1/0, f2/0, f3/0, f4/0, f5/0, f6/0, f7/0, f8/0, f9/0, f10/0,
         f11/0, f12/0, f13/0, f14/0, f15/0, f16/0, f17/0, f18/0, f19/0, f20/0,
         f21/0, f22/0, f23/0, f24/0, f25/0, f26/0]).

f1() -> ok.
f2() -> ok.
f3() -> ok.
f4() -> ok.
f5() -> ok.
f6() -> ok.
f7() -> ok.
f8() -> ok.
f9() -> ok.
f10() -> ok.
f11() -> ok.
f12() -> ok.
f13() -> ok.
f14() -> ok.
f15() -> ok.
f16() -> ok.
f17() -> ok.
f18() -> ok.
f19() -> ok.
f20() -> ok.
f21() -> ok.
f22() -> ok.
f23() -> ok.
f24() -> ok.
f25() -> ok.
f26() -> ok.

defensive_function(DynamicString) ->
    try
        list_to_atom(DynamicString)
    catch
        _:_ -> ok
    end.
