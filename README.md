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

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Huff`](https://github.com/bivex/DPX-Huff)** | **Huff / EVM Stack Assembly** (0.3.x+ / Cancun) | **Macros, Stack Layout, Jumpdest Labels, Selector Dispatchers, GoF 23** |
| **[`DPX-Yul`](https://github.com/bivex/DPX-Yul)** | **Yul / EVM Assembly** (0.8.x - 0.8.28+ / Cancun) | **Memory Management, Storage Packing, Transient Storage (EIP-1153), GoF 23** |
| **[`DPX-Cairo`](https://github.com/bivex/DPX-Cairo)** | **Cairo** (Cairo 1.0 - 2.8+ / Starknet) | **Components, Storage Mapping, Syscalls, Account Abstraction, Upgrades, GoF 23** |
| **[`DPX-Move`](https://github.com/bivex/DPX-Move)** | **Move** (Move 2024 / Aptos / Sui) | **Linear Resources, Abilities, Sui Objects, Hot Potato, Prover, GoF 23** |
| **[`DPX-Lua`](https://github.com/bivex/DPX-Lua)** | **Lua / Luau** (5.1 - 5.4 / LuaJIT) | **Metatable OOP, Coroutines, LuaJIT FFI, GameDev (Roblox/Neovim), GoF 23** |
| **[`DPX-Solidity`](https://github.com/bivex/DPX-Solidity)** | **Solidity** (0.8.x - 0.8.28+) | **EVM Gas Optimization, Proxies, CEI Reentrancy, Yul, GoF 23, Security** |
| **[`DPX-Zig`](https://github.com/bivex/DPX-Zig)** | **Zig** (0.11 - 0.14+) | **Comptime Generics, Allocator RAII, Defer Cleanup, SIMD, GoF 23** |
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

## 📄 License
MIT License. Created with ❤️ by the **Bivex Team**.


## 🌐 The DPX Multi-Language Static Analysis Family (27 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 2 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 3 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 4 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 5 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 6 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 7 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | **Fault Tolerance, Actor Model, OTP Behaviors** |
| 8 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 9 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 10 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 11 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 12 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 13 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 14 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 15 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 16 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 17 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 18 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 19 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 20 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 21 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 22 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 23 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 24 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 25 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 26 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 27 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |
