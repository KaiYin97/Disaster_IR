# DisastIR
The source code for **DisastIR: A Comprehensive Information Retrieval Benchmark for Disaster Management.**

We develop this end-to-end pipeline for constructing Disaster Information Retrieval (DisastIR) benchmark from scratch, starting from PDF download and text extraction, through semantic chunking and deduplication, to user query generation, labeling-pool construction, and final relevance scoring.

---

## 📑 Table of Contents

1. [Overview](#-overview)  
2. [Directory Structure](#-directory-structure)  
3. [Installation](#️-installation)  
4. [Configuration](#⚙️-configuration)  
5. [Pipeline Steps](#-pipeline-steps)  
   - [1. Build Corpus](#1-build-corpus)  
   - [2. Generate Queries](#2-generate-queries)  
   - [3. Build Label Pool](#3-build-label-pool)  
   - [4. Relevance Scoring](#4-relevance-scoring)  
6. [Viewing Results](#📈-viewing-results)  
7. [Tips](#📝-tips)  

---

## 🔍 Overview

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
python scripts/build_corpus.py   --keywords_json path/to/keywords.json
```

**Input:**  
- `--keywords_json`: JSON array of disaster-related search keywords, e.g.:

  ```json
  [
    "Civil unrest",
    "Earthquake",
    "Building collapse"
  ]
  ```

**Output:**  
1. **Downloaded PDFs**  
   - `data/raw_pdf/{keyword}/file_X.pdf`  
2. **Extracted & Cleaned Text**  
   - `data/txt_cleaned/{keyword}_txt/*.txt` (and `.csv` for tables)  
3. **File-level Deduplication**  
   - Unique: `data/deduped_txt/`  
   - Duplicates: `data/dup_txt/`  
4. **Semantic Chunking**  
   - `data/chunks_json/chunks_<batch>.json`, each record:
     ```json
     {
       "page_content": "...",
       "specific_type": "Hazardous waste",
       "general_type": "Chemical",
       "source": "file_1",
       "id": 1
     }
     ```
5. **Embedding-level Deduplication**  
   - `data/deduped_chunks/deduped_<batch>.json`

---

### 2. Generate Queries

```bash
python scripts/generate_queries.py --tasks all --filename chunks_001.json --start_index 0 --end_index 100
```

**Passage-level Query Generation**

**Input:**

1. **Chunk Files**  
   Directory: `data/deduped_chunks/`  
   Each file (e.g. `chunks_001.json`) is a JSON list of chunk objects:
   ```json
   [
     {
       "page_content": "Floods are the most common natural disaster ...",
       "specific_type": "Flood",
       "general_type": "WaterHazard",
       "source": "doc1",
       "id": 1
     },
     {
       "page_content": "Emergency kits should include ...",
       "specific_type": "Preparedness",
       "general_type": "Safety",
       "source": "doc1",
       "id": 2
     }
   ]
   ```
2. **Prompt Templates**  
   Defined in `configs/gen_config.py` or external JSON at `PROMPTS_FILE`.
3. **OpenAI Client & Tokenizer**  
   Configured with `OPENAI_API_KEY` and the specified model.

**Output (Passage-level):**

- Batch files under `data/test_queries/`, named:
  ```
  chunks_001_batch_001.json
  chunks_001_batch_002.json
  ...
  ```
- Each record includes original chunk fields plus task‐specific generated fields. Example for Twitter & QA:
  ```json
  {
    "page_content": "...",
    "specific_type": "Flood",
    "general_type": "WaterHazard",
    "source": "doc1",
    "id": 1,

    "Twitter_config": {
      "headline_1": { "task": "Generate a tweet about evacuation" }
    },
    "Twitter": {
      "query_1": "What should people do when floods rise?",
      "positive_tweet_1": "Stay informed via official channels...",
      "hard_negative_tweet_1": "I love rain!"
    },

    "QA_config": {
      "user_query_1": {
        "task": "Evacuation procedure",
        "query_length": "medium",
        "clarity": "clear",
        "difficulty": "easy",
        "num_words": 20
      }
    },
    "QA": {
      "user_query_1": "How do I evacuate safely during a flood?",
      "positive_document_1": "First, gather your essentials...",
      "hard_negative_document_1": "Floods are fun!"
    }
  }
  ```

**Document-level Query Generation**

- Include `doc` in `--tasks`.
- Outputs under `data/document_queries/`, e.g. `doc_batch_001.json`:
  ```json
  {
    "user_query": "What is the recommended evacuation radius?",
    "positive_document": "In case of a chemical spill, evacuate to at least 1 mile away...",
    "doc_title": "Chemical Spill Response Guide",
    "source": "doc2"
  }
  ```
---

### 3. Build Label Pool

The Build Label Pool step merges retrieval results into a label pool for each query set.

**Input:**

- **Query Files**: JSON files under `data/test_queries/`, each containing a list of records:
  ```json
  [
    {
      "user_query": "What are the evacuation procedures for floods?"
    },
    {
      "user_query": "How to prepare an emergency kit?"
    }
  ]
  ```
- **Query Embeddings**: NumPy `.npy` files under `data/query_embeddings/{model_name}/{filename}.npy`.
- **Corpora**: Ordered corpus JSON at `data/deduped_chunks/ordered_corpus.json`.

**Output:**

- **Label Pool Files**: For each query file `chunks_001.json`, produces `chunks_001_label_pool.json` under `data/label_pools/`. Each record is extended with `baseline_results` and `label_pool`:
  ```json
  [
    {
      "user_query": "What are the evacuation procedures for floods?",
      "baseline_results": {
        "infly_inf-retriever-v1_exact": [
          "Passage text A",
          "Passage text B"
        ],
        "infly_inf-retriever-v1_ann": [
          "Passage text C",
          "Passage text D"
        ]
      },
      "label_pool": [
        "Passage text A",
        "Passage text B",
        "Passage text C",
        "Passage text D"
      ]
    },
    ...
  ]
  ```

Run the script:
```bash
python scripts/build_label_pool.py
```

---

### 4. Relevance Scoring

```bash
python scripts/relevance_scoring.py   --task QA   --file_index 0   --part_index 0 
```

**Input:**  
- **Label Pool Files**: JSONs under `data/label_pools/`, each json item:
  ```json
  {
    "user_query": "What measures help contain hazardous waste leaks?",
    "label_pool": [
      "Passage A",
      "Passage B",
      ...
    ]
  }
  ```
- **Parameters:**  
  - `--task`: one of QA, FactCheck, NLI, STS, Twitter.  
  - `--file_index` / `--part_index`: slice into batches (`ITEMS_PER_PART`).  
  - `--force_default_prompts`: override prompts for FactCheck/NLI.

**Output:**  
- **Qrels Files**: `outputs/scores/{task}_..._qrels.json`. Each entry:
  ```json
  {
    "original_query": "...",
    "passage": "...",
    "score_phase4": 2,
    "score_cot": 1,
    "score_zero_shot": 2,
    "score_majority_vote": 2,
    "score_average": 1.67
  }
  ```
---

## 📈 Viewing Results

- **Raw scores**: `outputs/scores/<task>_…_qrels.json`  
- **Reports**: under `outputs/results`.
- **Benchmark release**: We will publicly release the full DisastIR benchmark after the anonymous review stage to support future research on disaster management-specific information retrieval models. 

---

## 📝 Tips

- Adjust `configs/*_config.py` for batch sizes, retrials.  
- Run in parallel by splitting `file_index`/`part_index`.  
- Monitor OpenAI usage for quotas.
