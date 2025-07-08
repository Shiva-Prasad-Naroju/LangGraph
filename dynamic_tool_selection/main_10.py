from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    selected_tool: str
    answer: str

# ----- TOOL SELECTOR -----
def tool_selector_node(state):
    query = state["query"].lower()
    if "remedy" in query:
        state["selected_tool"] = "remedy"
    elif "place" in query or "kitchen" in query:
        state["selected_tool"] = "placement"
    else:
        state["selected_tool"] = "general"
    return state

# ----- TOOL 1: Placement -----
def vaasthu_search_tool(state):
    state["answer"] = "📍 Place kitchen in southeast or east as per Vaasthu."
    return state

# ----- TOOL 2: Remedy -----
def remedy_tool(state):
    state["answer"] = "🪔 Use copper pyramid in northwest as remedy."
    return state

# ----- TOOL 3: General -----
def general_tool(state):
    state["answer"] = "ℹ️ I can help with Vaasthu placement or remedies. Please ask specifically."
    return state

# ----- OUTPUT -----
def output_node(state):
    print("✅ Final Answer:", state["answer"])
    return state

# ----- WRAP ALL -----
selector = RunnableLambda(tool_selector_node)
placement_node = RunnableLambda(vaasthu_search_tool)
remedy_node = RunnableLambda(remedy_tool)
general_node = RunnableLambda(general_tool)
output = RunnableLambda(output_node)

# ----- BUILD GRAPH -----
graph = StateGraph(GraphState)
graph.set_entry_point("selector")

graph.add_node("selector", selector)
graph.add_node("placement", placement_node)
graph.add_node("remedy", remedy_node)
graph.add_node("general", general_node)
graph.add_node("output", output)

# ----- CONDITIONAL EDGE -----
graph.add_conditional_edges(
    "selector",
    lambda s: s["selected_tool"],
    {
        "placement": "placement",
        "remedy": "remedy",
        "general": "general"
    }
)

# ----- FINAL EDGES -----
graph.add_edge("placement", "output")
graph.add_edge("remedy", "output")
graph.add_edge("general", "output")
graph.add_edge("output", END)

app = graph.compile()

# ----- TEST RUNS -----
# print("\n🧪 Test: Placement Query")
# app.invoke({"query": "Where should I place my kitchen?"})

print("\n🧪 Test: Remedy Query")
app.invoke({"query": "What is the remedy for northwest toilet?"})

# print("\n🧪 Test: General Query")
# app.invoke({"query": "Tell me something about Vaasthu."})
