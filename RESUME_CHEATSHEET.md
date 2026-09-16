# YapSearch — Resume & Interview Cheatsheet 🚀

This document is your definitive guide for showcasing **YapSearch** on your resume, LinkedIn, portfolio, and during technical interviews.

---

## 📄 Ready-to-Copy Resume Bullets

Choose the bullet set that matches the role you are applying for:

### Option A: Machine Learning / NLP / AI Engineer
* **Engineered a local semantic search engine** for 5,770+ code-mixed Hinglish group chat messages using `paraphrase-multilingual-MiniLM-L12-v2` and pure NumPy dense indexing, achieving **<45ms retrieval latency** without external vector database dependencies.
* **Solved the zero-keyword overlap retrieval failure mode** by designing a contextual embedding pipeline (concatenating preceding dialogue turns) and implementing a **Z-score normalized hybrid scoring algorithm** (`0.6 raw + 0.4 context`), boosting target message recovery in conversational threads.
* **Constructed an automated evaluation framework** with a 40-query benchmark dataset categorized into semantic, attributed, and temporal queries, measuring Recall@K (R@1: 22.5%, R@5: 37.5%) on conversational code-switched text.

### Option B: Backend / Software Engineer
* **Architected a high-performance local search engine** using FastAPI and NumPy vector operations to index and query 5,770+ unstructured messages in under **45ms** end-to-end.
* **Designed a rule-based pre-filtering pipeline** using vector-aligned NumPy boolean masks to extract speaker and temporal constraints prior to dense vector multiplication, guaranteeing **100% attribution accuracy** and reducing matrix search space.
* **Eliminated vector database infrastructure costs and cold starts** by implementing an in-memory dual-matrix dense index (`raw` and `contextual` 384-dimensional embeddings) serialized as memory-mapped `.npy` arrays.
* **Built and deployed a full-stack interactive interface** featuring asynchronous FastAPI REST endpoints and a responsive glassmorphism UI with thread context expansion (±3 message window).

### Option C: Full-Stack / Product Engineer
* **Built YapSearch**, a full-stack local semantic search tool for messy Hinglish group chats featuring asynchronous FastAPI backend, HuggingFace transformer pipeline, and a modern glassmorphic web interface.
* **Implemented an intelligent query parsing pipeline** capable of simultaneously extracting speaker attribution, relative temporal ranges, and core semantic intent.
* **Engineered contextual message previewing** that dynamically reconstructs surrounding conversation threads (±3 messages) around retrieved hits, surfacing conversational context directly in the UI.

---

## ⏱️ 30-Second Elevator Pitch (Memorize This)

> *"In chat apps like WhatsApp, standard search breaks when you don't remember the exact words used—especially in transliterated Hinglish where spelling varies wildly, or in zero-keyword cases where someone asks 'Did we finalize the trip?' and the answer is just 'bhai Manali final 😂'.*
> 
> *I built **YapSearch**, a local semantic search engine tailored for messy group chats. Instead of relying on a bulky vector database, I built an in-memory NumPy dense index using multilingual transformer embeddings. I solved the zero-keyword overlap problem by indexing both raw messages and contextual preceding turns, fusing them with Z-score normalized hybrid scoring. It also extracts speaker and temporal constraints via pre-filtering boolean masks, serving accurate search results in under 45ms."*

---

## 💡 Key Engineering Decisions & Interview Answers

### Q1: Why pure NumPy instead of Pinecone, Chroma, or Milvus?
**Answer:**
> *"For personal or group-chat-scale search (~5,000 to 100,000 messages), spinning up a distributed vector database introduces network latency, cold starts, and infrastructure costs. 5,770 384-dimensional `float32` vectors consume only **~8.8 MB** in memory. NumPy computes dot-product matrix multiplication across 5,770 vectors in **under 3 milliseconds**. Using NumPy arrays serialized as `.npy` files provided zero-dependency local deployment, instant startup, and sub-50ms end-to-end latency."*

### Q2: What is the "Zero-Keyword Overlap" problem, and how did you solve it?
**Answer:**
> *"In group chats, short messages often lack explicit keywords. For example, a user asks 'Where are we meeting?' but the answer is simply 'canteen aaja'—zero word overlap. Standard semantic search fails because the isolated message vector doesn't encode the question's context.*
> 
> *I solved this by creating a **dual-track contextual embedding pipeline**:
> 1. We compute a **raw embedding** for the individual message.
> 2. We compute a **contextual embedding** by prepending the prior 3 messages from the chat thread.
> 3. During retrieval, we fuse both scores. The contextual vector pulls in situational awareness, while the raw vector preserves precision on direct hits."*

### Q3: Why was Z-score normalization necessary before fusing raw and context scores?
**Answer:**
> *"Raw embeddings and contextual embeddings have fundamentally different cosine similarity distributions. Contextual embeddings are longer and denser, causing their cosine similarities to cluster tightly in a different range and with a smaller standard deviation compared to short, noisy raw messages.*
> 
> *If you do a naive linear blend (`0.6 * raw + 0.4 * context`), the distribution with higher mean or variance unintentionally dominates the ranking. By normalizing both distributions using Z-scores:
> $$z = \frac{s - \mu}{\sigma}$$
> both similarity tracks are centered around zero with unit variance, making the 60/40 weighting mathematically sound and stable."*

### Q4: Why pre-filter with NumPy boolean masks instead of post-filtering?
**Answer:**
> *"If you perform top-k vector search first and then post-filter for 'Priya', you risk discarding all k results if Priya's messages were ranked at positions 11–20. You get an empty result even though relevant messages exist.*
> 
> *Instead, our metadata parser parses speaker names and relative dates (`'last month'`, `'yesterday'`) into a NumPy boolean mask. We slice the embedding matrix **before** computing dot products:
> `valid_embeddings = embeddings[mask]`
> This guarantees 100% attribution recall and actually speeds up computation by shrinking the vector matrix."*

### Q5: How does the model handle code-switched Hinglish without fine-tuning?
**Answer:**
> *"`paraphrase-multilingual-MiniLM-L12-v2` is pre-trained across 50+ languages, including Hindi and English. Because Latin-script transliterated Hindi (Hinglish) shares subword tokens with both English and Romanized South Asian text, the multilingual subword tokenizer maps semantic concepts like 'wifi band hai' close to 'internet not working'. While contrastive fine-tuning would push accuracy higher, multilingual MiniLM provides impressive out-of-the-box cross-lingual semantic alignment at just 22MB footprint."*

---

## 🎯 The 3 Live Demo Queries That Always Win

When demonstrating YapSearch live or recording a screen demo:

1. **`What did Priya say about the budget?`**
   * **Category:** Attributed + Semantic Search
   * **Highlight:** Demonstrates automatic speaker extraction (`Priya`) + intent matching (`budget`).
   * **Rank 1 Result:** Priya: *"budget nahi hai mera"* (`56.9% Match`).

2. **`internet not working`**
   * **Category:** Cross-Lingual Semantic Search (Zero Keyword Overlap)
   * **Highlight:** English technical query matching colloquial Hinglish message with zero shared words.
   * **Rank 1 Result:** Priya: *"wifi band hai no way"* (`46.7% Match`).

3. **`assignment deadline`**
   * **Category:** Semantic Intent Mapping
   * **Highlight:** Maps academic intent to conversational student slang.
   * **Rank 1 Result:** Neha: *"yaar kisi ne project submit kiya?"* (`45.7% Match`).
