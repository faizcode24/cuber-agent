
# Cyber Ireland Autonomous Intelligence Backend

## Overview

This project implements an **agentic AI backend system** that transforms a static PDF report into a **dynamic, queryable knowledge system**.

The system ingests the **Cyber Ireland 2022 Report**, processes both **unstructured text and structured tables**, and enables an autonomous agent to answer complex multi-step questions with **verifiable citations and deterministic calculations**.

Unlike traditional Retrieval-Augmented Generation (RAG) systems, this architecture combines:

* Vector-based semantic search
* Structured SQL data retrieval
* Tool-based mathematical reasoning
* Agent orchestration with execution traces

The goal is to ensure **high factual reliability, transparency of reasoning, and strong data liquidity**.

---

# System Architecture

The system uses a **hybrid architecture combining vector search, SQL querying, and tool-based reasoning**.

```
PDF Document
      │
      ▼
ETL Pipeline
      │
 ┌───────────────┬───────────────┐
 │               │               │
Text Chunks   Parsed Tables   Metadata
 │               │
 ▼               ▼
Vector Database  PostgreSQL
      │
      ▼
Agent Orchestrator (LangGraph)
      │
 ┌────┴─────────────┬─────────────┬─────────────┐
 │                  │             │
Vector Tool     SQL Tool     Math Tool     Citation Tool
 │
 ▼
Verified Answer + Execution Trace
```

This architecture ensures the agent can:

* retrieve semantic information
* query structured data
* perform deterministic calculations
* validate citations

---

# Key Components

## 1. ETL Pipeline

The ETL pipeline extracts both **text and structured tables** from the PDF.

### Text Extraction

Uses:

* `pdfplumber`

Extracted text is chunked and stored in a **vector database** with metadata including page numbers.

### Table Extraction

Uses:

* `camelot`
* `tabula-py`

Extracted tables are cleaned and loaded into **PostgreSQL** to enable deterministic querying.

---

## 2. Vector Database

The system uses a vector database (such as **Qdrant**) to store semantic embeddings of text chunks.

Metadata stored with each chunk includes:

* page number
* section
* source text

This enables accurate citation retrieval.

---

## 3. SQL Database

Structured data extracted from tables is stored in PostgreSQL.

Example schema:

```
regional_stats
--------------
region
metric
value
year
source_page
```

This allows precise comparisons such as **regional vs national metrics**.

---

## 4. Agent Orchestration

The system uses **LangGraph** to implement an agent that can plan and execute multi-step reasoning tasks.

The agent performs:

1. Query analysis
2. Tool selection
3. Execution
4. Verification
5. Final response generation

---

# Tools Used by the Agent

## Vector Search Tool

Retrieves relevant document chunks using semantic similarity.

Used for:

* narrative information
* citation retrieval
* baseline values

---

## SQL Query Tool

Retrieves structured numerical data from the SQL database.

Used for:

* regional comparisons
* statistical values
* national averages

---

## Math Tool

Performs deterministic calculations using Python.

Example usage:

* Compound Annual Growth Rate (CAGR)
* percentage comparisons
* derived metrics

This avoids mathematical hallucinations by the LLM.

---

## Citation Validation Tool

Ensures that answers referencing the report include:

* exact text snippet
* page number
* source verification

This prevents hallucinated citations.

---

# API Endpoint

### POST `/query`

Send a natural language query to the agent.

Example request:

```
POST /query
{
  "query": "What is the total number of jobs reported and where is it stated?"
}
```

Example response:

```
{
  "answer": "18,475 jobs",
  "page": 17,
  "citation": "Total employment in Ireland’s cybersecurity sector reached 18,475 jobs in 2022."
}
```

---

# Setup Instructions

## 1. Clone the repository

```
git clone <repo-url>
cd cyber-ireland-agent
```

---

## 2. Install dependencies

```
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/cyber
QDRANT_URL=http://localhost:6333
```

---

## 4. Start services

```
docker-compose up -d
```

This starts:

* PostgreSQL
* Qdrant vector database

---

## 5. Run the ETL pipeline

```
python etl/run_pipeline.py
```

This will:

* extract text from the PDF
* parse tables
* load vector embeddings
* populate the SQL database

---

## 6. Start the backend

```
uvicorn app.main:app --reload
```

API will run at:

```
http://localhost:8000
```

---

# Execution Logs

The system records agent reasoning traces in:

```
logs/agent_traces.json
```

Example log entry:

```
{
 "timestamp": "...",
 "query": "...",
 "steps": [
   {"tool": "vector_search"},
   {"tool": "citation_validator"}
 ]
}
```

These logs provide transparency into how the agent arrives at its answers.

---

# Evaluation Scenarios

The system is designed to successfully handle the following test queries.

### Test 1: Verification Challenge

Query:

"What is the total number of jobs reported, and where exactly is this stated?"

Expected behavior:

* retrieve correct number
* return page number
* return exact citation

---

### Test 2: Data Synthesis Challenge

Query:

"Compare the concentration of Pure-Play cybersecurity firms in the South-West against the national average."

Expected behavior:

* query SQL table
* extract regional metrics
* compute comparison
* return synthesized result

---

### Test 3: Forecasting Challenge

Query:

"Based on our 2022 baseline and the 2030 target, what CAGR is required?"

Expected behavior:

* retrieve baseline
* retrieve target
* calculate CAGR using math tool

---

# Architecture Justification

### Hybrid Retrieval

Using both **vector search and SQL databases** allows the system to handle both narrative and structured data effectively.

### Tool-based Reasoning

Delegating math and structured queries to specialized tools ensures higher reliability compared to pure LLM reasoning.

### LangGraph Orchestration

LangGraph provides:

* deterministic agent workflows
* clear execution traces
* better control over tool usage

---

# Limitations

### Table Extraction Complexity

Some PDFs contain irregular layouts that may require manual adjustment to parsing logic.

### Agent Planning Simplicity

The current planner uses heuristic routing. This could be improved with a more advanced LLM-based planning module.

### Scalability

For large-scale deployments, improvements would include:

* distributed vector database
* async query execution
* caching layers
* observability tools

---

# Future Improvements

Potential enhancements include:

* automated evaluation pipelines
* self-correcting retrieval loops
* graph-based knowledge representation
* improved table normalization

---

# Conclusion

This project demonstrates a **robust agentic architecture for document intelligence**, combining structured and unstructured data processing with reliable multi-step reasoning.

The system emphasizes:

* factual accuracy
* transparency
* extensibility

and provides a strong foundation for building scalable document intelligence platforms.
