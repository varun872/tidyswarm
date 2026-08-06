from langgraph.graph import END, StateGraph
from src.nodes import data_auditor 
from src.nodes import code_engineer
from src.nodes import code_executor
from src.nodes import data_validator
from src.state import SwarmState
from src.config import MAX_RETRIES


def route_next_step(state: SwarmState) -> str:
    """Determines whether to complete the pipeline or loop back for self-correction."""
    if state.get("status") == "success":
        return "validator"

    if state.get("retry_count", 0) >= MAX_RETRIES:
        print(f"🛑 Pipeline terminated: Exceeded maximum repair attempts ({MAX_RETRIES}).")
        print(f"❗ Error Log: {state.get('error_log', 'No error log available.')}")
        return END

    print(f"🔄 Code execution failed. Looping back to Auditor with error logs (Attempt {state.get('retry_count')} of {MAX_RETRIES})...")
    print(f"❗ Error Log: {state.get('error_log', 'No error log available.')}")
    return "auditor"


def build_graph():
    """Builds and compiles the Scrub Swarm LangGraph state machine."""
    workflow = StateGraph(SwarmState)

    # 1. Register Nodes
    workflow.add_node("auditor", data_auditor)
    workflow.add_node("engineer", code_engineer)
    workflow.add_node("executor", code_executor)
    workflow.add_node("validator", data_validator)

    # 2. Define Sequential Edges
    workflow.set_entry_point("auditor")
    workflow.add_edge("auditor", "engineer")
    workflow.add_edge("engineer", "executor")
    workflow.add_edge("validator", END)

    # 3. Define Conditional Self-Correction Edge
    workflow.add_conditional_edges("executor", route_next_step)

    return workflow.compile()