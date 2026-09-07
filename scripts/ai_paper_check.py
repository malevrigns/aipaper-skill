#!/usr/bin/env python3
"""Locate manuscript editing candidates. Python 3.9+, standard library only."""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFENSE = re.compile(
    r"\bit is worth noting\b|\bit should be noted\b|\bto some extent\b|"
    r"\bin some cases\b|\bwe do not claim\b|\bunder certain conditions\b|"
    r"\binterpreted with caution\b|需要指出的是|在某种程度上|不能排除|谨慎解释", re.I)
INCONCLUSIVE = re.compile(
    r"\bcannot draw\b.{0,35}\bconclusions?\b|\bresults? (?:are|remain) (?:mixed|inconclusive)\b|"
    r"\bno statistically significant (?:difference|improvement)\b|无法得出.{0,8}结论|尚不能区分", re.I)
STATS = re.compile(
    r"\b(?:90|95|99)\s*%\s*(?:CI|confidence interval)\b|\bconfidence intervals?\b|"
    r"\bp\s*(?:[=<>≤≥]|\\(?:leq|geq))\s*(?:0?\.\d+|\d+(?:\.\d+)?(?:e[-+]?\d+)?)|"
    r"\bp[- ]values?\b|置信区间", re.I)
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|NEEDS REAL VALUE|INSERT RESULT HERE)\b|待填数值")
NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w.])")
TOKEN = re.compile(r"[\u4e00-\u9fff]|[a-z0-9]+(?:'[a-z]+)?", re.I)
SKIP_SECTION = re.compile(r"^(?:references|bibliography|参考文献|acknowledg(?:e)?ments?)\b", re.I)
APPENDIX = re.compile(r"^(?:appendix|appendices|supplement(?:ary)?|附录|补充材料)\b", re.I)
ABSTRACT = re.compile(r"^(?:abstract|摘要)\b", re.I)
KNOWN_HEADING = re.compile(
    r"^(?:(?:\d+(?:\.\d+)*\.?|[IVX]+\.?)\s+)?"
    r"(Introduction|Method(?:s|ology)?|Experiments?|Results?|Discussion|Conclusion(?:s)?|"
    r"Related Work|Limitations?|References|Bibliography|Abstract|Appendix(?:\s+\w+)?|"
    r"Supplementary(?: Material)?|引言|方法|实验|结果|结论|参考文献|摘要|附录)$", re.I)


