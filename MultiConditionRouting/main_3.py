from langgraph.graph import StateGraph
from typing import TypedDict, Optional

# 1. Define state
class VaasthuState(TypedDict):
    user_input: str
    response: Optional[str]

# 2. Decision function: returns branch name (string)
def classify_decision(state: VaasthuState) -> str:
    text = state["user_input"].lower()
    if "kitchen" in text:
        return "kitchen"
    elif "toilet" in text or "bathroom" in text or "washroom" in text:
        return "toilet"
    elif "pooja" in text or "puja" in text or "temple" in text:
        return "pooja"
    else:
        return "general"

# 3. Classifier node: returns the state unchanged
def classify_node(state: VaasthuState) -> VaasthuState:
    return state

# 4. Kitchen response
def kitchen_node(state: VaasthuState) -> VaasthuState:
    return {"response": "✅ Vaasthu Tip: Place the kitchen in the southeast."}

# 5. Toilet response
def toilet_node(state: VaasthuState) -> VaasthuState:
    return {"response": "🚫 Avoid toilet in northeast. Prefer northwest or southeast."}

# 6. Pooja response
def pooja_node(state: VaasthuState) -> VaasthuState:
    return {"response": "🛕 Best to place pooja room in the northeast. Avoid above toilets."}

# 7. General fallback
def general_node(state: VaasthuState) -> VaasthuState:
    return {"response": f"ℹ️ Echo: {state['user_input']}"}

# 8. Build the graph
builder = StateGraph(VaasthuState)

builder.add_node("classify", classify_node)
builder.add_node("kitchen", kitchen_node)
builder.add_node("toilet", toilet_node)
builder.add_node("pooja", pooja_node)
builder.add_node("general", general_node)

builder.set_entry_point("classify")

# 9. Add conditional routing
builder.add_conditional_edges(
    "classify",
    classify_decision,
    {
        "kitchen": "kitchen",
        "toilet": "toilet",
        "pooja": "pooja",
        "general": "general"
    }
)

# 10. Set finish points
builder.set_finish_point("kitchen")
builder.set_finish_point("toilet")
builder.set_finish_point("pooja")
builder.set_finish_point("general")

# 11. Compile and run
graph = builder.compile()

if __name__ == "__main__":
    query = input("Ask a Vaasthu question: ")
    result = graph.invoke({"user_input": query})
    print(result["response"])
