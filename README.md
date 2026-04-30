# AgentML

An agentic AutoML backend that takes a raw CSV or Excel dataset and automatically performs EDA, generates LLM-based preprocessing recommendations, validates and executes them, and returns a clean ML-ready dataset.

---

## What it does

1. User uploads a dataset (CSV or Excel) via the API
2. The system runs a LangGraph pipeline that:
   - Validates and ingests the data
   - Quick-encodes obvious binary columns (yes/no, male/female, true/false, etc.)
   - Detects column schema (numeric, categorical, text, datetime)
   - Runs full EDA (summary, statistics, missing values, skewness, correlation, class imbalance, health score)
   - Sends dataset context to an LLM which recommends a preprocessing plan
   - Validates the plan against the actual dataframe (removes hallucinated columns, invalid steps)
   - Executes the validated steps (impute, encode, scale, transform, drop, SMOTE)
   - Generates a plain-English health explanation
   - Saves the processed dataset to disk
3. Frontend polls for progress, fetches results, and downloads the processed CSV

---

## Architecture

```
FastAPI (api/)
    └── Background job (jobs/runner.py)
            └── LangGraph pipeline (workflow/graph.py)
                    ├── ingest_node
                    ├── quick_preprocess_node  →  tools/encoding_tools.py
                    ├── schema_detect_node     →  tools/schema_tools.py
                    ├── eda_node               →  tools/eda_tools.py
                    │                             tools/distribution_tools.py
                    │                             tools/correlation_tools.py
                    │                             tools/health_tools.py
                    ├── prompt_build_node      →  llm/prompts.py
                    ├── llm_recommend_node     →  llm/client.py
                    ├── validate_plan_node
                    ├── apply_preprocessing_node → tools/preprocessing_tools.py
                    ├── health_explain_node    →  llm/client.py
                    └── output_node
```

---

## Folder Structure

```
server/
├── main.py                  # FastAPI entry point
├── api/
│   ├── router.py            # 4 REST endpoints
│   ├── models.py            # Pydantic request/response schemas
│   ├── dependencies.py      # Shared FastAPI dependencies
│   └── middleware.py        # CORS, request logging
├── jobs/
│   ├── registry.py          # In-memory job store
│   └── runner.py            # Async graph executor
├── workflow/
│   ├── graph.py             # LangGraph StateGraph definition
│   ├── state.py             # AgentMLState TypedDict
│   └── edges.py             # Conditional edge routing
├── nodes/                   # One file per pipeline node
├── tools/                   # Pure computation functions
├── llm/
│   ├── client.py            # OpenAI model calls
│   ├── prompts.py           # Prompt builder
│   └── schema.py            # Pydantic output schemas
├── core/
│   └── data_loader.py       # CSV/Excel loader
├── uploads/                 # Incoming files (temp)
├── outputs/                 # Processed CSVs (by job_id)
└── logs/
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/run` | Upload file, start pipeline, returns `job_id` |
| GET | `/api/v1/status/{job_id}` | Poll progress (`current_node`, `progress` 0–100) |
| GET | `/api/v1/result/{job_id}` | Fetch full results (EDA + preprocessing output) |
| GET | `/api/v1/download/{job_id}` | Download processed CSV |

---

## Setup

**1. Clone and install dependencies**
```bash
cd server
pip install -r requirements.txt
```

**2. Set up environment variables**

Create a `.env` file in the project root (`AutoEDA/`) with:
```
OPENAI_API_KEY=your_api_key_here
```

**3. Run the server**
```bash
uvicorn main:app --reload
```

**4. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## Usage (via Swagger UI)

1. `POST /api/v1/run` — upload your CSV, set `target` column and `problem_type` (`classification` or `regression`), copy the returned `job_id`
2. `GET /api/v1/status/{job_id}` — poll every few seconds until `status` is `completed`
3. `GET /api/v1/result/{job_id}` — fetch the full result JSON
4. `GET /api/v1/download/{job_id}` — paste into browser to download the processed CSV

---

## Preprocessing Steps Supported

| Step | Description |
|------|-------------|
| `Impute` | Mean / Median / Mode imputation |
| `Encode` | Label encoding |
| `One_Hot` | One-hot encoding |
| `Scale` | StandardScaler or MinMaxScaler |
| `Transform` | Log transform (log1p) |
| `Drop` | Drop unnecessary columns |
| `SMOTE` | Synthetic oversampling (classification only) |

---

## Tech Stack

- **LangGraph** — pipeline orchestration
- **LangChain + OpenAI** — LLM calls with structured output
- **FastAPI** — REST API with background task execution
- **Pydantic** — structured LLM output schemas and API models
- **scikit-learn** — scaling, encoding
- **imbalanced-learn** — SMOTE
- **pandas / numpy** — data processing
- **LangSmith** — tracing and observability