def heading(line):
    m = re.match(r"^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
    if m:
        return m.group(1).strip()
    m = re.match(r"^\s*\\(?:sub)*section\*?(?:\[[^\]]*\])?\{([^}]+)\}", line)
    if m:
        return m.group(1).strip()
    m = KNOWN_HEADING.match(line.strip())
    return m.group(1) if m else None


def clean_heading(title):
    return re.sub(r"^(?:\d+(?:\.\d+)*\.?|[IVX]+\.?)\s+", "", title).strip()


def parse_text(text, source, include_appendix=False):
    """Preserve source line locations; exclude recognizable non-prose regions."""
    blocks, tables, pending, table_rows = [], [], [], []
    section, excluded, in_appendix = "body", False, False
    fence, environment = None, None
    counts = Counter()

    def flush():
        if pending:
            blocks.append({"source": source, "section": section,
                           "line": pending[0][0], "line_end": pending[-1][0],
                           "text": "\n".join(t for _, t in pending)})
            pending.clear()

    def flush_table():
        if table_rows:
            tables.append({"source": source, "section": section, "rows": list(table_rows)})
            table_rows.clear()

    for line_no, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        fm = re.match(r"^\s*(" + chr(96) + r"{3,}|~{3,})", raw)
        if fm:
            flush()
            flush_table()
            marker = fm.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            counts["non_prose_lines"] += 1
            continue
        if fence:
            counts["non_prose_lines"] += 1
            continue
        if environment:
            counts["non_prose_lines"] += 1
            if "\\end{" + environment + "}" in raw:
                environment = None
            continue
        em = re.search(r"\\begin\{(tabular\*?|tabularx|table\*?|equation\*?|align\*?|verbatim)\}", raw)
        if em:
            flush()
            flush_table()
            environment = em.group(1)
            if "\\end{" + environment + "}" in raw:
                environment = None
            counts["non_prose_lines"] += 1
            continue
        if s == "$$" or s == r"\[":
            flush()
            environment = "display_math"
            counts["non_prose_lines"] += 1
            continue
        title = heading(raw)
        if title:
            flush()
            flush_table()
            section = clean_heading(title)
            if APPENDIX.match(section):
                in_appendix = True
            excluded = bool(SKIP_SECTION.match(section) or
                            (in_appendix and not include_appendix))
            counts["headings"] += 1
            continue
        if excluded:
            counts["excluded_section_lines"] += 1
            continue
        if not s:
            flush()
            flush_table()
            continue
        if s.startswith("%") or s.startswith("![") or s.startswith(r"\includegraphics"):
            flush()
            counts["non_prose_lines"] += 1
            continue
        if "|" in raw and (s.startswith("|") or raw.count("|") >= 2):
            flush()
            cells = [x.strip() for x in s.strip("|").split("|")]
            table_rows.append((line_no, cells))
            counts["table_lines"] += 1
            continue
        flush_table()
        pending.append((line_no, raw))
    flush()
    flush_table()
    return blocks, tables, dict(counts)


def sentences(block):
    text = block["text"]
    # Split on sentence punctuation, but not decimal points or common abbreviations.
    start = 0
    for m in re.finditer(r"[。！？]|[.!?](?=\s|$)", text):
        before = text[start:m.end()]
        if re.search(r"\b(?:e\.g|i\.e|et al|Fig|Eq|Dr|Sec|vs)\.$", before, re.I):
            continue
        value = text[start:m.end()].strip()
        offset = start + len(text[start:m.end()]) - len(text[start:m.end()].lstrip())
        if value:
            yield {**block, "text": " ".join(value.split()),
                   "line": block["line"] + text[:offset].count("\n")}
        start = m.end()
    tail = text[start:].strip()
    if tail:
        offset = start + len(text[start:]) - len(text[start:].lstrip())
        yield {**block, "text": " ".join(tail.split()),
               "line": block["line"] + text[:offset].count("\n")}


def shingles(tokens, k=5):
    return {tuple(tokens[i:i+k]) for i in range(max(0, len(tokens)-k+1))}


def location(block, quote=None):
    return {"source": block["source"], "section": block["section"],
            "line": block["line"], "quote": quote if quote is not None else block["text"]}


def finding(code, title, evidence, suggestion, **extra):
    return {"code": code, "title": title, "status": "needs_context_review",
            "evidence": evidence, "suggestion": suggestion, **extra}


def analyze(sections, include_appendix=False, similarity=0.8,
            min_repeat_tokens=12, defense_threshold=3, stat_threshold=4):
    blocks, tables, excluded = [], [], Counter()
    for source, content in sections.items():
        # Display math has explicit delimiters; mask it without shifting lines.
        lines, math_mode = [], None
        for line in content.splitlines():
            s = line.strip()
            if s in ("$$", r"\[", r"\]"):
                if math_mode is None and s != r"\]":
                    math_mode = s
                elif (math_mode == "$$" and s == "$$") or (math_mode == r"\[" and s == r"\]"):
                    math_mode = None
                lines.append("")
            elif math_mode:
                lines.append("")
            elif s.startswith("$$") and s.endswith("$$"):
                lines.append("")
            else:
                lines.append(line)
        b, t, c = parse_text("\n".join(lines), source, include_appendix)
        blocks.extend(b)
        tables.extend(t)
        excluded.update(c)
    findings, observations = [], Counter()
    entries, index, duplicate_count = [], defaultdict(set), 0
    duplicate_examples_limit = 50
    for block in blocks:
        text = block["text"]
        defenses = list(DEFENSE.finditer(text))
        stats = list(STATS.finditer(text))
        observations["defensive_phrase_mentions"] += len(defenses)
        observations["statistic_mentions_in_prose"] += len(stats)
        observations["high_precision_numbers_in_prose"] += sum(
            len(n.group().split(".")[-1]) >= 5 for n in NUMBER.finditer(text)
            if "." in n.group() and "e" not in n.group().lower())
        if len(defenses) >= defense_threshold:
            findings.append(finding("B1_DEFENSE_CLUSTER", "成串限定语需要核对信息增量",
                [location(block)], "保留具体适用条件，检查是否有重复的空泛免责。"))
        if len(stats) >= stat_threshold:
            findings.append(finding("C2_STATS_CLUSTER", "统计量密集段落需要核对解释",
                [location(block)], "核对是否说明效应、比较对象与意义；关键统计量可以保留。"))
        for m in PLACEHOLDER.finditer(text):
            loc = location(block, m.group())
            loc["line"] += text[:m.start()].count("\n")
            findings.append(finding("E1_PLACEHOLDER", "可能尚未替换的内容", [loc],
                "检查是否为真实占位符；核实后填写或删除，不猜测结果。"))
        for sent in sentences(block):
            observations["inconclusive_sentence_mentions"] += bool(INCONCLUSIVE.search(sent["text"]))
            if ABSTRACT.match(sent["section"]):
                continue
            toks = TOKEN.findall(sent["text"].lower())
            if len(toks) < min_repeat_tokens:
                continue
            sh = shingles(toks)
            candidates = set()
            for key in sh:
                candidates.update(index[key])
            for j in sorted(candidates):
                prev, prior = entries[j]
                sim = len(sh & prior) / len(sh | prior)
                if sim >= similarity:
                    duplicate_count += 1
                    if duplicate_count <= duplicate_examples_limit:
                        findings.append(finding("B2_REPETITION", "长句重复候选",
                            [location(prev), location(sent)],
                            "检查第二次是否增加定义或证据；必要重述可以保留。",
                            similarity=round(sim, 3),
                            cross_section=(prev["source"], prev["section"]) !=
                                          (sent["source"], sent["section"])))
            current = len(entries)
            entries.append((sent, sh))
            for key in sh:
                index[key].add(current)

    for table in tables:
        rows = table["rows"]
        if len(rows) < 4 or not all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1][1]):
            continue
        headers = rows[0][1]
        for col, header in enumerate(headers):
            if re.search(r"\bp(?:[- ]?value)?\b|probability|epsilon", header, re.I):
                continue
            numeric = []
            for line_no, cells in rows[2:]:
                if col >= len(cells):
                    continue
                cell = cells[col].replace("*", "").strip()
                first = re.match(r"^\s*([-+]?\d+(?:\.\d+)?)(?![\d.eE])(?:\s*%|\s*(?:±|\+/-).+)?\s*$", cell)
                if first:
                    number = first.group(1)
                    precision = len(number.split(".")[1]) if "." in number else 0
                    numeric.append((line_no, cell, precision))
            if len(numeric) >= 2 and len({p for _, _, p in numeric}) > 1:
                ev = [{"source": table["source"], "section": table["section"],
                       "line": n, "quote": header + ": " + cell} for n, cell, _ in numeric]
                findings.append(finding("C1_TABLE_PRECISION", "表格同列精度需要核对", ev,
                    "先确认同一指标与单位，再统一显示精度；不要改动底层数据。"))
        for line_no, cells in rows[2:]:
            for cell in cells:
                if PLACEHOLDER.search(cell):
                    findings.append(finding("E1_PLACEHOLDER", "表格中可能尚未替换的内容",
                        [{"source": table["source"], "section": table["section"],
                          "line": line_no, "quote": cell}], "核实并填写真实结果。"))
    return {
        "schema_version": "2.0",
        "tool": "ai-paper-review",
        "summary": {"candidate_count": len(findings),
                    "repetition_pairs_total": duplicate_count,
                    "repetition_examples_truncated": duplicate_count > duplicate_examples_limit},
        "findings": findings,
        "observations": dict(sorted(observations.items())),
        "coverage": {
            "inputs": list(sections), "prose_blocks": len(blocks), "markdown_tables": len(tables),
            "include_appendix": include_appendix, "skipped": dict(excluded),
            "not_assessed": ["research motivation", "claim validity", "experimental adequacy",
                             "figure content and page layout", "authorship", "acceptance"],
            "parser_limits": "Heuristic text/Markdown/simple LaTeX parsing; PDF, OCR, complex macros, "
                             "HTML tables and cross-reference semantics are not supported.",
        },
        "settings": {"similarity": similarity, "min_repeat_tokens": min_repeat_tokens,
                     "defense_threshold": defense_threshold, "stat_threshold": stat_threshold},
        "note": "Candidates require contextual review. Counts are not scores; no finding is not a quality pass.",
    }


