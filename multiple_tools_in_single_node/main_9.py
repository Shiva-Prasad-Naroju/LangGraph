from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    query_type: str
    answer: str
    raw_result: str

# ----- CLASSIFIER -----
def classify(state):
    if "remedy" in state["query"].lower():
        state["query_type"] = "remedy"
    else:
        state["query_type"] = "placement"
    return state

# ----- TOOL 1: Vaasthu Search Tool -----
def vaasthu_search_tool(query):
    if "kitchen" in query.lower():
        return "Place kitchen in southeast or east as per Vaasthu."
    return "Placement rule not found."

# ----- TOOL 2: Format Result -----
def format_response(raw):
    return f"✅ Vaasthu Guidance: {raw}"

# ----- MULTI-TOOL NODE -----
def placement_node(state):
    raw = vaasthu_search_tool(state["query"])
    final = format_response(raw)
    state["raw_result"] = raw
    state["answer"] = final
    return state

# ----- REMEDY TOOL -----
def remedy_node(state):
    state["answer"] = "🪔 Use a copper pyramid in the northwest."
    return state

# ----- OUTPUT -----
def output_node(state):
    print("✅ Final Answer:", state["answer"])
    return state

# ----- WRAP -----
graph = StateGraph(GraphState)
graph.set_entry_point("classify")

graph.add_node("classify", RunnableLambda(classify))
graph.add_node("placement_tools", RunnableLambda(placement_node))
graph.add_node("remedy_tool", RunnableLambda(remedy_node))
graph.add_node("output", RunnableLambda(output_node))

# ----- ROUTING -----
graph.add_conditional_edges(
    "classify",
    lambda s: s["query_type"],
    {
        "placement": "placement_tools",
        "remedy": "remedy_tool"
    }
)

graph.add_edge("placement_tools", "output")
graph.add_edge("remedy_tool", "output")
graph.add_edge("output", END)

app = graph.compile()

# ----- RUN TESTS -----
print("\n🔍 Test 1: Placement Query")
app.invoke({"query": "Where to place kitchen?"})

print("\n🔍 Test 2: Remedy Query")
app.invoke({"query": "What is the remedy for wrong direction?"})
