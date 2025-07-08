from langgraph.graph import StateGraph
from typing import TypedDict, Optional

# 1. Define state type
class VaasthuState(TypedDict):
    user_input: str
    response: Optional[str]

# 2. Decision function: returns string (used only for routing)
def classify_decision(state: VaasthuState) -> str:
    text = state["user_input"].lower()
    if "kitchen" in text:
        return "kitchen"
    return "general"

# 3. Classify node: MUST return dict (even if empty)
def classify_node(state: VaasthuState) -> VaasthuState:
    # This node doesn't need to modify state, just return it as-is
    return state

# 4. Kitchen response
def kitchen_node(state: VaasthuState) -> VaasthuState:
    return {"response": "✅ Vaasthu Tip: Place the kitchen in the southeast."}

# 5. General fallback
def general_node(state: VaasthuState) -> VaasthuState:
    return {"response": f"Echo: {state['user_input']}"}

# 6. Build the graph
builder = StateGraph(VaasthuState)
builder.add_node("classify", classify_node)  # Node function (returns dict)
builder.add_node("kitchen", kitchen_node)
builder.add_node("general", general_node)

builder.set_entry_point("classify")

# 7. Routing: use separate decision function
builder.add_conditional_edges(
    "classify",
    classify_decision,  # Decision function (returns string)
    {
        "kitchen": "kitchen",
        "general": "general"
    }
)

builder.set_finish_point("kitchen")
builder.set_finish_point("general")

graph = builder.compile()

# 8. Run it
if __name__ == "__main__":
    query = input("Ask a Vaasthu question: ")
    result = graph.invoke({"user_input": query})
    print(result["response"])