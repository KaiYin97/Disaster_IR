# src/query/pipeline.py

import json
import argparse
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

from src.query.client     import tokenizer, safe_generate
from src.query.generators import TwitterGenerator, QAGenerator, STSGenerator, FactCheckGenerator, NLIGenerator
from configs.path_config import INPUT_DIR, OUTPUT_DIR, DOC_INPUT_DIR, DOC_OUTPUT_DIR
from configs.gen_config import MIN_TOKENS, CHECKPOINT_SIZE, DOC_ITEMS_PER_FILE, PROMPTS_FILE

PROMPTS = json.load(open(PROMPTS_FILE, "r", encoding="utf-8"))

GENS = {
    "tw":  TwitterGenerator(),
    "qa":  QAGenerator(),
    "sts": STSGenerator(),
    "fc":  FactCheckGenerator(),
    "nli": NLIGenerator(),
}


def dump_json(path: Path, obj): 
    """
    Ensure parent dir exists and write object as pretty-printed JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def run_passage_tasks(filename: str, tasks: list[str], start: int | None, end: int | None):
    path = Path(INPUT_DIR) / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data = data[start:end] if (start is not None or end is not None) else data

    out_root = Path(OUTPUT_DIR)
    batch_num = 1
    batch_cnt = 0
    batch = []
    cur_out = out_root / f"{path.stem}_batch_{batch_num:03d}.json"
    dump_json(cur_out, [])

    errs = defaultdict(list)
    for item in tqdm(data, desc=f"Passage-level ({','.join(tasks)})"):
        content = item.get("page_content", "")
        if len(tokenizer.encode(content)) < MIN_TOKENS:
            continue

        idx = item.get("id", batch_cnt + 1)
        rec = {k: item.get(k) for k in ("page_content", "specific_type", "general_type", "source")}

        for t in tasks:
            GENS[t].apply(content, rec, str(idx), errs)

        batch.append(rec)
        batch_cnt += 1
        dump_json(cur_out, batch)

        if batch_cnt >= CHECKPOINT_SIZE:
            batch_num += 1
            batch_cnt = 0
            batch = []
            cur_out = out_root / f"{path.stem}_batch_{batch_num:03d}.json"
            dump_json(cur_out, [])

    for t, lst in errs.items():
        if lst:
            dump_json(Path(OUTPUT_DIR) / f"errors_{t}.json", lst)

    print(f"Passage tasks done → {batch_num} file(s)")


def run_document_qa(start: int | None, end: int | None):
    abstract_files = sorted(Path(DOC_INPUT_DIR).glob("*.json"))
    abstract_files = abstract_files[start:end] if (start is not None or end is not None) else abstract_files

    batch = []
    file_idx = 1
    out_path = Path(DOC_OUTPUT_DIR) / f"doc_batch_{file_idx:03d}.json"
    dump_json(out_path, [])

    print(f"Document-QA: {len(abstract_files)} abstracts to process")
    for fp in tqdm(abstract_files, desc="Doc-QA"):
        info = json.loads(fp.read_text(encoding="utf-8"))
        abstract = info.get("abstract", "")
        if not abstract:
            continue

        # Phase 1: decide which document-level tasks apply
        tasks = safe_generate(
            PROMPTS["doc_task"],                     
            "Paragraph: " + json.dumps(abstract)
        )
        if not isinstance(tasks, list):
            continue

        for task in tasks:
            # Phase 2: generate a user_query for each task
            prompt = PROMPTS["doc_query"].format(task=task)
            res = safe_generate(
                prompt,
                "Paragraph: " + json.dumps(abstract)
            )
            if res and "user_query" in res:
                batch.append({
                    "user_query":       res["user_query"],
                    "positive_document": abstract,
                    "doc_title":        info.get("title", ""),
                    "source":           info.get("source", ""),
                })

            if len(batch) >= DOC_ITEMS_PER_FILE:
                dump_json(out_path, batch)
                file_idx += 1
                batch = []
                out_path = Path(DOC_OUTPUT_DIR) / f"doc_batch_{file_idx:03d}.json"
                dump_json(out_path, [])

    if batch:
        dump_json(out_path, batch)

    print(f"Document-QA done → {file_idx} file(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="chunk JSON filename under INPUT_DIR")
    parser.add_argument(
        "--tasks", nargs="+", required=True,
        choices=["all", "doc", "tw", "qa", "sts", "fc", "nli"],
        help="Which tasks to run; 'all' expands to all"
    )
    parser.add_argument("--start_index", type=int, default=None)
    parser.add_argument("--end_index",   type=int, default=None)
    args = parser.parse_args()

    tasks = ["doc", "tw", "qa", "sts", "fc", "nli"] if "all" in args.tasks else args.tasks
    passage = [t for t in tasks if t in GENS]
    if passage:
        if not args.filename:
            raise SystemExit("ERROR: --filename is required for passage-level tasks.")
        run_passage_tasks(args.filename, passage, args.start_index, args.end_index)
    if "doc" in tasks:
        run_document_qa(args.start_index, args.end_index)
