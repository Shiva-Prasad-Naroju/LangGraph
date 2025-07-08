## 🏡 Vaasthu Classifier (LangGraph with Conditional Routing)

This example demonstrates how to use **LangGraph** with **conditional edges** to route Vaasthu-related user inputs based on keywords like `kitchen`.

### ✅ What This Example Does

- Accepts a Vaasthu-related query from the user  

- Uses a **decision function** to classify the query (e.g., `kitchen` or `general`)  

- Routes to the appropriate response node  

- Returns a customized Vaasthu tip or a general fallback

### ⚙️ Components Used

| Component                | Purpose                                                     |
|--------------------------|-------------------------------------------------------------|
| `TypedDict`              | Defines structured state with `user_input` and `response`   |
| `StateGraph`             | Core LangGraph object for defining node-based logic flow    |
| `add_node()`             | Adds logic nodes like `classify`, `kitchen`, `general`      |
| `set_entry_point()`      | Starts execution from the `classify` node                   |
| `add_conditional_edges()`| Uses a **decision function** to determine routing           |
| `set_finish_point()`     | Marks end of graph at either `kitchen` or `general`         |
| `invoke()`               | Executes graph with dynamic user input                      |


### 🧠 Key Concepts

- **Separation of logic**:  

  - `classify_node` handles node execution (returns dict)  

  - `classify_decision` handles routing (returns string)

- **Branching logic** with keyword matching allows dynamic and modular rule expansion

### 🧪 Example Queries

| Input                                 | Routed To   | Output                                     |
|--------------------------------------|-------------|---------------------------------------------|
| `Where should I build the kitchen?`  | `kitchen`   | ✅ Tip about southeast placement            |
| `Tell me something`                  | `general`   | Echoes the input                            |

### 🚀 Example Output

$ python main.py

Ask a Vaasthu question: Where to keep kitchen?

✅ Vaasthu Tip: Place the kitchen in the southeast.