def render_markdown(report):
    lines = ["# Manuscript editing scan", "",
             f"Candidates: **{report['summary']['candidate_count']}**", "", report["note"], ""]
    for f in report["findings"]:
        lines.extend([f"## {f['code']} · {f['title']}", "", f"- Status: {f['status']}"])
        for e in f["evidence"]:
            quote = e["quote"].replace("\n", " ")
            lines.append(f"- {e['source']}:{e['line']} ({e['section']}): {quote}")
        lines.extend(["", f["suggestion"], ""])
    lines.extend(["## Coverage", "", "Not assessed: " + ", ".join(report["coverage"]["not_assessed"]),
                  "", report["coverage"]["parser_limits"], ""])
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("text", nargs="?", help="UTF-8 .txt, .md or simple .tex file")
    ap.add_argument("--sections", nargs="+", help="one file per section; full paths stay distinct")
    ap.add_argument("--json", dest="json_path", help="write schema v2 JSON report")
    ap.add_argument("--markdown", help="write readable Markdown report")
    ap.add_argument("--include-appendix", action="store_true")
    ap.add_argument("--fail-on-findings", action="store_true", help="exit 1 if candidates exist")
    ap.add_argument("--similarity", type=float, default=0.8)
    ap.add_argument("--min-repeat-tokens", type=int, default=12)
    ap.add_argument("--defense-threshold", type=int, default=3)
    ap.add_argument("--stat-threshold", type=int, default=4)
    args = ap.parse_args(argv)
    if bool(args.text) == bool(args.sections):
        ap.error("provide exactly one of a text file or --sections")
    if not 0 < args.similarity <= 1 or min(args.min_repeat_tokens, args.defense_threshold, args.stat_threshold) < 1:
        ap.error("similarity must be in (0, 1]; token and count thresholds must be positive")
    paths = [Path(p) for p in (args.sections or [args.text])]
    if len({p.resolve() for p in paths}) != len(paths):
        ap.error("the same input file was supplied more than once")
    outputs = [Path(p) for p in [args.json_path, args.markdown] if p]
    resolved_outputs = [p.resolve() for p in outputs]
    if set(resolved_outputs) & {p.resolve() for p in paths} or len(set(resolved_outputs)) != len(outputs):
        ap.error("report paths must be distinct from each other and from inputs")
    try:
        sections = {}
        for p in paths:
            if p.suffix.lower() not in {".txt", ".md", ".tex"}:
                ap.error("only .txt, .md and .tex are supported; extract PDF text first")
            sections[str(p)] = p.read_text(encoding="utf-8-sig")
        report = analyze(sections, args.include_appendix, args.similarity,
                         args.min_repeat_tokens, args.defense_threshold, args.stat_threshold)
        md = render_markdown(report)
        if args.json_path:
            Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if args.markdown:
            Path(args.markdown).write_text(md, encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        ap.error(str(exc))
    print(md)
    return 1 if args.fail_on_findings and report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
