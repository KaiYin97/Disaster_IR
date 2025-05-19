# src/corpus/deduper.py

import json
import pickle
import random
import shutil
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

from transformers import GPT2TokenizerFast
from datasketch import MinHash, MinHashLSH
from unisim import TextSim

from configs.path_config import (
    CHUNK_JSON_ROOT,
    EMBED_DEDUP_ROOT,
    SEARCH_CACHE_DIR,
    TXT_ROOT,
    DEDUP_TXT_ROOT,
    DUP_TXT_ROOT,
)
from configs.gen_config import MINHASH_THRESHOLD, MINHASH_PERM, MAX_ITEMS_PER_JSON


def _copy_file(src: Path, dst_root: Path) -> None:
    """
    Copy src file under dst_root, preserving folder structure.
    """
    rel = src.relative_to(src.parents[2])
    target = dst_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)


class EmbeddingDeduper:
    def __init__(
        self,
        chunk_root: Path = CHUNK_JSON_ROOT,
        out_root:   Path = EMBED_DEDUP_ROOT,
        cache_dir:  Path = SEARCH_CACHE_DIR
    ):
        self.chunk_root = Path(chunk_root)
        self.out_root   = Path(out_root)
        self.cache      = Path(cache_dir)
        self.out_root.mkdir(parents=True, exist_ok=True)
        self.cache.mkdir(parents=True, exist_ok=True)

    def run(self):
        """
        Run embedding-based deduplication: cluster chunks and keep one per cluster.
        """
        contents, items = self._load_items()
        keep = self._dedupe_indices(contents)
        self._write_unique(items, keep)

    def _load_items(self):
        contents, items = [], []
        for jf in self.chunk_root.glob("*.json"):
            data = json.loads(jf.read_text(encoding="utf-8"))
            contents.extend([d["page_content"] for d in data])
            items.extend(data)
        return contents, items

    def _dedupe_indices(self, contents):
        """
        Build approximate index with TextSim and union similar items.
        """
        ts = TextSim(store_data=True, index_type="approx",
                     batch_size=256, use_accelerator=True)

        # index in batches
        step = MAX_ITEMS_PER_JSON
        for i in tqdm(range(0, len(contents), step), desc="Indexing"):
            ts.add(contents[i:i+step])

        # union-find for cluster merging
        parent = list(range(len(contents)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        # search similar items and union by threshold
        for i in tqdm(range(0, len(contents), step), desc="Searching"):
            cache_f = self.cache / f"batch_{i//step:04d}.pkl"
            if cache_f.exists():
                res = pickle.loads(cache_f.read_bytes())
            else:
                res = ts.search(
                    contents[i:i+step],
                    similarity_threshold=MINHASH_THRESHOLD,
                    k=10,
                    drop_closest_match=False
                )
                cache_f.write_bytes(pickle.dumps(res))

            for qi, r in enumerate(res.results):
                src = i + qi
                for m in r.matches:
                    if m.idx != src and m.similarity >= MINHASH_THRESHOLD:
                        union(src, m.idx)

        # pick one representative per cluster
        clusters = defaultdict(list)
        for idx in range(len(contents)):
            clusters[find(idx)].append(idx)
        random.seed(42)
        return {random.choice(v) for v in clusters.values()}

    def _write_unique(self, items, keep):
        """
        Write only unique items (by index in keep) into JSON files.
        """
        kept = [items[i] for i in sorted(keep)]
        step = MAX_ITEMS_PER_JSON
        for i in range(0, len(kept), step):
            out = self.out_root / f"deduped_{i//step:03d}.json"
            out.write_text(
                json.dumps(kept[i:i+step], ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        print(f"kept {len(kept)} unique chunks")


class MinHashDeduper:
    def __init__(
        self,
        src_root    = TXT_ROOT,
        dst_unique  = DEDUP_TXT_ROOT,
        dst_dup     = DUP_TXT_ROOT
    ):
        self.src_root = Path(src_root)
        self.dst_u    = Path(dst_unique)
        self.dst_d    = Path(dst_dup)
        for p in (self.dst_u, self.dst_d):
            p.mkdir(parents=True, exist_ok=True)
        self.tok = GPT2TokenizerFast.from_pretrained("gpt2")

    def run(self):
        """
        Run MinHash-based deduplication: unique files → dst_unique, duplicates → dst_dup.
        """
        files = list(self.src_root.rglob("*.txt"))
        random.shuffle(files)

        lsh = MinHashLSH(threshold=MINHASH_THRESHOLD, num_perm=MINHASH_PERM)
        next_idx = 0

        for fp in tqdm(files, desc="MinHash dedup"):
            txt = fp.read_text(encoding="utf-8")
            mh = self._text2_minhash(txt)

            if lsh.query(mh):
                _copy_file(fp, self.dst_d)
            else:
                lsh.insert(str(next_idx), mh)
                next_idx += 1
                _copy_file(fp, self.dst_u)

    def _text2_minhash(self, txt: str) -> MinHash:
        """
        Convert text to a MinHash sketch of n-grams of token IDs.
        """
        mh = MinHash(num_perm=MINHASH_PERM)
        ids = self.tok.encode(txt, add_special_tokens=False)
        n = 3
        for i in range(len(ids) - n + 1):
            gram = tuple(ids[i:i+n])
            mh.update(str(gram).encode())
        return mh
