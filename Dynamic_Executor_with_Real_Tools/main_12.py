from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    plan: list
    step_index: int
    steps_done: list
    final_answer: str

# ----- PLANNER -----
def planner(state):
    query = state["query"].lower()

    if "kitchen" in query:
        state["plan"] = ["search", "format"]
    elif "staircase" in query:
        state["plan"] = ["search", "remedy", "format"]
    else:
        state["plan"] = ["search", "format"]

    state["step_index"] = 0
    state["steps_done"] = []
    state["final_answer"] = ""
    return state

# ----- EXECUTOR -----
def executor(state):
    step = state["plan"][state["step_index"]]

    # Dispatch logic
    if step == "search":
        result = "📍 Vaasthu Rule: Place kitchen in southeast."
    elif step == "remedy":
        result = "🪔 Remedy: Place copper pyramid in northwest corner."
    elif step == "format":
        combined = "\n".join(state["steps_done"])
        result = f"✅ Final Vaasthu Guidance:\n{combined}"
    else:
        result = "⚠️ Unknown step."

    # Update state
    state["steps_done"].append(result)
    state["step_index"] += 1
    if step == "format":
        state["final_answer"] = result
    return state

# ----- CONTINUATION CHECK -----
def should_continue(state):
    return "executor" if state["step_index"] < len(state["plan"]) else "output"

# ----- OUTPUT -----
def output_node(state):
    print("\n🎯 Final Output:\n" + state["final_answer"])
    return state

# ----- BUILD GRAPH -----
graph = StateGraph(GraphState)
graph.set_entry_point("planner")

graph.add_node("planner", RunnableLambda(planner))
graph.add_node("executor", RunnableLambda(executor))
graph.add_node("output", RunnableLambda(output_node))

graph.add_edge("planner", "executor")
graph.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor": "executor",
        "output": "output"
    }
)
graph.add_edge("output", END)

app = graph.compile()

# ----- TEST CASES -----
# print("\n🧪 Test 1: Placement Query")
# app.invoke({"query": "Where to place the kitchen?"})

print("\n🧪 Test 2: Remedy Query")
app.invoke({"query": "What is the remedy for staircase in northwest?"})
