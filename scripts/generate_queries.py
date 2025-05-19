#!/usr/bin/env python3
# scripts/generate_queries.py

import argparse
import sys
from pathlib import Path

# ensure src on PYTHONPATH for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.query.pipeline import run_passage_tasks, run_document_qa

def main():
    parser = argparse.ArgumentParser(
        description="Generate user queries for passage‐ and document‐level tasks"
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        required=True,
        choices=["all", "doc", "tw", "qa", "sts", "fc", "nli"],
        help="Tasks to run; 'all' expands to all six passage‐level plus doc"
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Input chunk JSON filename under INPUT_DIR (required for passage tasks)"
    )
    parser.add_argument(
        "--start_index",
        type=int,
        default=None,
        help="Optional start index (inclusive) to slice the input list"
    )
    parser.add_argument(
        "--end_index",
        type=int,
        default=None,
        help="Optional end index (exclusive) to slice the input list"
    )
    args = parser.parse_args()

    # Determine which tasks to run
    tasks = ["doc", "tw", "qa", "sts", "fc", "nli"] if "all" in args.tasks else args.tasks
    passage_tasks = [t for t in tasks if t in {"tw", "qa", "sts", "fc", "nli"}]

    # Run passage‐level generators if requested
    if passage_tasks:
        if not args.filename:
            parser.error("`--filename` is required when running passage‐level tasks")
        run_passage_tasks(
            filename=args.filename,
            tasks=passage_tasks,
            start=args.start_index,
            end=args.end_index
        )

    # Run document‐level QA if requested
    if "doc" in tasks:
        run_document_qa(
            start=args.start_index,
            end=args.end_index
        )

if __name__ == "__main__":
    main()
