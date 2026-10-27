"""Keyword statistics for the ACL abstract translations.

Open-source stack: scikit-learn (stop words), wordcloud, matplotlib.
Reads English abstracts from papers/abstracts-翻译 and writes
frequency word clouds, year-distinctive word clouds, and a seed-term chart.

  python3 analysis/abstract_keywords.py
  python3 analysis/abstract_keywords.py --max-words 300 --top 80 --min-docs 1
  python3 analysis/abstract_keywords.py --max-df 0.4
  python3 analysis/abstract_keywords.py --keep-common --max-df 1 --sections 1-建议通读 2-相邻
"""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from wordcloud import WordCloud

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "papers" / "abstracts-翻译"
OUT = ROOT / "analysis" / "keyword_stats"
SECTIONS = ("1-建议通读", "2-相邻", "3-关键词撞车")
YEARS = ("2024", "2025", "2026")

TOKEN = re.compile(r"[a-z][a-z0-9]+(?:-[a-z0-9]+)*")
ABSTRACT = re.compile(r"## 英文原文摘要[^\n]*\n+(.*?)(?:\n## |\Z)", re.S)

# Function words plus boilerplate that appears in almost every abstract.
STOP = set(ENGLISH_STOP_WORDS) | {
    "paper", "papers", "propose", "proposed", "proposes", "method", "methods",
    "approach", "approaches", "result", "results", "show", "shows", "shown",
    "using", "used", "use", "based", "task", "tasks", "dataset", "datasets",
    "experiment", "experiments", "experimental", "performance", "framework",
    "novel", "existing", "work", "study", "studies", "present", "presents",
    "introduce", "introduces", "introduced", "including", "different", "various",
    "via", "across", "within", "without", "toward", "towards", "however",
    "significantly", "significant", "demonstrate", "demonstrates", "demonstrated",
    "achieve", "achieves", "achieved", "extensive", "new", "two", "three",
    "first", "second", "also", "well", "can", "may", "one", "et", "al",
    "effect", "effects", "issue", "issues", "address", "detailed", "automatic",
    "progress", "promising", "current", "relative", "fig", "figure", "table",
    "github", "http", "https", "available", "code",
    "our", "we", "this", "these", "such", "than", "into", "from",
}
# Shared topic words. Removed from the frequency cloud only, so it shows
# what the abstracts talk about besides "LLM recommendation system".
CLOUD_EXTRA = {
    "recommendation", "recommendations", "recommender", "recommenders",
    "recommend", "recommended", "system", "systems", "user", "users",
    "item", "items", "model", "models", "language", "llm", "llms", "large",
    "learning", "data", "information", "research", "real", "world",
}

# Phrases tracked as the share of abstracts that mention them.
SEEDS = [
    ("agent", r"\bagents?\b|\bagentic\b"),
    ("user simulator", r"user simul"),
    ("reinforcement / DPO", r"\breinforcement learning\b|\bgrpo\b|\bdpo\b|\bpreference optimization\b"),
    ("reasoning", r"\breasoning\b"),
    ("conversational", r"conversation"),
    ("memory", r"\bmemor"),
    ("shopping / e-commerce", r"shopping|\be-?commerce\b"),
    ("personalization", r"personali[sz]"),
    ("benchmark", r"\bbenchmark"),
    ("retrieval / RAG", r"\bretriev|\brag\b"),
    ("multimodal", r"multimodal"),
    ("collaborative", r"collaborative"),
]


def load(section: str, year: str) -> list[str]:
    folder = SRC / section / year
    texts = []
    for path in sorted(folder.glob("*.md")):
        match = ABSTRACT.search(path.read_text())
        if match:
            texts.append(match.group(1).strip())
    return texts


def tokenize(text: str) -> list[str]:
    words = TOKEN.findall(text.lower().replace("–", "-").replace("—", "-"))
    return [w for w in words if w not in STOP and len(w) > 2 and not w.isdigit()]


def doc_counter(texts: list[str]) -> Counter:
    counts: Counter = Counter()
    for text in texts:
        words = tokenize(text)
        counts.update(set(words) | set(ngrams(words, 2)))
    return counts


def ngrams(words: list[str], n: int) -> list[str]:
    if n == 1:
        return words
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def log_odds(
    year_counts: Counter,
    other_counts: Counter,
    year_docs: Counter,
    min_docs: int = 2,
) -> list[tuple[str, float, int]]:
    """Monroe-style log-odds vs the other years, with a 0.5 prior.

    min_docs drops a method name that one abstract repeats.
    """
    scored = []
    for term, count in year_counts.items():
        if year_docs[term] < min_docs:
            continue
        other = other_counts[term]
        lor = math.log(count + 0.5) - math.log(other + 0.5)
        var = 1 / (count + 0.5) + 1 / (other + 0.5)
        scored.append((term, lor / math.sqrt(var), count))
    scored.sort(key=lambda row: row[1], reverse=True)
    return scored


