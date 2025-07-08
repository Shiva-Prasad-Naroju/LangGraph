from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# 1. Define the State structure
class EchoState(TypedDict):
    user_input: str
    output: Optional[str]

# 2. Create a simple node
def echo_node(state: EchoState) -> EchoState:
    user_input = state["user_input"]
    return {"output": f"You said: {user_input}"}

# 3. Build the graph
graph_builder = StateGraph(EchoState)
graph_builder.add_node("echo", echo_node)
graph_builder.set_entry_point("echo")
graph_builder.set_finish_point("echo")

# 4. Compile the graph
echo_graph = graph_builder.compile()

# 5. Run the graph
if __name__ == "__main__":
    result = echo_graph.invoke({"user_input": "Hello LangGraph!"})
    print(result)
