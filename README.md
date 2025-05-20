# DisastIR
The source code for **DisastIR: A Comprehensive Information Retrieval Benchmark for Disaster Management.**
We develop this complete end-to-end pipeline for constructing Disaster Information Retrieval (DisastIR) benchmark from scratch, starting from PDF download and text extraction, through semantic chunking and deduplication, to user query generation, labeling-pool construction, and final relevance scoring.

---

## 🔍 Project Overview

1. **Corpus Construction**  
   - Download disaster management-related PDFs.  
   - Extract and clean text.  
   - Deduplicate at the file and chunk level.  
   - Semantic chunking into passages.

2. **Query Generation**  
   - Passage-level tasks: Twitter, QA, STS, Fact-Check, NLI.  
   - Document-level QA.

3. **Retrieval & Label Pool**  
   - Encode corpus & queries with dense models.  
   - Build ANN indices, perform exact & approximate retrieval.  
   - Merge top-K results into `label_pool.json`.

4. **Relevance Scoring**  
   - Rate each (query, passage) pair via three LLM-based raters:  
     - Four-phase decomposed  
     - Chain-of-Thought  
     - Zero-Shot  
   - Aggregate scores (majority vote, average).

---

## 📂 Directory Structure

```
DisastIR/
├── README.md
├── requirements.txt
├── configs/
│   ├── path_config.py      # all paths
│   ├── model_config.py     # model names, device, batch sizes
│   └── gen_config.py       # LLM settings, prompt templates
├── data/
│   ├── raw_pdf/
│   ├── txt_cleaned/
│   ├── deduped_chunks/
│   ├── embeddings/
│   └── label_pools/
├── outputs/
│   ├── scores/
│   └── results/
├── scripts/
│   ├── build_corpus.py
│   ├── generate_queries.py
│   ├── build_label_pool.py
│   └── relevance_scoring.py
└── src/
    ├── __init__.py
    ├── corpus/             # downloader, manager, processor, chunker, deduper
    ├── query/              # client, generators, pipeline
    ├── retrieval/          # embedder, index_builder, retriever, label_pool_builder
    ├── scoring/            # scorer + raters
    └── utils/              # embedding, llm, io, misc helpers
```

---

## 🛠️ Installation

1. **Clone & enter project**  
   ```bash
   git clone https://<your-repo>.git
   cd DisastIR
   ```

2. **Create a Python 3.10+ virtual env**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**  
   Edit `configs/gen_config.py`:
   ```python
   OPENAI_API_KEY = "sk-..."
   ```

---

## ⚙️ Configuration

All paths and constants are centralized:

- **`configs/path_config.py`**  
- **`configs/model_config.py`**  
- **`configs/gen_config.py`**

---

## 🚀 Pipeline Steps

### 1. Build Corpus

```bash
python scripts/build_corpus.py \
  --keywords_json path/to/keywords.json
```

### 2. Generate Queries

```bash
python scripts/generate_queries.py \
  --tasks all \
  --filename chunks_001.json \
  --start_index 0 \
  --end_index 100
```

### 3. Build Label Pool

```bash
python scripts/build_label_pool.py
```

### 4. Relevance Scoring

```bash
python scripts/relevance_scoring.py \
  --task QA \
  --file_index 0 \
  --part_index 0 \
  --input_dir data/label_pools \
  --output_dir outputs/scores \
  --force_default_prompts
```

---

## 📈 Viewing Results

- **Raw scores**: `outputs/scores/<task>_…_qrels.json`  
- **Reports**: under `outputs/results`.

---

## 📝 Tips

- Adjust `configs/*_config.py` for batch sizes, retrials.  
- Run in parallel by splitting file_index/part_index.  
- Monitor OpenAI usage for quotas.


