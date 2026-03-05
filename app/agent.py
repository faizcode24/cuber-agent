from langgraph.graph import StateGraph
from app.tools.vector_tool import vector_search
from app.tools.sql_tool import execute_sql
from app.tools.math_tool import calculate_cagr
from app.tools.citation_tool import validate_citation
from app.logger import log_trace

class AgentState(dict):
    pass

async def planner(state: AgentState):
    q = state["query"].lower()
    if "cagr" in q or "growth" in q:
        state["task"] = "math"
    elif "compare" in q or "pure-play" in q:
        state["task"] = "sql"
    else:
        state["task"] = "verification"
    return state

async def executor(state: AgentState):
    if state["task"] == "verification":
        res = vector_search(state["query"])
        state["result"] = validate_citation(res)
    elif state["task"] == "sql":
        state["result"] = execute_sql(state["query"])
    else:
        state["result"] = calculate_cagr(state["query"])

    log_trace(state)
    return state

async def run_agent(query: str):
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    app_graph = graph.compile()
    result = await app_graph.invoke({"query": query})
    return result["result"]
