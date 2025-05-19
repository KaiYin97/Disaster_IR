# src/scoring/scorer.py

import os
import json
import glob
import math
import time
import argparse
from pathlib import Path
from collections import Counter
from typing import Any, Optional, List, Tuple, Dict

from openai import OpenAIError
from openai import OpenAI as OpenAIClient

from configs.path_config import LABEL_POOL_DIR, OUTPUT_QRELS_DIR
from configs.gen_config import (
    MODEL_NAME,
    MAX_RETRIES,
    RETRY_DELAY,
    DEFAULT_TEMPERATURE,
    ITEMS_PER_PART,
    SAVE_INTERVAL,
    TASK2PREFIX,
)

from query.client import client  # already configured OpenAI client
from scoring.raters.base import BaseRater
from scoring.raters.phase4_rater  import Phase4Rater
from scoring.raters.cot_rater     import ChainOfThoughtRater
from scoring.raters.zeroshot_rater import ZeroShotRater


def load_json(path: str, default: Any):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def dump_json(path: str, data: Any):
    """
    Write JSON to `path`, creating parent directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_final_scores(s1: Optional[int], s2: Optional[Any], s3: Any) -> Tuple[Any, Optional[float]]:
    """
    Combine three method scores into (majority_vote, average_score).
    """
    vals = [v for v in (s1, s2, s3) if isinstance(v, (int, float))]
    if not vals:
        return None, None
    avg = round(sum(vals) / len(vals), 2)
    if len(vals) == 1:
        return vals[0], avg
    cnt = Counter(vals)
    mode, freq = cnt.most_common(1)[0]
    # if unique mode
    if list(cnt.values()).count(freq) == 1:
        return mode, avg
    # else tie → use average
    return avg, avg


def process_part(
    client: OpenAIClient,
    input_file: str,
    output_file: str,
    part_idx: int,
    task: str,
    force_default: bool
):
    data = load_json(input_file, [])
    if not isinstance(data, list):
        print(f"ERROR: {input_file} is not a list")
        return

    start = part_idx * ITEMS_PER_PART
    end = (part_idx + 1) * ITEMS_PER_PART
    items = data[start:end]

    # initialize existing results
    results = load_json(output_file, [])
    done_pairs = {(r.get("original_query"), r.get("passage")) for r in results}

    # collect all (query, passage) to rate
    to_rate: List[Tuple[str, str]] = []
    for item in items:
        q = item.get("user_query")
        pool = item.get("label_pool", [])
        if not q or not isinstance(pool, list):
            continue
        for p in pool:
            if (q, p) not in done_pairs:
                to_rate.append((q, p))

    total = len(to_rate)
    print(f"{task}-Part{part_idx}: {total} pairs to process")

    # initialize raters
    rater1 = Phase4Rater()
    rater2 = ChainOfThoughtRater()
    rater3 = ZeroShotRater()

    new_count = 0
    from tqdm import tqdm
    for q, psg in tqdm(to_rate, desc=f"Rating {task}"):
        try:
            prefix = TASK2PREFIX.get(task, "")
            mq = (f"{prefix} {q}" if prefix else q).strip()
            mp = psg.strip()

            if task == "STS":
                # only zero-shot for STS
                score = rater3.rate(client, "STS", mq, mp, force_default)
                results.append({
                    "original_query": mq,
                    "passage":        mp,
                    "score_average":  score,
                })
            else:
                s1, sub1 = rater1.rate(client, task, mq, mp, force_default)
                s2, _flag2, sub2 = rater2.rate(client, task, mq, mp, force_default)
                s3 = rater3.rate(client, task, mq, mp, force_default)

                maj, avg = calculate_final_scores(s1, s2, s3)
                results.append({
                    "original_query":      q,
                    "passage":             psg,
                    "score_phase4":        s1,
                    "score_cot":           s2,
                    "score_zero_shot":     s3,
                    "score_majority_vote": maj,
                    "score_average":       avg,
                })

            new_count += 1
            done_pairs.add((q, psg))
            # checkpoint save
            if new_count % SAVE_INTERVAL == 0:
                dump_json(output_file, results)

        except Exception as e:
            print(f"[ERR {task}] ({q[:30]} / {psg[:30]}): {e}")

    # final save
    dump_json(output_file, results)
    print(f"Appended {new_count} new results to {output_file}")


def main():
    tasks = list(TASK2PREFIX.keys()) + ["STS"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--task",        required=True, choices=tasks)
    parser.add_argument("--file_index",  type=int, required=True)
    parser.add_argument("--part_index",  type=int, required=True)
    parser.add_argument(
        "--input_dir",  default=str(LABEL_POOL_DIR),
        help="Directory of label_pool JSON files"
    )
    parser.add_argument(
        "--output_dir", default=str(OUTPUT_QRELS_DIR),
        help="Directory to write scored qrels"
    )
    parser.add_argument(
        "--force_default_prompts",
        action="store_true",
        help="Use default prompts for FactCheck/NLI"
    )
    args = parser.parse_args()

    pattern = os.path.join(args.input_dir, f"{args.task}_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f"No files for {args.task} in {args.input_dir}")
    if not (0 <= args.file_index < len(files)):
        raise SystemExit("file_index out of range")

    input_file  = files[args.file_index]
    total_items = len(load_json(input_file, []))
    parts = max(1, math.ceil(total_items / ITEMS_PER_PART))
    if not (0 <= args.part_index < parts):
        raise SystemExit("part_index out of range")

    stem = Path(input_file).stem
    out_name = f"{stem}_f{args.file_index}_p{args.part_index}_qrels.json"
    output_file = os.path.join(args.output_dir, out_name)

    # run rating
    process_part(
        client,
        input_file,
        output_file,
        args.part_index,
        args.task,
        args.force_default_prompts,
    )


if __name__ == "__main__":
    main()
