from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# ----- STATE -----
class GraphState(dict):
    query: str
    query_type: str
    answer: str

# ----- CLASSIFIER NODE -----
def classify(state):
    query = state["query"].lower()
    if "remedy" in query:
        state["query_type"] = "remedy"
    else:
        state["query_type"] = "placement"
    return state

# ----- TOOL 1: Vaasthu Qdrant-Like Tool -----
def vaasthu_search_tool(state):
    query = state["query"].lower()
    # Mocked Qdrant response
    if "kitchen" in query:
        state["answer"] = "🏠 Place kitchen in southeast or east for best energy flow."
    else:
        state["answer"] = "📍 Placement rules depend on the element; try asking about kitchen, bedroom, etc."
    return state

# ----- TOOL 2: Remedy Tool -----
def remedy_tool(state):
    # Mocked remedy response
    state["answer"] = "🪔 Use a copper pyramid in the northwest to correct placement."
    return state

# ----- OUTPUT NODE -----
def return_output(state):
    print("✅ Final Answer:", state["answer"])
    return state

# ----- WRAP TOOLS -----
classifier_node = RunnableLambda(classify)
placement_tool = RunnableLambda(vaasthu_search_tool)
remedy_tool_node = RunnableLambda(remedy_tool)
output_node = RunnableLambda(return_output)

# ----- GRAPH -----
graph = StateGraph(GraphState)
graph.set_entry_point("classify")

graph.add_node("classify", classifier_node)
graph.add_node("placement_tool", placement_tool)
graph.add_node("remedy_tool", remedy_tool_node)
graph.add_node("output", output_node)

# ----- CONDITIONAL ROUTING -----
graph.add_conditional_edges(
    "classify",
    lambda state: state["query_type"],
    {
        "placement": "placement_tool",
        "remedy": "remedy_tool"        
    }
)

graph.add_edge("placement_tool", "output")
graph.add_edge("remedy_tool", "output")
graph.add_edge("output", END)

app = graph.compile()

# ----- RUN TESTS -----
print("\n🔍 Test: Placement Query")
app.invoke({"query": "Where should I place my kitchen?"})

print("\n🔍 Test: Remedy Query")
app.invoke({"query": "What is the remedy for staircase in northwest?"})
