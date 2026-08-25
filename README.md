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
 **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
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
