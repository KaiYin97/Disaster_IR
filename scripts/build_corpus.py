#!/usr/bin/env python3
# scripts/build_corpus.py

import argparse
from pathlib import Path

# make sure 'src' is on PYTHONPATH so we can import our modules
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.corpus.downloader import PDFDownloader
from src.corpus.processor  import PDFProcessor, Cleaner
from src.corpus.deduper    import MinHashDeduper, EmbeddingDeduper
from src.corpus.chunker    import Chunker


def main(keywords_json: Path):
    """
    Complete corpus construction pipeline:
    1. Download PDFs by keywords
    2. Extract text (and tables if enabled)
    3. Clean extracted text
    4. MinHash-based deduplication
    5. Semantic chunking
    6. Embedding-based deduplication
    """
    # 1. Download PDFs
    PDFDownloader().run(keywords_json)

    # 2. Extract text from PDFs
    PDFProcessor().run()

    # 3. Clean up raw text files
    Cleaner().run()

    # 4. Remove near-duplicate chunks via MinHash
    MinHashDeduper().run()

    # 5. Split cleaned, deduped text into semantic chunks
    Chunker().run()

    # 6. Remove embedding-level duplicates among chunks
    EmbeddingDeduper().run()

    print("✓ Corpus build completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the end-to-end corpus construction pipeline."
    )
    parser.add_argument(
        "--keywords_json",
        type=Path,
        required=True,
        help="This json is in Disaster_IR/configs/disaster_type.json"
    )
    args = parser.parse_args()
    main(args.keywords_json)
