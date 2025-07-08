## 🗣️ Echo Graph (LangGraph Basics)

This is a **minimal example** demonstrating how to use **LangGraph** to build a simple single-node graph that echoes user input.

### ✅ What This Example Does

- Accepts a `user_input` string  
- Passes it through a graph node  
- Returns a response like:  
  `You said: <user_input>`

### ⚙️ Components Used

| Component            | Purpose                                      |
|----------------------|----------------------------------------------|
| `TypedDict`          | Defines a structured state for the graph     |
| `StateGraph`         | Manages graph creation and compilation       |
| `add_node()`         | Adds a functional node (`echo`)              |
| `set_entry_point()`  | Defines the graph's entry node               |
| `set_finish_point()` | Defines the graph's exit node                |
| `invoke()`           | Executes the graph with user input           |


### 🧠 Key Concept

This file helps you understand the **core structure of LangGraph**:
- Define a shared state schema  
- Add one or more nodes (steps)  
- Set entry and finish points  
- Compile and run the graph

It's the **hello world** of LangGraph development.

### 🚀 Example Output

$ python main.py

{'user_input': 'Hello LangGraph!', 'output': 'You said: Hello LangGraph!'}
