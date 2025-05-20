import re
import fitz
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from configs.path_config import RAW_PDF_ROOT, TXT_ROOT
from configs.gen_config    import TABLES_EXTRACT

_LINE_RE     = re.compile(r"\s{2,}")
_NUMERIC_RE  = re.compile(r"^\[\d.]+\$")

class PDFProcessor:
    def __init__(
        self,
        table_extract: bool = TABLES_EXTRACT,
        txt_root:      Path = TXT_ROOT
    ):
        self.table_extract = table_extract
        self.txt_root       = Path(txt_root)

    def run(self, pdf_root: Path = RAW_PDF_ROOT):
        """
        Iterate over all subfolders in pdf_root,
        extract text (and tables if enabled), write out .txt/.csv files.
        """
        pdf_root = Path(pdf_root)
        for sub in tqdm(sorted(pdf_root.iterdir()), desc="PDF → TXT"):
            if not sub.is_dir():
                continue
            out_dir = self.txt_root / f"{sub.name}_txt"
            out_dir.mkdir(parents=True, exist_ok=True)
            for pdf_file in sorted(sub.glob("*.pdf")):
                self._process_single(pdf_file, out_dir)

    def _process_single(self, pdf_path: Path, out_dir: Path):
        txt_path = out_dir / f"{pdf_path.stem}.txt"
        csv_path = out_dir / f"{pdf_path.stem}.csv"

        text = self._extract_pdf_content(pdf_path, csv_path)
        txt_path.write_text(text, encoding="utf-8")

    def _extract_pdf_content(self, pdf_path: Path, csv_path: Path) -> str:
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Failed to open PDF: {e}")
            return ""

        full_text = ""
        colnames0 = None
        rows      = []

        for page in doc:
            blocks = page.get_text("blocks")
            tables = page.find_tables() if self.table_extract else []

            for b in blocks:
                bbox, txt = b[:4], b[4]
                # skip headers/footers and page numbers
                if bbox[1] > page.rect.height * 0.9 or bbox[3] < page.rect.height * 0.1:
                    if txt.strip().isdigit():
                        continue
                # avoid text overlapping table areas
                if any(fitz.Rect(bbox).intersects(t.bbox) for t in tables):
                    continue
                full_text += txt + "\n"

            if self.table_extract:
                for tb in tables:
                    hdr   = tb.header
                    names = hdr.names
                    if colnames0 is None:
                        colnames0 = names
                    elif names != colnames0:
                        self._save_table(rows, colnames0, csv_path)
                        rows, colnames0 = [], names
                    extract = tb.extract()
                    if not hdr.external:
                        extract = extract[1:]  # drop duplicate header row
                    rows.extend(extract)

        if rows:
            self._save_table(rows, colnames0, csv_path)
        doc.close()
        return full_text

    @staticmethod
    def _save_table(rows: list, cols: list, path: Path):
        """
        Save a list of rows (and column names) to a CSV file.
        """
        df = pd.DataFrame(rows, columns=cols)
        df.to_csv(path.with_suffix(".csv"), index=False)


class Cleaner:
    """
    Post-processing for extracted .txt files:
     - Remove reference sections
     - Filter out very short or garbled lines
     - Drop empty files
    """
    def __init__(self, txt_root: Path = TXT_ROOT):
        self.txt_root = Path(txt_root)

    def run(self):
        for sub in tqdm(sorted(self.txt_root.iterdir()), desc="Cleaning TXT"):
            if not sub.is_dir():
                continue
            for txt_file in sorted(sub.glob("*.txt")):
                raw = txt_file.read_text(encoding="utf-8")
                cleaned = self._clean(raw)
                if cleaned.strip():
                    txt_file.write_text(cleaned, encoding="utf-8")
                else:
                    # remove entirely if nothing remains
                    txt_file.unlink()

    def _clean(self, text: str) -> str:
        in_refs = False
        out_lines = []
        for ln in text.splitlines():
            s = ln.strip()
            # detect start of references section
            if s.lower() in {"reference", "references"}:
                in_refs = True
                continue
            if in_refs:
                continue

            # word/count heuristics
            wc = len(s.split())
            mwl = sum(len(w) for w in s.split()) / wc if wc else 0

            # drop lines with common garble or punctuation artifacts
            if any(tok in ln for tok in ("....", "���", ". . .", "\x07", "…")):
                continue
            if _NUMERIC_RE.match(s):
                continue
            if wc < 2 or mwl < 4:
                continue
            if _LINE_RE.search(ln):
                continue

            out_lines.append(ln)

        return "\n".join(out_lines)
