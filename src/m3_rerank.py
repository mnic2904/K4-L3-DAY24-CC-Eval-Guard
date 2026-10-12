from __future__ import annotations

"""Module 3: Reranking — Cross-encoder top-20 → top-3 + latency benchmark."""

import os
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RERANK_TOP_K


@dataclass
class RerankResult:
    text: str
    original_score: float
    rerank_score: float
    metadata: dict
    rank: int


class CrossEncoderReranker:
    """Pipeline-compatible reranker backed by lightweight FlashRank."""

    def __init__(self, model_name: str = "ms-marco-TinyBERT-L-2-v2"):
        from flashrank import Ranker
        self.model_name = model_name
        self._model = Ranker(model_name=model_name,
                             cache_dir=os.path.join(tempfile.gettempdir(), "flashrank"))

    def rerank(self, query: str, documents: list[dict], top_k: int = RERANK_TOP_K) -> list[RerankResult]:
        """Rerank documents: top-20 → top-k."""
        if not documents or top_k <= 0:
            return []

        from flashrank import RerankRequest
        passages = [{"id": index, "text": document["text"]}
                    for index, document in enumerate(documents)]
        ranked = self._model.rerank(RerankRequest(query=query, passages=passages))
        return [RerankResult(
            text=row["text"], original_score=float(documents[row["id"]].get("score", 0.0)),
            rerank_score=float(row["score"]), metadata=documents[row["id"]].get("metadata", {}),
            rank=rank,
        ) for rank, row in enumerate(ranked[:top_k])]


class FlashrankReranker:
    """Lightweight alternative (<5ms). Optional."""
    def __init__(self, model_name: str = "ms-marco-TinyBERT-L-2-v2"):
        from flashrank import Ranker
        self._model = Ranker(model_name=model_name,
                             cache_dir=os.path.join(tempfile.gettempdir(), "flashrank"))

    def rerank(self, query: str, documents: list[dict], top_k: int = RERANK_TOP_K) -> list[RerankResult]:
        if not documents or top_k <= 0:
            return []
        from flashrank import RerankRequest
        passages = [{"id": index, "text": document["text"]}
                    for index, document in enumerate(documents)]
        ranked = self._model.rerank(RerankRequest(query=query, passages=passages))
        return [RerankResult(
            text=row["text"], original_score=float(documents[row["id"]].get("score", 0.0)),
            rerank_score=float(row["score"]), metadata=documents[row["id"]].get("metadata", {}),
            rank=rank,
        ) for rank, row in enumerate(ranked[:top_k])]


def benchmark_reranker(reranker, query: str, documents: list[dict], n_runs: int = 5) -> dict:
    """Benchmark latency over n_runs. (Đã implement sẵn)"""
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        reranker.rerank(query, documents)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    return {"avg_ms": sum(times) / len(times), "min_ms": min(times), "max_ms": max(times)}


if __name__ == "__main__":
    query = "Nhân viên được nghỉ phép bao nhiêu ngày?"
    docs = [
        {"text": "Nhân viên được nghỉ 12 ngày/năm.", "score": 0.8, "metadata": {}},
        {"text": "Mật khẩu thay đổi mỗi 90 ngày.", "score": 0.7, "metadata": {}},
        {"text": "Thời gian thử việc là 60 ngày.", "score": 0.75, "metadata": {}},
    ]
    reranker = CrossEncoderReranker()
    for r in reranker.rerank(query, docs):
        print(f"[{r.rank}] {r.rerank_score:.4f} | {r.text}")
