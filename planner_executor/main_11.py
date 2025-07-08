from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    plan: list
    step_index: int
    final_answer: str

# ----- PLANNER NODE -----
def planner(state):
    query = state["query"].lower()

    # Simulated step planning logic
    if "bedroom" in query:
        state["plan"] = [
            "Check bedroom direction",
            "Verify lighting",
            "Suggest remedy if needed"
        ]
    else:
        state["plan"] = [
            "Check placement",
            "Suggest improvement"
        ]
    
    state["step_index"] = 0
    return state

# ----- EXECUTOR NODE -----
def executor(state):
    steps = state["plan"]
    i = state["step_index"]

    if i >= len(steps):
        return state  # No more steps

    current_step = steps[i]

    # Simulated execution output
    result = f"✅ Step {i+1}: {current_step} completed."
    print(result)

    if "final_answer" not in state:
        state["final_answer"] = result
    else:
        state["final_answer"] += "\n" + result

    state["step_index"] += 1
    return state

# ----- CHECK CONTINUE LOOP -----
def should_continue(state):
    return "executor" if state["step_index"] < len(state["plan"]) else "output"

# ----- OUTPUT NODE -----
def output_node(state):
    print("\n🎯 Final Response:\n" + state["final_answer"])
    return state

# ----- WRAP -----
graph = StateGraph(GraphState)
graph.set_entry_point("planner")

graph.add_node("planner", RunnableLambda(planner))
graph.add_node("executor", RunnableLambda(executor))
graph.add_node("output", RunnableLambda(output_node))

# Looping logic
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

# ----- RUN TEST -----
print("\n🧪 Planner → Executor Agent")
app.invoke({"query": "Where should I place the bedroom?"})
