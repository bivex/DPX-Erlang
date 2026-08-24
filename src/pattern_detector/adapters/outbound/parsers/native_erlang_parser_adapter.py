"""High-performance Native Erlang AST & CST Parser Adapter implementing ParserPort."""

from __future__ import annotations

import os
import re
from pathlib import Path

from pattern_detector.domain.code_model import (
    CallbackModel,
    CodeModel,
    FunctionClauseModel,
    FunctionModel,
    ModuleModel,
    RecordFieldModel,
    RecordModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class NativeErlangParserAdapter(ParserPort):
    """High-performance, fault-tolerant native Erlang/OTP parser supporting OTP 20 - 27+ syntax."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            mod_model = self.parse_file(file_path, source_text)
            if mod_model:
                model.modules[mod_model.name] = mod_model
        return model

    def parse_file(self, file_path: str, source_text: str) -> ModuleModel:
        loc = SourceLocation(file_path=file_path, line=1, column=1)
        mod_name = self._parse_module_name(source_text, file_path)

        mod_model = ModuleModel(
            name=mod_name,
            file_path=file_path,
            raw_source=source_text,
            location=loc,
        )

        clean_text = self._strip_comments(source_text)

        # 1. Behaviours: -behaviour(...) or -behavior(...)
        mod_model.behaviours = self._parse_behaviours(clean_text)

        # 2. Exports: -export([...]).
        mod_model.exports = self._parse_exports(clean_text)

        # 3. Records: -record(name, {...}).
        mod_model.records = self._parse_records(clean_text, file_path)

        # 4. Callbacks: -callback name(...) -> ...
        mod_model.callbacks = self._parse_callbacks(clean_text, file_path)

        # 5. Functions
        mod_model.functions = self._parse_functions(clean_text, file_path, mod_model.exports)

        return mod_model

    # -------------------------------------------------------------------------
    # Parsing Helpers
    # -------------------------------------------------------------------------

    def _parse_module_name(self, text: str, file_path: str) -> str:
        m = re.search(r"-module\s*\(\s*([a-zA-Z0-9_]+)\s*\)\.", text)
        if m:
            return m.group(1)
        return Path(file_path).stem

    def _strip_comments(self, text: str) -> str:
        # Strip % comments, but preserve newlines for accurate line numbers
        lines = []
        for line in text.splitlines():
            # Strip anything after unquoted %
            clean_line = re.sub(r"%(?=(?:[^\"\']*[\"\'][^\"\']*[\"\'])*[^\"\']*$).*", "", line)
            lines.append(clean_line)
        return "\n".join(lines)

    def _parse_behaviours(self, text: str) -> list[str]:
        behaviours = []
        matches = re.finditer(r"-(?:behaviour|behavior)\s*\(\s*([a-zA-Z0-9_]+)\s*\)\.", text)
        for m in matches:
            behaviours.append(m.group(1))
        return behaviours

    def _parse_exports(self, text: str) -> list[tuple[str, int]]:
        exports = []
        matches = re.finditer(r"-export\s*\(\s*\[\s*([^\]]*)\s*\]\s*\)\.", text)
        for m in matches:
            items_str = m.group(1)
            for item in items_str.split(","):
                item = item.strip()
                if "/" in item:
                    parts = item.split("/")
                    name = parts[0].strip()
                    try:
                        arity = int(parts[1].strip())
                        exports.append((name, arity))
                    except ValueError:
                        pass
        return exports

    def _parse_records(self, text: str, file_path: str) -> dict[str, RecordModel]:
        records = {}
        pattern = re.compile(r"-record\s*\(\s*([a-zA-Z0-9_]+)\s*,\s*\{([^}]*)\}\s*\)\.", re.MULTILINE)
        for m in pattern.finditer(text):
            rec_name = m.group(1)
            fields_raw = m.group(2)
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            fields = []
            for f in fields_raw.split(","):
                f = f.strip()
                if not f:
                    continue
                f_parts = f.split("=")
                f_name = f_parts[0].strip()
                f_default = f_parts[1].strip() if len(f_parts) > 1 else ""
                fields.append(RecordFieldModel(name=f_name, default_val=f_default))

            records[rec_name] = RecordModel(name=rec_name, fields=fields, location=loc)
        return records

    def _parse_callbacks(self, text: str, file_path: str) -> dict[str, CallbackModel]:
        callbacks = {}
        pattern = re.compile(r"-callback\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)", re.MULTILINE)
        for m in pattern.finditer(text):
            cb_name = m.group(1)
            args_raw = m.group(2)
            arity = len(args_raw.split(",")) if args_raw.strip() else 0
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            callbacks[f"{cb_name}/{arity}"] = CallbackModel(name=cb_name, arity=arity, location=loc)
        return callbacks

    def _split_top_level_comma(self, text: str) -> list[str]:
        if not text.strip():
            return []
        items = []
        current = []
        depth = 0
        in_string = False
        quote_char = ""
        escape = False

        for c in text:
            if escape:
                escape = False
                current.append(c)
                continue
            if c == "\\" and in_string:
                escape = True
                current.append(c)
                continue
            if c in ('"', "'") and not in_string:
                in_string = True
                quote_char = c
                current.append(c)
            elif c == quote_char and in_string:
                in_string = False
                current.append(c)
            elif not in_string:
                if c in ("(", "{", "[", "<"):
                    depth += 1
                    current.append(c)
                elif c in (")", "}", "]", ">"):
                    depth -= 1
                    current.append(c)
                elif c == "," and depth == 0:
                    items.append("".join(current).strip())
                    current = []
                else:
                    current.append(c)
            else:
                current.append(c)

        if current:
            items.append("".join(current).strip())
        return [it for it in items if it]

    def _parse_functions(
        self, text: str, file_path: str, exports: list[tuple[str, int]]
    ) -> dict[str, FunctionModel]:
        functions: dict[str, FunctionModel] = {}
        export_set = set(exports)

        # Match function definition blocks ending with '.'
        # Example: name(Args) -> Body; name(Args2) -> Body2.
        blocks = re.finditer(r"(?<!-)\b([a-zA-Z0-9_]+)\s*\(([\s\S]*?)\)\s*(?:when\s+([^-]+?))?->([\s\S]+?)\.", text)

        for m in blocks:
            name = m.group(1)
            if name in ("record", "module", "export", "import", "behaviour", "behavior", "compile", "include", "ifdef", "endif"):
                continue

            args_raw = m.group(2)
            args_list = self._split_top_level_comma(args_raw)
            arity = len(args_list)

            # Check if this function is already declared in exports (e.g. handle_call/3)
            # If arity matches export or default, use it
            for exp_name, exp_arity in exports:
                if exp_name == name and exp_arity == arity:
                    break

            fn_id = f"{name}/{arity}"
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)
            body = m.group(0)

            # Analyze function calls: Mod:Func(
            call_matches = re.findall(r"\b([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+)\s*\(", body)
            calls = [(c[0], c[1], 0) for c in call_matches]

            has_receive = "receive" in body
            has_spawn = "spawn" in body or "spawn_link" in body
            has_try_catch = "try" in body or "catch" in body
            has_ets = "ets:" in body
            clause_count = 1 + body.count(f";\n{name}(") + body.count(f"; {name}(") + body.count(f";{name}(")
            complexity = 1 + body.count(";") + body.count("case") + body.count("if")

            clause = FunctionClauseModel(
                head_patterns=args_list,
                guard=m.group(3) or "",
                body=body,
                line=line_no,
            )

            if fn_id in functions:
                functions[fn_id].clauses.append(clause)
                functions[fn_id].cyclomatic_complexity += 1
                functions[fn_id].calls.extend(calls)
            else:
                is_exp = (name, arity) in export_set
                functions[fn_id] = FunctionModel(
                    name=name,
                    arity=arity,
                    clauses=[clause] * max(1, clause_count),
                    is_exported=is_exp,
                    cyclomatic_complexity=complexity,
                    calls=calls,
                    has_receive=has_receive,
                    has_spawn=has_spawn,
                    has_try_catch=has_try_catch,
                    has_ets_call=has_ets,
                    location=loc,
                )

        return functions
