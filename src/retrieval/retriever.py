# src/retrieval/retriever.py

from typing import Dict, List
import numpy as np
import torch
from usearch.index import Index

from configs.model_config import DEFAULT_TOPK, DEVICE


class Retriever:
    def __init__(
        self,
        corpus: List[str],
        corpus_emb: np.ndarray,
        ann_idxs: Dict[str, Index],
        top_k: int = DEFAULT_TOPK,
        device: str = DEVICE,
    ):
        """
        Wrap exact (dot-product) and ANN retrieval over a text corpus.

        Args:
            corpus:         list of passages (strings)
            corpus_emb:     numpy array of shape (N, D) with normalized embeddings
            ann_idxs:       dict mapping model name → Usearch Index
            top_k:          number of results to return
            device:         torch device (e.g., 'cpu' or 'cuda')
        """
        self.corpus = corpus
        self.top_k = top_k
        self.device = device

        self.corpus_T = torch.tensor(corpus_emb, dtype=torch.float32, device=device)
        self.ann_idxs = ann_idxs

    def _exact(self, q_emb: np.ndarray) -> List[List[str]]:
        """
        Compute exact retrieval by dot-product similarity.

        Args:
            q_emb: numpy array (B, D) of query embeddings

        Returns:
            List of top_k passages for each query.
        """
        qT = torch.tensor(q_emb, dtype=torch.float32, device=self.device)
        with torch.no_grad():
            sim = qT @ self.corpus_T.T
            _, idxs = sim.topk(self.top_k, dim=1)
        
        return [[self.corpus[i] for i in row] for row in idxs.cpu().numpy()]

    def _ann(self, model: str, q_emb: np.ndarray) -> List[List[str]]:
        """
        Perform approximate nearest neighbor search using Usearch.

        Args:
            model: model name key into self.ann_idxs
            q_emb: numpy array (B, D) of query embeddings

        Returns:
            List of top_k passages per query via ANN index.
        """
        hits = self.ann_idxs[model].search(q_emb, self.top_k, threads=1)
        return [[self.corpus[int(h.key)] for h in row] for row in hits]

    def retrieve(self, model: str, q_emb: np.ndarray) -> Dict[str, List[List[str]]]:
        """
        Return both exact and ANN retrieval results.

        Args:
            model: model name for ANN search
            q_emb: numpy array of query embeddings

        Returns:
            {
              "exact": [[passage, ...], ...],
              "ann":   [[passage, ...], ...]
            }
        """
        return {
            "exact": self._exact(q_emb),
            "ann":   self._ann(model, q_emb),
        }
