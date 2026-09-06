#!/usr/bin/env python3
"""
ai_paper_check.py — Quantitative "AI-flavor" scanner for research papers.

Feeds a paper's plain text (optionally section-tagged) and computes the
observable signals defined in checklists/ai_flavor.md:

  * hedging density          (over-defensive / disclaimer overload)   -> B1
  * cross-section duplication (same sentence in Intro & Method)       -> B2
  * inconclusive ratio        (raw-log style results)                 -> C5
  * decimal inconsistency     (messy data reporting)                  -> C1
  * raw-stat-in-body          (CI / p-value dumped into prose)        -> C2
  * low info-density proxy    (very long sentences, few clauses)      -> B3

Then maps hits to an AI-Flavor Score (0-10) + verdict per rubric.md.

Usage:
  python ai_paper_check.py paper.txt
  python ai_paper_check.py --sections intro.txt method.txt exp.txt
  python ai_paper_check.py paper.txt --json out.json

--sections: each file = one section; label = filename stem before first digit.
No third-party deps (stdlib only). Exit code = rounded score (0-10).
"""
import re
import sys
import json
import argparse



# --- Signal detectors -------------------------------------------------------

HEDGE_PATTERNS = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bcan be argued\b",
    r"\bto some extent\b", r"\bit is worth noting\b", r"\bit should be noted\b",
    r"\bwe argue (that|cautiously)\b", r"\bappears? to\b", r"\bpotentially\b",
    r"\bin some cases\b", r"\bunder certain conditions\b", r"\bto the best of our knowledge\b",
    r"\bwe do not claim\b", r"\bthis is not to say\b", r"\bwith the caveat\b",
    r"\bmay not necessarily\b", r"\bsuggests that\b",
]

INCONCLUSIVE_PATTERNS = [
    r"cannot draw (any )?(a )?robust conclusion",
    r"no (clear |statistically significant )?(improvement|gain)",
    r"results are (inconclusive|mixed|not conclusive)",
    r"we (are unable|fail) to (draw|establish) a (clear|robust|definitive)",
    r"no statistically significant difference",
    r"the results do not (support|confirm)",
]

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def split_sentences(text):
    """Split into sentences; return list of normalized non-trivial sentences."""
    raw = SENT_SPLIT.split(text.strip())
    out = []
    for s in raw:
        s = " ".join(s.split())
        if len(s.split()) >= 6:  # ignore fragments
            out.append(s)
    return out


def hedge_density(text):
    """B1: hedging phrases per paragraph."""
    paras = [p for p in text.split("\n") if len(p.split()) >= 5]
    n_paras = max(len(paras), 1)
    hits = {}
    total = 0
    low = text.lower()
    for pat in HEDGE_PATTERNS:
        c = len(re.findall(pat, low))
        if c:
            hits[pat] = c
            total += c
    return {
        "total_hedges": total,
        "per_paragraph": round(total / n_paras, 2),
        "n_paragraphs": n_paras,
        "breakdown": hits,
        "hit": total / n_paras > 3.0,   # rubric red line: >3/para
    }


def _shingles(tokens, k=6):
    return set(tuple(tokens[i:i + k]) for i in range(max(len(tokens) - k, 0)))


def cross_section_duplication(sections):
    """B2: near-duplicate sentences appearing in DIFFERENT sections.

    sections: dict {label: text}. Uses 6-word shingle Jaccard similarity;
    a pair with sim >= 0.5 across different sections counts as duplication.
    """
    sents = {}   # label -> list of (text, shingles)
    for lab, txt in sections.items():
        arr = []
        for s in split_sentences(txt):
            toks = re.findall(r"[a-z0-9']+", s.lower())
            if len(toks) >= 8:
                arr.append((s, _shingles(toks)))
        sents[lab] = arr

    pairs = []
    labels = list(sents.keys())
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            la, lb = labels[i], labels[j]
            for sa, sha in sents[la]:
                for sb, shb in sents[lb]:
                    if not sha or not shb:
                        continue
                    inter = len(sha & shb)
                    union = len(sha | shb)
                    sim = inter / union if union else 0
                    if sim >= 0.5:
                        pairs.append({
                            "similarity": round(sim, 2),
                            "section_a": la, "section_b": lb,
                            "sentence_a": sa[:140], "sentence_b": sb[:140],
                        })
    pairs.sort(key=lambda p: -p["similarity"])
    return {"pairs": pairs, "count": len(pairs), "hit": len(pairs) >= 1}