def project_rate(rates: list[float]) -> float:
    """Linear fit on 2024, 2025, 2026 (t = 0, 1, 2) and evaluate at 2027."""
    mean_y = sum(rates) / 3
    slope = ((-1) * (rates[0] - mean_y) + (rates[2] - mean_y)) / 2
    intercept = mean_y - slope
    return max(0.0, intercept + slope * 3)


def cloud(frequencies: dict[str, float], path: Path, color: str, max_words: int, title: str = "") -> None:
    if not frequencies:
        return
    image = WordCloud(
        width=1600,
        height=900,
        background_color="white",
        max_words=max_words,
        collocations=False,
        prefer_horizontal=0.9,
        relative_scaling=0.4,
        color_func=lambda *args, **kwargs: color,
        random_state=0,
    ).generate_from_frequencies(frequencies)
    figure, ax = plt.subplots(figsize=(11, 6.2))
    ax.imshow(image, interpolation="bilinear")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=14, pad=8)
    figure.tight_layout(pad=0.4)
    figure.savefig(path, dpi=140)
    plt.close(figure)


def seed_chart(rows: dict[str, dict[str, float]], path: Path) -> None:
    labels = [name for name, _ in SEEDS]
    colors = {"2024": "#4C78A8", "2025": "#F58518", "2026": "#54A24B"}
    figure, ax = plt.subplots(figsize=(10, 7))
    import numpy as np

    y = np.arange(len(labels))
    height = 0.25
    for index, year in enumerate(YEARS):
        values = [rows[year][name] for name in labels]
        ax.barh(y + (index - 1) * height, values, height=height, label=year, color=colors[year])
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Share of abstracts mentioning the phrase (%)")
    ax.invert_yaxis()
    ax.legend()
    ax.set_xlim(0, 100)
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)


def below_max_df(frequencies: dict[str, float], doc_counts: Counter, n_docs: int, max_df: float) -> dict[str, float]:
    """Drop terms that show up in too many abstracts. This is sklearn's max_df."""
    if n_docs == 0 or max_df >= 1:
        return frequencies
    return {term: weight for term, weight in frequencies.items() if doc_counts[term] / n_docs <= max_df}


