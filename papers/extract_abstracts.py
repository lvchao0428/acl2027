#!/usr/bin/env python3
"""Extract abstracts from PDFs - column-aware extraction."""
import os
import re
import json
import pymupdf

SRC_DIR = "/Users/a58/project/paper/acl2027/papers/acl2024-2026/3-关键词撞车"
OUT_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/3-关键词撞车"
RAW_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/_raw_extracts"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

PDFS = [
    "A Semi-supervised Scalable Unified Framework for E-commerce Query Classification.pdf",
    "Agent-Ops - A Multi-Agent Orchestration Framework for End-to-End SOP Automation in E-Commerce Operations.pdf",
    "AIGuard - A Benchmark and Lightweight Detection for E-commerce AIGC Risks.pdf",
    "Aligning AI Research with the Needs of Clinical Coding Workflows - Eight Recommendations Based on US Data Analysis and Critical Review.pdf",
    "AutoPKG - An Automated Framework for Dynamic E-commerce Product-Attribute Knowledge Graph Construction.pdf",
    "Chinese Live-Streaming E-Commerce Morph Resolution - Datasets and Methods.pdf",
    "ConECT Dataset - Overcoming Data Scarcity in Context-Aware E-Commerce MT.pdf",
    "DiaLLMs - EHR-Enhanced Clinical Conversational System for Clinical Test Recommendation and Diagnosis Prediction.pdf",
    "Domain Adaptation of Foundation LLMs for e-Commerce.pdf",
    "E-ABSA20K - A Dataset and Propose-and-Verify for Aspect-Based Sentiment Analysis in Long E-commerce Reviews.pdf",
    "Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce.pdf",
    "LLM-Enhanced Self-Evolving Reinforcement Learning for Multi-Step E-Commerce Payment Fraud Risk Detection.pdf",
    "MICE - Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction.pdf",
    "MIRA - Empowering One-Touch AI Services on Smartphones with MLLM-based Instruction Recommendation.pdf",
    "MTIVE - Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce.pdf",
    "Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning.pdf",
    "Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce.pdf",
    "ProvBench - A Benchmark of Legal Provision Recommendation for Contract Auto-Reviewing.pdf",
    "Scholar Inbox - Personalized Paper Recommendations for Scientists.pdf",
    "Stronger, Lighter, Better - Towards Life-Long Attribute Value Extraction for E-Commerce Products.pdf",
    "SymTax - Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation.pdf",
    "TablePilot - Recommending Human-Preferred Tabular Data Analysis with Large Language Models.pdf",
    "Visualization Recommendation with Prompt-based Reprogramming of Large Language Models.pdf",
]


def page_text_column_aware(page):
    """Extract text from a page, handling two-column layout.

    Strategy: get all blocks with coordinates. If page width > 400 and blocks
    clearly split into two columns, sort left column top-to-bottom then right.
    Otherwise use normal sort.
    """
    blocks = page.get_text("blocks", sort=False)
    # blocks: (x0, y0, x1, y1, text, block_no, block_type)
    # Filter out empty / image blocks
    text_blocks = [b for b in blocks if b[6] == 0 and b[4].strip()]
    if not text_blocks:
        return ""

    page_w = page.rect.width
    page_h = page.rect.height

    # Detect two-column: split at mid. Check if most blocks are in left or right half
    mid = page_w / 2
    left = [b for b in text_blocks if (b[0] + b[2]) / 2 < mid]
    right = [b for b in text_blocks if (b[0] + b[2]) / 2 >= mid]

    # Heuristic: if there are substantial blocks on both sides and they're narrow
    if left and right and len(left) >= 2 and len(right) >= 2:
        left_widths = [b[2] - b[0] for b in left]
        right_widths = [b[2] - b[0] for b in right]
        avg_left_w = sum(left_widths) / len(left)
        avg_right_w = sum(right_widths) / len(right)
        # If columns are roughly half page width, treat as two-column
        if avg_left_w < page_w * 0.6 and avg_right_w < page_w * 0.6:
            left.sort(key=lambda b: (b[1], b[0]))
            right.sort(key=lambda b: (b[1], b[0]))
            ordered = left + right
            return "\n".join(b[4] for b in ordered)

    # Single column: sort by y then x
    text_blocks.sort(key=lambda b: (round(b[1] / 5), b[0]))
    return "\n".join(b[4] for b in text_blocks)


