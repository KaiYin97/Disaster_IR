# src/utils/io.py

import json
import glob
import os
from pathlib import Path
from typing import Any, List, Tuple


def load_json(path: str, default: Any = None) -> Any:
    """
    Load a JSON file from `path`. Return `default` if file does not exist or on error.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def dump_json(path: str, obj: Any, indent: int = 2) -> None:
    """
    Write `obj` as JSON to `path`, creating parent directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)


def build_ordered_corpus(corpus_dir: str, out_fp: str) -> List[str]:
    """
    Read all .json files under `corpus_dir`, flatten their lists of strings,
    filter out empty lines, and write the ordered list to `out_fp`.
    Returns the list of passages.
    """
    files = sorted(glob.glob(os.path.join(corpus_dir, "*.json")))
    corpus: List[str] = []
    for fp in files:
        try:
            arr = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        for txt in arr:
            line = txt.strip()
            if line:
                corpus.append(line)

    # ensure output directory exists, then write
    Path(out_fp).parent.mkdir(parents=True, exist_ok=True)
    with open(out_fp, "w", encoding="utf-8") as wf:
        json.dump(corpus, wf, ensure_ascii=False, indent=2)
    print(f"Built ordered corpus at {out_fp} with {len(corpus)} passages.")

    return corpus


def load_ordered_corpus(corpus_json: str) -> List[str]:
    """
    Load and return the ordered corpus list from `corpus_json`.
    """
    return json.load(open(corpus_json, encoding="utf-8"))


def load_test_file(path: str) -> Tuple[List[dict], List[str]]:
    """
    Load a test query JSON file:
    - Returns a tuple (full_data, list_of_queries),
      where list_of_queries is extracted from the "user_query" field.
    """
    data = json.load(open(path, encoding="utf-8"))
    queries = [item.get("user_query", "").strip() for item in data]
    return data, queries
