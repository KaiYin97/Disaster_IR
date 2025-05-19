# src/corpus/chunker.py

from pathlib import Path
from tqdm import tqdm

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

from configs.path_config import DEDUP_TXT_ROOT, CHUNK_JSON_ROOT
from configs.gen_config import PDF_MAX_CHUNK_TOKENS, FIRST_CHUNK_ID, MAX_ITEMS_PER_JSON


class Chunker:
    def __init__(
        self,
        txt_root: Path = DEDUP_TXT_ROOT,
        out_root: Path = CHUNK_JSON_ROOT,
    ):
        """
        Initialize the semantic chunker with OpenAI embeddings.
        """
        self.txt_root = Path(txt_root)
        self.out_root = Path(out_root)
        self.out_root.mkdir(parents=True, exist_ok=True)

        # create a LangChain-based chunker for splitting by semantic coherence
        self.splitter = SemanticChunker(
            OpenAIEmbeddings(),
            add_start_index=True,
            breakpoint_threshold_amount=95,
            max_chunk_tokens=PDF_MAX_CHUNK_TOKENS,
            min_chunk_tokens=32,
        )

        # counters for assigning unique IDs and batching output
        self.doc_id   = FIRST_CHUNK_ID
        self.acc      = []
        self.file_idx = 1

    def run(self):
        """
        Walk through all deduplicated TXT files and produce JSON chunk files.
        """
        all_txts = list(self.txt_root.rglob("*.txt"))
        print(f"Found {len(all_txts)} text files to chunk")

        for txt_path in tqdm(sorted(all_txts), desc="Chunking files"):
            folder = txt_path.parent.name
            spec, gen = self._parse_folder(folder)
            self._handle_file(txt_path, spec, gen)

        self._flush(final=True)

    def _handle_file(self, txt_path: Path, spec: str, gen: str):
        """
        Read a TXT file, split into semantic chunks, and accumulate them.
        """
        text = txt_path.read_text(encoding="utf-8")
        docs = self.splitter.create_documents([text])

        for doc in docs:
            self.doc_id += 1
            self.acc.append({
                "page_content":  doc.page_content,
                "specific_type": spec,
                "general_type":  gen,
                "source":        txt_path.stem,
                "id":            self.doc_id,
            })

            # dump to disk once batch size reached
            if len(self.acc) >= MAX_ITEMS_PER_JSON:
                self._flush()

    def _flush(self, final: bool = False):
        """
        Write out accumulated chunks to a JSON file, then reset accumulator.
        """
        if not self.acc:
            return

        out_path = self.out_root / f"chunks_{self.file_idx:03d}.json"
        out_path.write_text(
            Path.json_dumps(self.acc, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"Wrote {len(self.acc)} chunks → {out_path.name}")

        # reset for next batch
        self.acc.clear()
        self.file_idx += 1

        if final:
            print("All chunking done!")

    @staticmethod
    def _parse_folder(name: str):
        """
        Infer specific/general types from folder naming convention.
        """
        if "_HT_" in name:
            sp, gp = name.split("_HT_", 1)
            if gp.endswith("_txt"):
                gp = gp[:-4]
            return sp, gp
        return name, ""
