from __future__ import annotations

import math
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import numpy as np

from college_data import load_college_dataset


_STOPWORDS = {
    "the",
    "and",
    "or",
    "for",
    "to",
    "in",
    "of",
    "a",
    "an",
    "with",
    "near",
    "at",
    "on",
    "is",
    "are",
    "be",
    "this",
    "that",
    "it",
    "as",
    "by",
    "from",
    "college",
    "institute",
    "university",
    "engineering",
    "diploma",
}


def _tokenize(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    toks = [t for t in text.split() if t and t not in _STOPWORDS and len(t) > 1]
    return toks


@dataclass(frozen=True)
class _TfidfIndex:
    vocab: dict[str, int]
    idf: np.ndarray  # (V,)
    matrix: np.ndarray  # (N, V) float32
    norms: np.ndarray  # (N,) float32
    docs: list[dict[str, Any]]


def _build_docs() -> list[dict[str, Any]]:
    dataset = load_college_dataset("cleaned.xlsx")
    df = dataset.df
    docs: list[dict[str, Any]] = []
    for _, r in df.iterrows():
        institute = str(r.get("Institute_Name", "")).strip()
        district = str(r.get("District", "")).strip()
        branch = str(r.get("Branch_Name", "")).strip()
        fee = r.get("Fee", None)
        content = f"{institute}. District: {district}. Branch: {branch}. Fee: {fee}."
        docs.append(
            {
                "content": content,
                "Institute_Name": institute,
                "District": district,
                "Branch_Name": branch,
                "Fee": fee,
            }
        )
    return docs


@lru_cache(maxsize=1)
def _get_index() -> _TfidfIndex:
    docs = _build_docs()
    tokenized = [_tokenize(d["content"]) for d in docs]

    # Build vocabulary
    df_counts: dict[str, int] = {}
    for toks in tokenized:
        for t in set(toks):
            df_counts[t] = df_counts.get(t, 0) + 1

    # Keep a reasonable vocab size (small dataset)
    vocab_terms = sorted(df_counts.keys())
    vocab = {t: i for i, t in enumerate(vocab_terms)}
    n_docs = len(docs)
    v = len(vocab)

    idf = np.zeros((v,), dtype=np.float32)
    for term, i in vocab.items():
        df_t = df_counts.get(term, 0)
        idf[i] = float(math.log((n_docs + 1) / (df_t + 1)) + 1.0)

    matrix = np.zeros((n_docs, v), dtype=np.float32)
    for di, toks in enumerate(tokenized):
        if not toks:
            continue
        tf: dict[int, int] = {}
        for t in toks:
            idx = vocab.get(t)
            if idx is None:
                continue
            tf[idx] = tf.get(idx, 0) + 1
        if not tf:
            continue
        max_tf = max(tf.values())
        for idx, cnt in tf.items():
            # sublinear tf scaling
            tf_w = 0.5 + 0.5 * (cnt / max_tf)
            matrix[di, idx] = tf_w * idf[idx]

    norms = np.linalg.norm(matrix, axis=1).astype(np.float32)
    return _TfidfIndex(vocab=vocab, idf=idf, matrix=matrix, norms=norms, docs=docs)


def retrieve_context(query: str, k: int = 5) -> list[dict[str, Any]]:
    idx = _get_index()
    toks = _tokenize(query)
    if not toks:
        return []

    q = np.zeros((len(idx.vocab),), dtype=np.float32)
    tf: dict[int, int] = {}
    for t in toks:
        ti = idx.vocab.get(t)
        if ti is None:
            continue
        tf[ti] = tf.get(ti, 0) + 1
    if not tf:
        return []

    max_tf = max(tf.values())
    for ti, cnt in tf.items():
        tf_w = 0.5 + 0.5 * (cnt / max_tf)
        q[ti] = tf_w * idx.idf[ti]

    qn = float(np.linalg.norm(q))
    if qn == 0.0:
        return []

    dots = idx.matrix @ q
    sims = dots / (idx.norms * qn + 1e-8)
    top_idx = np.argsort(-sims)[: int(k)]

    out: list[dict[str, Any]] = []
    for i in top_idx.tolist():
        if sims[i] <= 0:
            continue
        d = dict(idx.docs[i])
        d["similarity"] = float(sims[i])
        out.append(d)
    return out


def get_explanation(payload: Any) -> str:
    """
    Backward-compatible wrapper.

    - If given a string (old behavior), we retrieve context and explain.
    - If given a dict, we expect keys like `student` and `top_college`.
    """
    if isinstance(payload, str):
        query = payload
        ctx = retrieve_context(query, k=5)
        if not ctx:
            return "I couldn't find relevant context in the college database for that query."
        bullets = "\n".join(
            f"- {c['Institute_Name']} ({c.get('District','')}) — {c.get('Branch_Name','')}, fee: {c.get('Fee','')}"
            for c in ctx[:5]
        )
        return (
            "Based on the college database, the most relevant entries are:\n"
            f"{bullets}\n\n"
            "Your top recommendation fits because it matches your branch/location/fee constraints and has a cutoff rank compatible with your rank."
        )

    if isinstance(payload, dict):
        student = payload.get("student", {}) or {}
        top = payload.get("top_college", {}) or {}
        query = (
            f"{top.get('Institute_Name','')} {top.get('District','')} {top.get('Branch_Name','')} "
            f"rank {student.get('rank','')} category {student.get('category','')} gender {student.get('gender','')} "
            f"budget {student.get('budget','')}"
        )
        ctx = retrieve_context(query, k=5)
        reasons = []
        if top.get("Branch_Name"):
            reasons.append(f"Matches your branch preference (**{top.get('Branch_Name')}**).")
        if student.get("district") and top.get("District"):
            reasons.append(f"Matches your location filter (**{top.get('District')}**).")
        if top.get("Fee") is not None and student.get("budget"):
            reasons.append(f"Fits your fee budget (fee **{top.get('Fee')}**, budget **{student.get('budget')}**).")
        if top.get("Cutoff_Rank") is not None and student.get("rank"):
            reasons.append(
                f"Your rank (**{student.get('rank')}**) is within the cutoff (**{top.get('Cutoff_Rank')}**) for {student.get('category')} ({student.get('gender')})."
            )

        ctx_hint = ""
        if ctx:
            ctx_hint = "Similar colleges in the database include: " + ", ".join(
                f"{c['Institute_Name']} ({c.get('District','')})" for c in ctx[:3]
            ) + "."

        if not reasons:
            reasons.append("It ranks highly after applying your filters and scoring.")

        return "Why this college is recommended:\n- " + "\n- ".join(reasons) + (f"\n\n{ctx_hint}" if ctx_hint else "")

    return "Unsupported explanation request."