def inconclusive_ratio(text):
    """C5: fraction of result sentences that are inconclusive."""
    low = text.lower()
    n_inc = sum(len(re.findall(p, low)) for p in INCONCLUSIVE_PATTERNS)
    # proxy denominator: count experiment-ish result statements
    n_res = max(n_inc, len(re.findall(r"\bwe (find|observe|show|report|evaluate)\b", low)), 1)
    ratio = round(min(n_inc / max(n_inc + (n_res - n_inc), 1), 1.0), 3) \
        if n_inc else 0.0
    # simpler robust metric: inconclusive mentions vs total hedged-result verbs
    total_result_verbs = len(re.findall(
        r"\bwe (find|observe|show|report|evaluate|cannot|are unable|fail)\b", low))
    frac = round(n_inc / total_result_verbs, 3) if total_result_verbs else 0.0
    return {
        "inconclusive_mentions": n_inc,
        "result_verb_total": total_result_verbs,
        "fraction_inconclusive": frac,
        "hit": bool(total_result_verbs and frac > 0.5),
    }


def decimal_inconsistency(text):
    """C1: how many distinct decimal precisions appear in numbers."""
    nums = re.findall(r"\d+\.\d+", text)
    precisions = set(len(n.split(".")[1]) for n in nums)
    # ignore precision 0 (integers written as x.0 handled above -> length>=1)
    return {
        "n_decimal_numbers": len(nums),
        "distinct_precisions": sorted(precisions),
        "max_precision": max(precisions) if precisions else 0,
        "hit": (len(precisions) > 1) or (precisions and max(precisions) >= 5),
    }


def raw_stat_in_body(text):
    """C2: CI / p-value raw statistics mentioned in prose (not tables)."""
    ci = len(re.findall(r"(?:9[05]|confidence)\s*(?:%|\s)?\s*CI|confidence interval", text, re.I))
    pval = len(re.findall(r"\bp\s*[=<]\s*0?\.\d+|\bp-value\b|\bp\s*=\s*\d", text, re.I))
    total = ci + pval
    return {"ci_mentions": ci, "pvalue_mentions": pval, "total": total,
            "hit": total >= 3}


# --- Scoring (mirrors rubric.md weights) ------------------------------------

def compute_score(hedge, dup, incon, dec, rawstat):
    """Map signal hits to AI-Flavor Score (0-10) using rubric.md weights."""
    score = 0.0
    detail = []
    if hedge["hit"]:
        w = min(2.0, 1.0 + (hedge["per_paragraph"] - 3) / 5)
        score += w
        detail.append(("B1 over-hedging", round(w, 2),
                       "%s hedges/para" % hedge["per_paragraph"]))
    if dup["hit"]:
        score += 2.0
        detail.append(("B2 cross-section duplication", 2.0,
                       "%d pair(s)" % dup["count"]))
    if incon["hit"]:
        score += 2.0
        detail.append(("C5 inconclusive results", 2.0,
                       "frac=%.2f" % incon["fraction_inconclusive"]))
    if dec["hit"]:
        score += 1.5
        detail.append(("C1 decimal inconsistency", 1.5,
                       "precisions=%s" % dec["distinct_precisions"]))
    if rawstat["hit"]:
        score += 1.0
        detail.append(("C2 raw-stat-in-body", 1.0,
                       "%d mentions" % rawstat["total"]))
    return round(min(score, 10.0), 2), detail


