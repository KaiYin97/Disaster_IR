# DisastIR: A Comprehensive Information Retrieval Benchmark for Disaster Management.

---

## 📜 License & Dataset Link
**License:** MIT License   ||     **Dataset:** [Hugging Face](https://huggingface.co/datasets/KaiYinTAMU/DisastIR)

---
## 📰 News
- **[20/Aug]** Our *DisastIR* has been accepted to **EMNLP 2025 Findings** 🎉  
- **[15/Sep]** *DisastIR* is now publicly available at [Hugging Face Datasets](https://huggingface.co/datasets/KaiYinTAMU/DisastIR)

---
## 📑 Table of Contents

1. [📘 Introduction](#-1introduction)
2. [📊 Statistics of DisastIR](#-2statistics-of-disastir)
3. [📈 Leaderboard](#-3leaderboard)
4. [🔍 Workflow Overview](#-4workflow-overview)
5. [📂 Directory Structure](#-5directory-structure)
6. [🛠️ Installation](#-installation)
7. [⚙️ Configuration](#-configuration)
8. [🚀 Pipeline Steps](#-8pipeline-steps)
   - [1. Build Corpus](#-8-1build-corpus)
   - [2. Generate Queries](#-8-2generate-queries)
   - [3. Build Label Pool](#-8-3build-label-pool)
   - [4. Relevance Scoring](#-8-4relevance-scoring)
9. [📈 Viewing Results](#-9viewing-results)
10. [📝 Tips](#-10tips)



---
## 📘 1.Introduction
Effective disaster management requires timely access to accurate and contextually relevant information. Existing Information Retrieval (IR) benchmarks, however, focus primarily on general or specialized domains, such as medicine or finance, neglecting the unique linguistic complexity and diverse information needs encountered in disaster management scenarios. To bridge this gap, we introduce \textbf{DisastIR}, the first comprehensive IR evaluation benchmark specifically tailored for disaster management. DisastIR comprises 9,600 diverse user queries and more than 1.3 million labeled query-passage pairs, covering 48 distinct retrieval tasks derived from six search intents and eight general disaster categories that include 301 specific event types. Our evaluations of 30 state-of-the-art retrieval models demonstrate significant performance variances across tasks, with no single model excelling universally. Furthermore, comparative analyses reveal significant performance gaps between general-domain and disaster management-specific tasks, highlighting the necessity of disaster management-specific benchmarks for guiding IR model selection to support effective decision-making in disaster management scenarios.

<p align="center">
  <img src="disasIR_workflow.jpg" width="600"/>
</p>

---
## 📊 2.Statistics of DisastIR

The following table summarizes the number of labeled query-passage pairs and the average number of pairs per query (shown in parentheses) across six task types and eight disaster categories in the DisastIR benchmark:

|              | QA (avg)         | QAdoc (avg)      | Twitter (avg)     | FC (avg)         | NLI (avg)        | STS (avg)        |
|--------------|------------------|------------------|-------------------|------------------|------------------|------------------|
| **Bio**      | 26651 (133.3)    | 25335 (126.7)    | 35182 (175.9)     | 23987 (119.9)    | 25896 (129.5)    | 27065 (135.3)    |
| **Chem**     | 26885 (134.4)    | 26032 (130.2)    | 34186 (170.9)     | 24592 (123.0)    | 27856 (139.3)    | 26787 (133.9)    |
| **Env**      | 26685 (133.4)    | 25930 (129.7)    | 33243 (166.2)     | 25805 (129.0)    | 25207 (126.0)    | 27048 (135.2)    |
| **Extra**    | 26807 (134.0)    | 25598 (128.0)    | 33202 (166.0)     | 24363 (121.8)    | 26399 (132.0)    | 27313 (136.6)    |
| **Geo**      | 27140 (135.7)    | 26573 (132.9)    | 35503 (177.5)     | 27864 (139.3)    | 28210 (141.1)    | 29816 (149.1)    |
| **MH**       | 28422 (142.1)    | 27256 (136.3)    | 33924 (169.6)     | 26670 (133.4)    | 27052 (135.3)    | 28702 (143.5)    |
| **Soc**      | 27116 (135.6)    | 23353 (116.8)    | 33834 (169.2)     | 27850 (139.3)    | 26997 (135.0)    | 27074 (135.4)    |
| **Tech**     | 28044 (140.2)    | 27071 (135.4)    | 33388 (166.9)     | 26759 (133.8)    | 28394 (142.0)    | 26920 (134.6)    |


---
## 📈 3.Leaderboard


| Model                          | Size  | Type   | MTEB Avg | MIRACL | XOR-TyDi | BEIR | LoCo | M3 | Ex.Avg | Ann.Avg | Drop |
|--------------------------------|-------|--------|----------|--------|----------|------|------|----|--------|---------|------|
| Linq-Embed-Mistral             | 7B    | XL     | 74.40    | **70.50** | 64.22    | **70.77** | 52.56 | 71.35 | **67.30** | **66.98** | 0.48 |
| SFR-Embedding-Mistral          | 7B    | XL     | 71.50    | 67.34   | **69.62** | _70.39_ | 51.08 | 72.71 | _66.71_ | _66.39_ | 0.48 |
| inf-retriever-v1               | 7B    | XL     | _72.84_  | 66.92   | _66.37_  | 65.76 | 52.02 | _76.00_ | 66.65 | 65.98 | 1.01 |
| inf-retriever-v1-1.5b          | 1.5B  | XL     | 69.47    | 64.40   | 63.08    | 65.49 | 54.14 | 73.96 | 65.09 | 64.85 | 0.37 |
| NV-Embed-v2                    | 7B    | XL     | **74.55** | _69.51_ | 42.55    | 68.39 | **58.39** | **76.13** | 64.92 | 64.57 | 0.54 |
| gte-Qwen2-1.5B-instruct        | 1.5B  | XL     | 69.96    | 59.21   | 65.21    | 62.84 | _55.73_ | 73.61 | 64.43 | 64.24 | 0.29 |
| multilingual-e5-large          | 560M  | Large  | 67.08    | 64.08   | 62.99    | 60.06 | 51.20 | 74.14 | 63.26 | 62.79 | 0.74 |
| e5-mistral-7b-instruct         | 7B    | XL     | 65.65    | 65.16   | 63.42    | 67.94 | 47.68 | 66.39 | 62.71 | 61.99 | 1.15 |
| multilingual-e5-large-instruct | 560M  | Large  | 68.14    | 64.72   | 62.46    | 66.96 | 48.75 | 63.53 | 62.43 | 62.01 | 0.67 |
| e5-small-v2                    | 33M   | Small  | 65.66    | 62.84   | 60.10    | 61.78 | 47.12 | 73.93 | 61.90 | 61.48 | 0.68 |
| e5-base-v2                     | 109M  | Medium | 65.54    | 62.91   | 57.76    | 62.11 | 45.52 | 73.73 | 61.26 | 60.72 | 0.88 |
| e5-large-v2                    | 335M  | Large  | 60.03    | 63.24   | 55.48    | 62.03 | 50.96 | 74.09 | 60.97 | 60.45 | 0.85 |
| NV-Embed-v1                    | 7B    | XL     | 68.14    | 62.87   | 56.13    | 59.85 | 48.25 | 67.11 | 60.39 | 59.60 | 1.31 |
| granite-embedding-125m          | 125M  | Medium | 64.63    | 60.85   | 46.55    | 62.56 | 48.11 | 71.06 | 58.96 | 58.60 | 0.61 |
| gte-Qwen2-7B-instruct          | 7B    | XL     | 70.30    | 47.65   | 63.24    | 31.87 | 53.88 | 74.86 | 56.97 | 55.99 | 1.72 |
| snowflake-arctic-embed-m-v2.0  | 305M  | Medium | 61.28    | 62.31   | 47.20    | 57.84 | 42.43 | 64.56 | 55.94 | 55.15 | 1.41 |
| mxbai-embed-large-v1           | 335M  | Large  | 64.37    | 62.79   | 40.07    | 58.30 | 40.26 | 67.96 | 55.62 | 55.25 | 0.67 |
| gte-base-en-v1.5               | 137M  | Medium | 60.46    | 55.85   | 46.44    | 52.34 | 39.85 | 70.41 | 54.22 | 53.93 | 0.53 |
| bge-base-en-v1.5               | 109M  | Medium | 51.65    | 52.89   | 46.78    | 60.13 | 41.41 | 68.56 | 53.57 | 53.13 | 0.82 |
| gte-large-en-v1.5              | 434M  | Large  | 67.46    | 58.37   | 39.71    | 52.90 | 34.79 | 66.51 | 53.29 | 53.21 | 0.15 |
| snowflake-arctic-embed-l-v2.0  | 568M  | Large  | 55.20    | 59.29   | 38.26    | 60.23 | 41.23 | 62.64 | 52.81 | 52.32 | 0.93 |
| bge-large-en-v1.5              | 335M  | Large  | 56.88    | 54.56   | 32.32    | 55.03 | 35.25 | 64.43 | 49.74 | 49.04 | 1.41 |
| bge-small-en-v1.5              | 33M   | Small  | 56.87    | 51.24   | 25.19    | 55.30 | 32.95 | 64.46 | 47.67 | 47.00 | 1.41 |
| snowflake-arctic-embed-s       | 33M   | Small  | 38.69    | 28.82   | 21.43    | 47.30 | 40.02 | 66.95 | 40.54 | 38.15 | 5.90 |
| snowflake-arctic-embed-m-v1.5  | 109M  | Medium | 25.66    | 30.43   | 18.09    | 48.10 | 42.98 | 64.20 | 38.24 | 36.85 | 3.63 |
| snowflake-arctic-embed-l       | 335M  | Large  | 40.73    | 30.33   | 15.11    | 32.60 | 34.44 | 56.11 | 34.89 | 32.17 | 7.80 |
| thenlper-gte-base              | 109M  | Medium | 9.16     | 5.34    | 38.06    | 60.58 | 42.80 | 45.99 | 33.66 | 32.22 | 4.28 |
| snowflake-arctic-embed-m       | 109M  | Medium | 33.26    | 14.22   | 8.62     | 35.16 | 38.75 | 56.21 | 31.02 | 29.42 | 5.16 |
| snowflake-arctic-embed-m-long  | 137M  | Medium | 21.43    | 10.84   | 19.49    | 36.20 | 41.90 | 55.00 | 30.81 | 29.30 | 4.90 |
| thenlper-gte-small             | 33M   | Small  | 18.20    | 9.08    | 11.04    | 49.81 | 37.71 | 55.47 | 30.22 | 29.43 | 2.61 |



---

## 🔍 4.Workflow Overview

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

## 📂 5.Directory Structure

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

## 🛠️Installation

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

## ⚙️Configuration

All paths and constants are centralized:

- **`configs/path_config.py`**  
- **`configs/model_config.py`**  
- **`configs/gen_config.py`**

---

## 🚀 8.Pipeline Steps

### 8-1. Build Corpus

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

### 8-2. Generate Queries

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

### 8-3. Build Label Pool

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

### 8-4. Relevance Scoring

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
    "score_phase4": 1,
    "score_cot": 2,
    "score_zero_shot": 3,
    "score_majority_vote": 2,
    "score_average": 2
  }
  ```
---

## 📈 9.Viewing Results

- **Raw scores**: `outputs/scores/<task>_…_qrels.json`  
- **Reports**: under `outputs/results`.
- **Benchmark release**: We will publicly release the full DisastIR benchmark after the anonymous review stage to support future research on disaster management-specific information retrieval models. 

---

## 📝 10.Tips

- Adjust `configs/*_config.py` for batch sizes, retrials.  
- Run in parallel by splitting `file_index`/`part_index`.  
- Monitor OpenAI usage for quotas.

---
## Citation

If you find this repository helpful, please kindly consider citing the corresponding paper as shown below. Thanks!

```bibtex
@article{yin2025disastir,
    title={DisastIR: A Comprehensive Information Retrieval Benchmark for Disaster Management},
    author={Yin, Kai and Dong, Xiangjue and Liu, Chengkai and Huang, Lipai and Xiao, Yiming and Liu, Zhewei and Mostafavi, Ali and Caverlee, James},
    journal={arXiv preprint arXiv:2505.15856},
    year={2025}
}