def write_table(path: Path, blocks: list[str]) -> None:
    path.write_text("\n".join(blocks) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Abstract keyword counts and word clouds.")
    parser.add_argument("--max-words", type=int, default=200, help="words drawn in each word cloud (default 200)")
    parser.add_argument("--top", type=int, default=60, help="rows kept in each year's distinctive-term table (default 60)")
    parser.add_argument("--min-docs", type=int, default=2, help="a distinctive term must appear in at least this many abstracts that year (default 2; use 1 to keep rare words)")
    parser.add_argument("--keep-common", action="store_true", help="keep recommendation/user/model/llm in the frequency clouds")
    parser.add_argument("--max-df", type=float, default=0.5, help="drop a word from frequency clouds if it appears in more than this fraction of abstracts (default 0.5; use 1 to disable)")
    parser.add_argument("--sections", nargs="+", default=["1-建议通读"], choices=SECTIONS, help="which abstract folders to pool (default: 1-建议通读)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    colors = {"2024": "#4C78A8", "2025": "#F58518", "2026": "#54A24B"}
    hidden = set() if args.keep_common else CLOUD_EXTRA
    by_year = {year: [] for year in YEARS}
    for section in args.sections:
        for year in YEARS:
            by_year[year].extend(load(section, year))
    counts = {year: len(texts) for year, texts in by_year.items()}

    bags = {year: Counter(ngrams(sum((tokenize(text) for text in texts), []), 1)) for year, texts in by_year.items()}
    bigrams = {year: Counter(ngrams(sum((tokenize(text) for text in texts), []), 2)) for year, texts in by_year.items()}
    docs = {year: doc_counter(texts) for year, texts in by_year.items()}

    lines = [
        "# 建议通读摘要的关键词",
        "",
        f"语料文件夹：{', '.join(args.sections)}。不包含 `recommendation/` 里的重复笔记。",
        "参数："
        f" --max-words {args.max_words}"
        f" --top {args.top}"
        f" --min-docs {args.min_docs}"
        f" --max-df {args.max_df}"
        f"{' --keep-common' if args.keep_common else ''}。",
        "词频词云默认去掉 recommendation、user、model、llm，并且丢掉出现在超过 --max-df 比例摘要里的词。--keep-common 只取消前一份手写名单；--max-df 1 才连文档频率过滤一起关掉。",
        "区分词是相对其他年份的对数优势比，并且至少出现在该年的 --min-docs 篇摘要里。",
        "种子词是摘要里是否出现该短语，分母是该年摘要篇数。",
        "",
        "| 年 | 摘要篇数 |",
        "|---|---|",
    ]
    for year in YEARS:
        lines.append(f"| {year} | {counts[year]} |")
    lines.append("")

    for year in YEARS:
        freq = below_max_df(
            {term: count for term, count in bags[year].items() if term not in hidden},
            docs[year],
            counts[year],
            args.max_df,
        )
        cloud(freq, OUT / f"freq_{year}.png", colors[year], args.max_words)
        other = Counter()
        other_bi = Counter()
        for other_year in YEARS:
            if other_year == year:
                continue
            other.update(bags[other_year])
            other_bi.update(bigrams[other_year])
        distinctive = log_odds(bags[year] + bigrams[year], other + other_bi, docs[year], args.min_docs)
        cloud(
            {term: score for term, score, _ in distinctive[: args.max_words] if score > 0},
            OUT / f"distinct_{year}.png",
            colors[year],
            args.max_words,
        )
        lines.append(f"## {year} 相对其他年份更常出现")
        lines.append("")
        lines.append("| 词 | 对数优势比 z | 该年次数 |")
        lines.append("|---|---|---|")
        for term, score, count in distinctive[: args.top]:
            lines.append(f"| {term} | {score:.2f} | {count} |")
        lines.append("")

    all_freq: Counter = Counter()
    all_docs: Counter = Counter()
    n_docs = sum(counts.values())
    for year in YEARS:
        all_freq.update({term: count for term, count in bags[year].items() if term not in hidden})
        all_docs.update(docs[year])
    cloud(below_max_df(dict(all_freq), all_docs, n_docs, args.max_df), OUT / "freq_all.png", "#333333", args.max_words)

    seed_rows = {}
    lines.append("## 种子短语：多少篇摘要提到")
    lines.append("")
    header = "| 短语 | " + " | ".join(f"{year} (n={counts[year]})" for year in YEARS) + " |"
    lines.append(header)
    lines.append("|---|" + "---|" * len(YEARS))
    for name, pattern in SEEDS:
        compiled = re.compile(pattern, re.I)
        seed_rows[name] = {}
        cells = []
        for year in YEARS:
            hits = sum(1 for text in by_year[year] if compiled.search(text))
            pct = 100 * hits / counts[year]
            seed_rows[name][year] = pct
            cells.append(f"{hits} ({pct:.0f}%)")
        # reshape below
        lines.append("| " + name + " | " + " | ".join(cells) + " |")
    # seed_chart expects year -> name -> pct
    chart_rows = {year: {name: seed_rows[name][year] for name, _ in SEEDS} for year in YEARS}
    seed_chart(chart_rows, OUT / "seed_share.png")
    pooled_docs: Counter = Counter()
    for year in YEARS:
        pooled_docs.update(docs[year])
    projected = {}
    for term in set().union(*bags.values()):
        if term in hidden:
            continue
        # Filter on the observed three-year share, not the projected share.
        # Otherwise a word that is rising into common use, such as reasoning, disappears.
        if n_docs and pooled_docs[term] / n_docs > args.max_df:
            continue
        if docs["2026"][term] < 2:
            continue
        weight = project_rate([bags[year][term] / counts[year] for year in YEARS])
        if weight > 0:
            projected[term] = weight
    cloud(
        projected,
        OUT / "freq_2027_projected.png",
        "#6B4C9A",
        args.max_words,
        title="2027 projected word frequency (not observed)",
    )
    ranked = sorted(projected.items(), key=lambda item: item[1], reverse=True)
    lines.append("## 2027 预估词频")
    lines.append("")
    lines.append("不是 2027 年的真实摘要。每个词用 2024、2025、2026 的「每篇摘要出现次数」做直线外推。`--max-df` 只用在这三年已经观察到的占比上，避免把正在变常见的词删掉。2026 年只出现在一篇摘要里的词不外推。")
    lines.append("")
    lines.append("| 词 | 预估每篇出现次数 |")
    lines.append("|---|---|")
    for term, weight in ranked[: args.top]:
        lines.append(f"| {term} | {weight:.2f} |")
    lines.append("")
    lines.append("图：`freq_YYYY.png` 词频词云，`distinct_YYYY.png` 区分词词云，`seed_share.png` 种子短语占比，`freq_all.png` 三年合计词频，`freq_2027_projected.png` 是外推。")
    write_table(OUT / "关键词统计.md", lines)
    print({year: counts[year] for year in YEARS})
    print("wrote", OUT)


if __name__ == "__main__":
    main()
