#!/usr/bin/env python3
# scripts/relevance_scoring.py

import sys
from pathlib import Path

# ensure project root on PYTHONPATH so that `src` and `configs` are importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.scoring.scorer import main

if __name__ == "__main__":
    main()
 