from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# Define state schema
class GraphState(dict):
    query: str
    query_type: str
    answer: str

# 1. Classifier Node
def classify(state):
    query = state["query"]
    if "remedy" in query.lower():
        state["query_type"] = "remedy"
    else:
        state["query_type"] = "placement"
    return state

# 2. Placement Node
def handle_placement(state):
    state["answer"] = "🔧 Place kitchen in southeast as per Vaasthu."
    return state

# 3. Remedy Node
def handle_remedy(state):
    state["answer"] = "🪔 Use copper pyramid in northwest for correction."
    return state

# 4. Final Output Node
def return_output(state):
    print("✅ Final Answer:", state["answer"])
    return state

# Wrap all into RunnableLambda
classifier_node = RunnableLambda(classify)
placement_node = RunnableLambda(handle_placement)
remedy_node = RunnableLambda(handle_remedy)
output_node = RunnableLambda(return_output)

# Build the Graph
builder = StateGraph(GraphState)

builder.add_node("classify", classifier_node)
builder.add_node("placement", placement_node)
builder.add_node("remedy", remedy_node)
builder.add_node("output", output_node)

# Entry
builder.set_entry_point("classify")

# Conditional Routing
builder.add_conditional_edges(
    "classify",
    lambda state: state["query_type"],
    {
        "placement": "placement",
        "remedy": "remedy"
    }
)

# Routing to output
builder.add_edge("placement", "output")
builder.add_edge("remedy", "output")
builder.add_edge("output", END)

# Compile & Run
graph = builder.compile()

# Test Query
user_input = {"query": "What is the remedy for kitchen in northwest?"}
graph.invoke(user_input)
