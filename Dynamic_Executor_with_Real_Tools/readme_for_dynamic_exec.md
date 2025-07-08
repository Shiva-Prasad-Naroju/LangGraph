# 🤖 LangGraph – Dynamic Executor with Real Tools (Final Agent Loop)

This setup creates a **fully agentic LangGraph**:

- A `planner` creates a list of step names.

- An `executor` dynamically maps each step to a real tool.

- Loop continues until all steps are completed.

- Final response is returned via `output`.


## 🎯 Goal

Build a fully agentic loop:

- Planner creates dynamic steps like ["search", "remedy", "format"]

- Executor dynamically dispatches to the correct tool per step

- Loop continues until all steps are done

- Final answer is compiled

## 🧰 Tools You'll Include

- Step Name	        Tool Description
- search	    Simulates Qdrant/Vaasthu rule retrieval


- remedy	    Suggests remedies based on rule or direction

- format	    Formats all collected info into final answer

- (Optional)	Add your real functions instead of mocks

## Flow structure:

User Query

   ↓

Planner → ["search", "remedy", "format"]

   ↓

Loop over Executor:

    └── "search" → search_tool()

    └── "remedy" → remedy_tool()

    └── "format" → format_tool()

   ↓

Final Answer → Output