def extract_abstract_from_text(text: str):
    """Locate abstract in extracted text.

    Returns (abstract_text, method).
    """
    if not text or len(text.strip()) < 100:
        return "", "empty"

    # Normalize whitespace per line but keep line structure
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l]

    # Find abstract heading
    abs_idx = -1
    for i, line in enumerate(lines[:60]):
        s = line.strip().rstrip(":").strip()
        if re.fullmatch(r"(Abstract|ABSTRACT|Summary|SUMMARY|摘要)", s):
            abs_idx = i
            break

    if abs_idx >= 0:
        # Collect until next section heading
        start = abs_idx + 1
        body = []
        for j in range(start, min(len(lines), start + 80)):
            s = lines[j].strip()
            # Stop conditions - common section headers
            if re.match(r"^(1\s+Introduction|I\.\s+Introduction|Introduction\s*$|Index Terms|Keywords|CCS\s+CONCEPTS|CCS\s+Concepts|1\s+Related Work|Related Work\s*$|1\s+Methodology|1\s+Method|1\s+Approach|1\s+Overview|1\s+Background|1\s+Model)", s, re.IGNORECASE):
                break
            # Numbered section like "1. Introduction" or "1 Introduction"
            if re.match(r"^\d+[\.\)]\s+[A-Z]", s) and len(s) < 80:
                break
            # Capitalized short heading
            if re.match(r"^[A-Z][A-Za-z\s]{3,40}$", s) and len(body) > 30:
                # Could be a section header
                break
            body.append(lines[j])
        abstract = " ".join(body)
        abstract = re.sub(r"\s+", " ", abstract).strip()
        if len(abstract) > 300:
            return abstract, "abstract_label"

    # Fallback: find first long paragraph (joined lines) that looks like abstract
    # Join all text and find the first ~200-3000 char run
    full = re.sub(r"\s+", " ", text).strip()
    # Try to locate "Abstract" inline
    m = re.search(r"\bAbstract[:\.\s]+", full, re.IGNORECASE)
    if m:
        rest = full[m.end():].strip()
        # Cut at common stop phrases
        stops = [r"\s+1\.\s+Introduction", r"\s+1\s+Introduction", r"\s+Index Terms", r"\s+Keywords", r"\s+CCS\s+Concepts", r"\s+Introduction\s"]
        cut = len(rest)
        for s in stops:
            mm = re.search(s, rest, re.IGNORECASE)
            if mm and mm.start() < cut:
                cut = mm.start()
        abstract = rest[:cut].strip()
        if len(abstract) > 300:
            return abstract, "abstract_inline"

    # Last fallback: return the first 2500 chars after skipping obvious title/author noise
    return full[:2500], "intro_start"


def process_pdf(pdf_path: str):
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        return None, f"open_failed: {e}"

    n = doc.page_count
    chunks = []
    for i in range(min(2, n)):
        chunks.append(page_text_column_aware(doc[i]))
    text = "\n\n".join(chunks)
    doc.close()

    if len(text.strip()) < 100:
        return {"text": text, "abstract": "", "method": "empty", "pages": n}, None

    abstract, method = extract_abstract_from_text(text)
    return {"text": text, "abstract": abstract, "method": method, "pages": n}, None


def main():
    results = {}
    for fname in PDFS:
        path = os.path.join(SRC_DIR, fname)
        stem = os.path.splitext(fname)[0]
        if not os.path.exists(path):
            results[fname] = {"error": "file_not_found"}
            continue
        data, err = process_pdf(path)
        if err:
            results[fname] = {"error": err}
            continue
        raw_path = os.path.join(RAW_DIR, stem + ".txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(data["text"])
        results[fname] = {
            "pages": data["pages"],
            "method": data["method"],
            "abstract_len": len(data["abstract"]),
            "abstract": data["abstract"],
        }

    out_json = os.path.join(RAW_DIR, "_abstracts.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    for fname, info in results.items():
        if "error" in info:
            print(f"[ERR] {fname}: {info['error']}")
        else:
            print(f"[{info['method']:14s}] len={info['abstract_len']:5d} pages={info['pages']:3d}  {fname}")


if __name__ == "__main__":
    main()
