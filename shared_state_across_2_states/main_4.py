from langgraph.graph import StateGraph
from typing import TypedDict, Optional

# Step 1: Define structured state
class VaasthuState(TypedDict):
    user_input: str
    room: Optional[str]
    warning: Optional[str]
    response: Optional[str]

# Step 2: Classifier node updates `room`
def classify_room(state: VaasthuState) -> VaasthuState:
    text = state["user_input"].lower()
    if "pooja" in text or "puja" in text:
        state["room"] = "pooja"
    else:
        state["room"] = "general"
    return state

# Step 3: Validation node adds a warning if needed
def validate_room(state: VaasthuState) -> VaasthuState:
    if state["room"] == "pooja":
        state["warning"] = "⚠️ Avoid placing pooja above toilet."
    return state

# Step 4: Final response node returns everything
def final_response(state: VaasthuState) -> VaasthuState:
    if state["room"] == "pooja":
        state["response"] = "🛕 Best direction: Northeast."
        if state.get("warning"):
            state["response"] += f" {state['warning']}"
    else:
        state["response"] = f"Echo: {state['user_input']}"
    return state

# Step 5: Build the graph
graph_builder = StateGraph(VaasthuState)
graph_builder.add_node("classify", classify_room)
graph_builder.add_node("validate", validate_room)
graph_builder.add_node("respond", final_response)

graph_builder.set_entry_point("classify")
graph_builder.add_edge("classify", "validate")
graph_builder.add_edge("validate", "respond")
graph_builder.set_finish_point("respond")

graph = graph_builder.compile()

# Step 6: Run
if __name__ == "__main__":
    query = input("Ask a Vaasthu question: ")
    result = graph.invoke({"user_input": query})
    print(result["response"])
