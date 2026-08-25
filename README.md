# 🔴 DPX-Erlang: Software Architecture & OTP Design Pattern Scanner

[![CI](https://github.com/bivex/DPX-Erlang/actions/workflows/ci.yml/badge.svg)](https://github.com/bivex/DPX-Erlang/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Erlang/OTP](https://img.shields.io/badge/Erlang%2FOTP-20--27%2B-crimson.svg)](https://www.erlang.org)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-blueviolet.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))

**DPX-Erlang** is an enterprise-grade, high-performance static analysis and software design pattern detection engine for **Erlang / OTP (OTP 20 - 27+)**.

Built with a clean **Hexagonal (Ports & Adapters) Domain-Driven Design (DDD)** architecture, DPX-Erlang uses a Bayesian evidence trail to accurately detect OTP behaviours, actor concurrency patterns, supervisor hierarchy trees, Let-It-Crash resilience violations, and code smells across Erlang applications and releases.

---

## 🚀 Key Features

* **30 Erlang & OTP Architecture Rules:**
  * **OTP Behaviours (6):** `gen_server`, `supervisor`, `gen_statem` / `gen_fsm`, `gen_event`, `application`, `special_process` (`proc_lib` / `sys`).
  * **Actor Concurrency (5):** Native Actor Model loop (`receive ... end`), Publish/Subscribe process groups (`pg` / `pg2`), Worker Pools (`poolboy`), Circuit Breakers (`fuse`), Process Lifecycle Observers (`monitor` / `link`).
  * **Structural Patterns (6):** Adapter, Decorator / Interceptor, Facade API modules, Process Proxies, ETS / `persistent_term` Flyweights, Composite Supervision Trees.
  * **Behavioral Patterns (6):** Tagged Tuple Command Dispatch, Dynamic Strategy Callback Dispatch (`Mod:Func(...)`), Template Method (`-callback`), Memento State Snapshots (`dets` / `mnesia`), Middleware Pipelines, Functional Data Transformations (`lists:foldl`).
  * **Resilience, SOLID & Safety (10):** Let-It-Crash Violations (`catch _:_ -> ignore`), Selective Receive Mailbox Leaks, Blocked Actor `handle_call` I/O, Supervisor Restart Storms, God Modules (SRP), Behaviour Callback Compliance, Circular Module Cycles, KISS, DRY, Dynamic Atom Exhaustion (`list_to_atom`).
* **High-Throughput Streaming AST Parser:**
  * Analyzes **~1,000 Erlang files per second** without relying on external compiler dependencies or Beam VM execution.
* **Interactive Semantic UI HTML Dashboard:**
  * Dark Semantic UI (Fomantic-UI) dashboard with instant filtering, zero-violation alerts, and **"Copy Architecture Map for LLM"** prompt generator for AI coding assistants.
* **OASIS SARIF v2.1.0 & CI/CD Support:**
  * Native output format for GitHub Code Scanning, GitLab SAST, SonarQube, JSON, and Markdown.

---

## 📦 Quickstart & Installation

```bash
# Clone the repository
git clone https://github.com/bivex/DPX-Erlang.git
cd DPX-Erlang

# Install with uv
uv sync
```

---

## 💻 CLI Usage

```bash
# Scan current Erlang project
uv run dpx scan .

# Scan specific Erlang app and generate all reports
uv run dpx scan /path/to/erlang_app \
    --html-output reports/dashboard.html \
    --sarif-output reports/security.sarif \
    --markdown-output reports/analysis.md \
    --json-output reports/data.json

# Filter by pattern
uv run dpx scan . -p gen_server -p supervisor

# Output LLM context map directly for AI agents
uv run dpx scan . --llm
```

---

## 📊 Real-World Benchmarks

| Project | Category | Files | Findings | Time | Speed | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **[ninenines/cowboy](https://github.com/ninenines/cowboy)** | HTTP / Websocket Server | **189** | **484** | 0.206s | 917 f/s | ✅ 0 crashes |
| **[erlang/rebar3](https://github.com/erlang/rebar3)** | Erlang Build Tool | **297** | **973** | 0.363s | 818 f/s | ✅ 0 crashes |
| **[mochi/mochiweb](https://github.com/mochi/mochiweb)** | Lightweight Web Server | **59** | **180** | 1.641s | - | ✅ 0 crashes |
| **[ninenines/ranch](https://github.com/ninenines/ranch)** | Socket Acceptor Pool | **47** | **135** | 0.038s | 1,236 f/s | ✅ 0 crashes |
| **[erlang-lager/lager](https://github.com/erlang-lager/lager)** | Logging Framework | **43** | **164** | 0.048s | 895 f/s | ✅ 0 crashes |
| **[eproxus/meck](https://github.com/eproxus/meck)** | Mocking Library | **24** | **138** | 0.022s | 1,090 f/s | ✅ 0 crashes |
| **[talentdeficit/jsx](https://github.com/talentdeficit/jsx)** | Streaming JSON Engine | **11** | **67** | 0.047s | 234 f/s | ✅ 0 crashes |
| **[devinus/poolboy](https://github.com/devinus/poolboy)** | Worker Pool Management | **7** | **25** | 0.006s | 1,166 f/s | ✅ 0 crashes |
| **TOTAL** | **8 Repositories** | **677 files** | **2,166 detections** | **2.370s** | **285 f/s** | 🚀 **100% stable** |

---

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
