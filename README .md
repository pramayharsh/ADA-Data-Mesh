# 🤖 ADA: Autonomous Data Analyst

**A Multi-Agent Mesh for Self-Correcting Data Exploration & Visualization**

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)
![Inference](https://img.shields.io/badge/Inference-Groq-orange.svg)
![Embeddings](https://img.shields.io/badge/Embeddings-HuggingFace-yellow.svg)

ADA is not just a "Text-to-SQL" tool — it is a collaborative ecosystem of specialized AI agents designed to act as a **Virtual Data Science Team**. While standard LLM tools often hallucinate table names or fail on complex joins, ADA uses **Schema-RAG** and a **Self-Correction Loop** to explore databases, write code, generate visualizations, and provide business narratives autonomously.

---

## 🌟 Why ADA Stands Out

Most AI data tools struggle with "context window noise" — sending an entire database schema to an LLM confuses it. ADA solves this via a **Multi-Agent Mesh**:

- **Schema-RAG (The Librarian):** Uses semantic search (BGE-small embeddings) to identify only the most relevant tables for a query, reducing hallucinations.
- **Dialect-Aware Architect:** Specially tuned for SQLite syntax (e.g., `strftime` for dates), preventing the common "Postgres-syntax" errors found in vanilla LLMs.
- **Autonomous Self-Healing:** If a SQL query fails, the Architect captures the traceback, analyzes the error, and attempts a strategic fix before the user ever sees a mistake.
- **Multi-Modal Handoff:** SQL results are passed to a Data Scientist Agent that writes Python code to generate physical `.png` charts, which are then interpreted by a Storyteller Agent.

---

## 🧠 The Agentic Team

ADA operates through four specialized personas:

| Agent | Role | Technology |
|---|---|---|
| **The Librarian** | Metadata & Context | BGE-small + Vector Search |
| **The Architect** | SQL Engineering | Llama 3.3 (Groq) |
| **The Analyst** | Python & Visualization | Pandas + Matplotlib |
| **The Storyteller** | Narrative Synthesis | Generative AI |

### Workflow

```
User Question
    ➡️ Librarian   (Filters Schema)
    ➡️ Architect   (Writes / Self-Heals SQL)
    ➡️ Analyst     (Generates Chart)
    ➡️ Storyteller (Explains "Why it matters")
```

---

## 🛠️ Technical Architecture

| Component | Technology |
|---|---|
| LLM Engine | Groq (`llama-3.3-70b-versatile`) |
| Embeddings | HuggingFace Inference API (`BAAI/bge-small-en-v1.5`) |
| Database | SQLite (Chinook Digital Media Store) |
| Frontend | Streamlit |
| Vector Search | Local NumPy-based Cosine Similarity (lightweight & DLL-safe) |

---

## 📂 Project Structure

```
ADA-Data-Mesh/
├── data/               # SQLite DB, Schema Index, and Generated Charts
├── src/
│   ├── agents/         # Logic for Librarian, Architect, Analyst, Storyteller
│   ├── tools/          # DB Connectors & Setup scripts
│   └── utils/          # Groq/HuggingFace API Clients & Vector Math
├── app.py              # Streamlit Web Dashboard
├── main.py             # Interactive CLI Version
├── .gitignore          # Ignoring .env and venv
├── LICENSE             # The file we just created
├── .env.example        # Template for Users (oringinal locally only - .env)
├── requirements.txt    # Dependencies
└── README.md           # The detailed documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com/)
- [HuggingFace API Token](https://huggingface.co/settings/tokens)

### 1. Clone the Repository

```bash
git clone https://github.com/pramayharsh/ADA-Data-Mesh.git
cd ADA-Data-Mesh
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_key_here
HF_API_KEY=your_huggingface_key_here
```

### 5. Run the Application

**Web Dashboard (Recommended):**

```bash
streamlit run app.py
```

**CLI Version:**

```bash
python main.py
```

---

## 📈 Lessons Learned & Evolution

| Challenge | Solution |
|---|---|
| **The SQL Dialect Trap** | Vanilla LLMs often use Postgres `EXTRACT` functions. ADA's Architect is constrained via system prompting to enforce SQLite `strftime` logic. |
| **The Join Hub Problem** | The Librarian initially missed central "hub" tables like `Track`. Increasing recall to 5 tables and enhancing metadata descriptions fixed complex many-to-many navigation. |
| **Safe Code Execution** | Implemented a sandbox-style `exec()` for the Analyst agent, allowing dynamic chart generation without crashing the main application thread. |

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👤 Author

**Pramay Harsh**
- GitHub: [@pramayharsh](https://github.com/pramayharsh)
- LinkedIn: [Pramay Harsh](https://www.linkedin.com/in/pramay-harsh-71562b1b5/)
