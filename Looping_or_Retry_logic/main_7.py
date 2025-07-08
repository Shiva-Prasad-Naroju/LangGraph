from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    retries: int
    answer: str
    confidence: float

# ----- NODE 1: THINK -----
def think(state):
    print(f"\n🧠 Reasoning attempt #{state['retries'] + 1}...")
    query = state["query"]

    # Simulated logic: If query contains 'kitchen', we're confident
    if "kitchen" in query.lower():
        state["answer"] = "✅ Place kitchen in southeast as per Vaasthu."
        state["confidence"] = 0.95
    else:
        state["answer"] = "🤔 Still unclear... trying again."
        state["confidence"] = 0.4

    state["retries"] += 1
    return state

# ----- NODE 2: EXIT DECISION -----
def should_continue(state):
    if state["confidence"] > 0.9:
        return "exit"
    elif state["retries"] >= 3:
        return "fallback"
    else:
        return "retry"

# ----- NODE 3: FALLBACK -----
def fallback(state):
    state["answer"] = "⚠️ Unable to determine. Please rephrase your query."
    return state

# ----- NODE 4: OUTPUT -----
def output(state):
    print("\n🟢 Final Output:", state["answer"])
    return state

# ----- GRAPH BUILD -----
think_node = RunnableLambda(think)
fallback_node = RunnableLambda(fallback)
output_node = RunnableLambda(output)

graph = StateGraph(GraphState)
graph.add_node("think", think_node)
graph.add_node("fallback", fallback_node)
graph.add_node("output", output_node)

# Control Flow
graph.set_entry_point("think")
graph.add_conditional_edges(
    "think",
    should_continue,
    {
        "exit": "output",
        "retry": "think",
        "fallback": "fallback"
    }
)
graph.add_edge("fallback", "output")
graph.add_edge("output", END)

app = graph.compile()

# ----- RUN TEST -----
print("\n=== Test Case 1: Confident Query ===")
app.invoke({"query": "Where should I place my kitchen?", "retries": 0})

print("\n=== Test Case 2: Ambiguous Query ===")
app.invoke({"query": "Where to keep things?", "retries": 0})
