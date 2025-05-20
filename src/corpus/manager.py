# src/corpus/manager.py

from pathlib import Path
import json, glob
from typing import List

class CorpusManager:
    """
    Build or load an ordered JSON corpus of passages.
    """
    def __init__(self, corpus_dir: str, out_fp: str):
        self.corpus_dir  = Path(corpus_dir)
        self.ordered_json = Path(out_fp)

    def build(self) -> List[str]:
        """Scan all .json in corpus_dir, flatten & save to ordered_json."""
        files = sorted(glob.glob(str(self.corpus_dir / "*.json")))
        corpus: List[str] = []
        for fp in files:
            for txt in json.load(open(fp, encoding="utf-8")):
                t = txt.strip()
                if t:
                    corpus.append(t)
        self.ordered_json.parent.mkdir(parents=True, exist_ok=True)
        json.dump(corpus,
                  open(self.ordered_json, "w", encoding="utf-8"),
                  ensure_ascii=False)
        print(f"built corpus {self.ordered_json} ({len(corpus):,d})")
        return corpus

    def load(self) -> List[str]:
        """Load ordered JSON corpus."""
        return json.load(open(self.ordered_json, encoding="utf-8"))
