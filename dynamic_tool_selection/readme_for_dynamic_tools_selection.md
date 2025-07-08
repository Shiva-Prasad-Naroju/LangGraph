# 🧭 LangGraph Tutorial – Dynamic Tool Selection (Tool Router Pattern)

Instead of routing manually with if/else logic (like conditional branching), you let a Tool Selector decide which tool to use at runtime based on the query.

## Graph Flow:

user_query → tool_selector → selected_tool → output


## 🧠 Goal

Build a LangGraph that:

- Uses a `tool_selector_node()` to dynamically choose the right tool

- Routes to:

  - `vaasthu_search_tool()` for placement queries

  - `remedy_tool()` for remedy-related queries

  - `general_tool()` for other inputs

- Then forwards result to output

## ⚙️ Dependencies

pip install langgraph




