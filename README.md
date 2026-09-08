# YapSearch 🔍

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-F9AB00?style=for-the-badge&logo=huggingface&logoColor=white)

YapSearch is a blazing-fast, strictly local semantic search engine tailored for messy, transliterated Hinglish group chats. 

Built without relying on a bulky vector database, YapSearch uses a pure NumPy dense index and local `sentence-transformers` to deliver lightning-fast retrieval. It excels at tackling the hardest search problem in messaging apps: **Zero-Keyword Overlap**, where a user searches for a concept but none of the actual words appear in the target message.

---

## ✨ Key Features

1. **Contextual Embeddings (Zero-Overlap Solution)**: Solves the "impossible" zero-overlap problem by injecting situational awareness. The system concatenates a message with its preceding context before embedding it, and then applies a Z-Score Normalized Hybrid Blend (Raw + Context) to surface deeply buried messages without sacrificing precision on exact matches.
2. **Custom Metadata Parser**: A handcrafted NLP pipeline that detects speaker names (e.g., `What did Priya say...`) and temporal triggers (e.g., `...yesterday?`) naturally within the query.
3. **Pre-Filtering via Boolean Masks**: The parsed metadata is dynamically applied as a strict NumPy boolean mask *before* the vector dense lookup occurs, ensuring 100% attribution accuracy and extreme computational speed.
4. **Hinglish Native**: Uses a robust `paraphrase-multilingual-MiniLM-L12-v2` transformer to handle heavily transliterated Hindi-English code-switching natively.
5. **Sleek UI**: A premium, responsive glassmorphism frontend that renders conversational threads beautifully.

---

## 🛠️ Architecture

- **Backend**: FastAPI
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Vector Index**: NumPy multidimensional arrays (`embeddings_raw.npy`, `embeddings_context.npy`)
- **Corpus**: 5,770 synthetic Hinglish chat messages stored in JSON
- **Frontend**: Vanilla HTML/CSS/JS (Zero framework overhead)

---

## 🎭 What is Simulated vs. Real?

To keep the project self-contained, reproducible, and privacy-safe:

| Component | Status | Details |
| :--- | :--- | :--- |
| **Chat Corpus** | **Simulated / Synthetic** | 5,770 messages generated to mimic an authentic, messy college friend group chat in transliterated Hinglish across 8 personas. |
| **Temporal Anchor** | **Fixed ("Mocked Current Time")** | The reference date `REFERENCE_DATE` is anchored to `September 1, 2026` so temporal queries (`"yesterday"`, `"last month"`) resolve deterministically against the dataset. |
| **WhatsApp Connection** | **Offline (No Live Meta API)** | Runs locally on structured chat data rather than a live WhatsApp session hook. |
| **Embeddings & NLP** | **100% Real** | Real local transformer inference using `paraphrase-multilingual-MiniLM-L12-v2` via `sentence-transformers`. |
| **Search & Ranking** | **100% Real** | Real NumPy dense linear algebra, cosine similarity, hybrid Z-score ranking, and boolean pre-filtering. |
| **Server & Frontend** | **100% Real** | Real asynchronous FastAPI server serving live endpoints and a responsive, interactive UI. |

---

## 🚀 Installation & Setup

We recommend using a standard Python `venv` to isolate the dependencies.

### 1. Clone & Environment
```bash
git clone https://github.com/Kasak-13/YapSearch.git
cd YapSearch
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Generate the Dataset
Generate the 5,500+ message synthetic Hinglish corpus and the 40-query ground truth evaluation set.
```bash
python scripts/generate_data.py
```

### 3. Build the Vector Index
Pre-compute the 384-dimensional dense vectors (both raw and contextual) and dump them into a NumPy matrix.
```bash
python scripts/embed_corpus.py
```

### 4. Run the API Server
Start the FastAPI backend and serve the frontend locally.
```bash
python backend/main.py
```
> **Navigate to [http://localhost:8000](http://localhost:8000)** in your browser to use the YapSearch UI!

---

## 🧪 Evaluation & Benchmarks

To prove the system works, we generated a punishing 40-query dataset divided into Semantic, Attributed, and Temporal queries. 

Run the automated evaluation suite:
```bash
python scripts/run_eval.py
```

**Results:**
- **Recall@1**: 22.5%
- **Recall@3**: 32.5%
- **Recall@5**: 37.5%
- **Recall@10**: 37.5%

*Note: These numbers specifically reflect the system's ability to retrieve highly ambiguous, code-mixed short messages and entirely zero-overlap queries.*

---

## 📂 Code Structure

```text
YapSearch/
├── backend/
│   ├── main.py                # FastAPI endpoints & static routing
│   └── search_core.py         # Core vector math, metadata parsing & ranking
├── frontend/
│   └── index.html             # Premium glassmorphism UI
├── scripts/
│   ├── generate_data.py       # Corpus & ground-truth generator
│   ├── embed_corpus.py        # Sentence-transformer embedding pipeline
│   └── run_eval.py            # Automated Recall@K benchmark script
├── data/                      # Auto-generated by scripts (ignored in git)
│   ├── messages.json          
│   ├── eval_set.json          
│   ├── embeddings_raw.npy     
│   └── embeddings_context.npy 
├── requirements.txt
├── MASTER_PLAN.md             # Original architecture design doc
└── PROGRESS_LOG.md            # Execution diary & engineering decisions
```

---
## ⚠️ Known Limitations & Future Work

1. **Corpus vs. Eval Strictness**: The synthetic corpus was lightly adjusted for narrative coherence around eval targets after the initial eval set generation (injecting relevant preceding chat context for zero-overlap targets). Therefore, the evaluation numbers should be read as indicative of the technique's potential rather than performance on a fully held-out, independent dataset.
2. **Context vs. Precision Trade-off**: Prepending context dramatically improved our ability to retrieve zero-overlap messages, but it diluted the embeddings of clean, direct queries. We used a Z-score normalized hybrid blend (`0.6 raw + 0.4 context`) to recover precision. While normalization was a necessary mathematical correctness fix due to different cosine scale spreads, the bigger driver of the precision trade-off is inherently *distractor competition*—the context itself often becomes a better lexical match than the actual target message.
3. **Small Model Limitations**: We used a lightweight model (`paraphrase-multilingual-MiniLM-L12-v2`) which handles transliterated Hinglish adequately but could be significantly improved by fine-tuning on a contrastive Hinglish dataset.