def verdict(score):
    if score <= 2:
        return "Likely human (minor AI polish)"
    if score <= 5:
        return "Mixed (clear AI assistance; verify storyline & experiments)"
    if score <= 8:
        return "Likely AIGC (check motivation, ablation completeness, data norms)"
    return "Very likely raw-AutoResearch (author may not have checked; desk-reject candidate)"


def analyze(sections):
    """sections: dict {label: text}. Returns full report dict."""
    full_text = "\n\n".join(sections.values())
    hedge = hedge_density(full_text)
    dup = cross_section_duplication(sections)
    incon = inconclusive_ratio(full_text)
    dec = decimal_inconsistency(full_text)
    rawstat = raw_stat_in_body(full_text)
    score, detail = compute_score(hedge, dup, incon, dec, rawstat)
    return {
        "ai_flavor_score": score,
        "verdict": verdict(score),
        "signals": {
            "B1_hedging": hedge,
            "B2_cross_section_duplication": dup,
            "C5_inconclusive_ratio": incon,
            "C1_decimal_inconsistency": dec,
            "C2_raw_stat_in_body": rawstat,
        },
        "score_breakdown": [{"item": a, "weight": b, "evidence": c} for a, b, c in detail],
        "note": ("Quantitative proxy only. 'Rigor' is not a defect: honest negative "
                 "results are fine; the red flags are over-hedging, verbatim "
                 "cross-section repetition, and mostly-inconclusive experiments."),
    }


def main():
    ap = argparse.ArgumentParser(description="AI-flavor scanner for papers")
    ap.add_argument("text", nargs="?", help="single paper .txt file")
    ap.add_argument("--sections", nargs="+", help="one file per section")
    ap.add_argument("--json", help="write JSON report to this path")
    args = ap.parse_args()

    sections = {}
    if args.sections:
        for f in args.sections:
            stem = re.split(r"\d|_", os.path.basename(f))[0] or f
            with open(f, encoding="utf-8", errors="ignore") as fh:
                sections[stem] = fh.read()
    elif args.text:
        with open(args.text, encoding="utf-8", errors="ignore") as fh:
            sections["full"] = fh.read()
    else:
        sys.stderr.write("provide a text file or --sections\n")
        return 2

    rep = analyze(sections)
    print("AI-Flavor Score : %.2f / 10" % rep["ai_flavor_score"])
    print("Verdict         : %s" % rep["verdict"])
    print("\nScore breakdown:")
    for d in rep["score_breakdown"]:
        print("  +%-4s %-32s (%s)" % (str(d["weight"]), d["item"], d["evidence"]))
    s = rep["signals"]
    print("\nSignals:")
    print("  B1 hedging      : %s/para  [hit=%s]" % (s["B1_hedging"]["per_paragraph"], s["B1_hedging"]["hit"]))
    print("  B2 x-section dup: %d pair(s) [hit=%s]" % (s["B2_cross_section_duplication"]["count"], s["B2_cross_section_duplication"]["hit"]))
    if s["B2_cross_section_duplication"]["pairs"]:
        p = s["B2_cross_section_duplication"]["pairs"][0]
        print("      top: [%s]~[%s] sim=%.2f" % (p["section_a"], p["section_b"], p["similarity"]))
        print('        A: "%s"' % p["sentence_a"])
        print('        B: "%s"' % p["sentence_b"])
    print("  C5 inconclusive : frac=%.2f     [hit=%s]" % (s["C5_inconclusive_ratio"]["fraction_inconclusive"], s["C5_inconclusive_ratio"]["hit"]))
    print("  C1 decimals     : precisions=%s [hit=%s]" % (s["C1_decimal_inconsistency"]["distinct_precisions"], s["C1_decimal_inconsistency"]["hit"]))
    print("  C2 raw-stat     : %d mentions   [hit=%s]" % (s["C2_raw_stat_in_body"]["total"], s["C2_raw_stat_in_body"]["hit"]))
    print("\nNote:", rep["note"])
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=2)
        print("\nJSON report ->", args.json)
    return int(round(rep["ai_flavor_score"]))


if __name__ == "__main__":
    import os
    sys.exit(main())
