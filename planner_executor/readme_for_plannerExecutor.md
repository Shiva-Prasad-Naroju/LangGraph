# LangGraph: Planner → Executor Agent Pattern

This example demonstrates how to build a **Planner–Executor architecture** using LangGraph — a foundational pattern for agentic systems like AutoGPT, ReAct, and tool-using agents.

## 💡 Why It Matters

This is the core architecture behind agentic workflows:

- LLM plans multiple steps (Planner)

- Each step is executed one by one (Executor)

- Can loop until goal is achieved

✅ Think: like AutoGPT, but controlled.



## 🧩 Components

| Node        | Description                                      |
|-------------|--------------------------------------------------|
| `planner`   | Creates a list of steps based on the query       |
| `executor`  | Executes each step sequentially (in a loop)      |
| `output`    | Compiles and returns the final answer            |


## 🔧 Features Demonstrated

- ✅ Shared state between nodes  


- ✅ Looping with conditional edge (step_index logic)  

- ✅ Agent-like behavior with step-by-step execution  

- ✅ Clean planner–executor separation  







