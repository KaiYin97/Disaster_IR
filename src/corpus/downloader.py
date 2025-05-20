# src/corpus/downloader.py

import json
import time
from pathlib import Path

import requests
from googlesearch import search
from tqdm import tqdm

from configs.path_config import RAW_PDF_ROOT, SEARCH_CACHE_DIR
from configs.gen_config import MAX_PDFS_PER_KEYWORD, GOOGLE_PAUSE_SEC, HTTP_429_SLEEP_MIN


class PDFDownloader:
    def __init__(self, save_root: Path = RAW_PDF_ROOT):
        self.save_root = Path(save_root)
        self.save_root.mkdir(parents=True, exist_ok=True)
        # Path-to-URL mapping for downloaded PDFs
        self.result_json = self.save_root.parent / "download_pdf_url.json"
        self._url_map = self._load_url_map()

    def run(self, keywords_json: Path):
        """
        Download PDFs based on a list of keywords.
        """
        with open(keywords_json, "r", encoding="utf-8") as f:
            keywords = json.load(f)

        for kw in tqdm(keywords, desc="Downloading PDFs"):
            safe_kw = self._sanitize_folder_name(kw)
            kw_dir = self.save_root / safe_kw
            kw_dir.mkdir(exist_ok=True)

            query = f"{kw} hazard pdf filetype:pdf"
            urls = self._safe_search(query)

            pdf_count = 0
            for url in urls:
                if not url.lower().endswith(".pdf"):
                    continue

                save_path = kw_dir / f"file_{pdf_count+1}.pdf"
                if self._download(url, save_path):
                    pdf_count += 1
                    self._url_map[str(save_path)] = url
                    self._save_url_map()
                if pdf_count >= MAX_PDFS_PER_KEYWORD:
                    break

            # Wait to avoid Google blocking after each keyword
            time.sleep(GOOGLE_PAUSE_SEC)

    @staticmethod
    def _safe_search(query: str, retries: int = 3) -> list[str]:
        """
        Wrapper for Google search with HTTP 429 retry handling.
        """
        for attempt in range(retries):
            try:
                return list(search(query, num=10, stop=40, pause=GOOGLE_PAUSE_SEC))
            except Exception as e:
                if "429" in str(e):
                    print(f"HTTP 429 – sleeping {HTTP_429_SLEEP_MIN} minutes before retrying...")
                    time.sleep(HTTP_429_SLEEP_MIN * 60)
                else:
                    print(f"Search error: {e}")
                    return []
        return []

    @staticmethod
    def _download(url: str, path: Path) -> bool:
        """
        Download a single PDF from URL to disk.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=10)
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Download failed for {url!r}: {e}")
            return False

    def _load_url_map(self) -> dict:
        """
        Load existing URL mapping if it exists.
        """
        if self.result_json.exists():
            with open(self.result_json, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_url_map(self) -> None:
        """
        Save updated URL mapping to disk.
        """
        with open(self.result_json, "w", encoding="utf-8") as f:
            json.dump(self._url_map, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _sanitize_folder_name(name: str) -> str:
        """
        Make folder name filesystem-safe.
        """
        return "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in name).strip()
