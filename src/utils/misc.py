# src/utils/misc.py

import re
import time
import random
from typing import Optional


def sanitize_folder_name(name: str) -> str:
    safe = re.sub(r'[^A-Za-z0-9 _-]', '_', name)
    safe = re.sub(r'[_\s]+', '_', safe).strip('_')
    return safe


def wait_random(min_sec: float = 1.0, max_sec: Optional[float] = None) -> None:
    """
    Sleep for a random duration between min_sec and max_sec.
    If max_sec is None, sleep exactly min_sec.
    """
    if max_sec is None or max_sec <= min_sec:
        time.sleep(min_sec)
    else:
        time.sleep(random.uniform(min_sec, max_sec))


def normalise(text: str) -> str:
    """
    Normalize text for deduplication:
    - Lowercase
    - Remove non-alphanumeric characters (keep spaces)
    - Collapse whitespace
    """
    s = text.lower()
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s
