from fastapi import FastAPI
from app.schemas.query_schema import QueryRequest
from app.agent import run_agent

app = FastAPI(title="Cyber Ireland Autonomous Agent")

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    return await run_agent(request.query)
