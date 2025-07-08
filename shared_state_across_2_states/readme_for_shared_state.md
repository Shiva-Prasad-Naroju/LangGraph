# 🧠 LangGraph - Shared State Across 2 Nodes (Vaasthu Example)

This example demonstrates how to **pass and update shared state** across multiple nodes in a LangGraph flow.

## 📌 Objective

To simulate a Vaasthu assistant that:

- Classifies user queries (e.g., kitchen, pooja)

- Performs validation (e.g., avoid pooja above toilet)

- Constructs a final response combining insights from all nodes


## 📂 File: `main_4.py`

### 🔧 Tech Stack

- `LangGraph` for graph-based flow logic

- `TypedDict` for clean state type enforcement

- Multi-node graph using shared memory (state)


## 🧩 Components

### 1. **State Structure**  

Defined using `TypedDict` with:

- `user_input` – raw query from user

- `room` – classified room type (`pooja`, `kitchen`, etc.)

- `warning` – any alerts/flags

- `response` – final message to return

### 2. **Graph Nodes**

- `classify_room` – identifies which room is being asked

- `validate_room` – adds warning if room placement violates Vaasthu

- `final_response` – builds full response using room + warning


## 🔄 Graph Flow

[ classify_room ]

       ↓

[ validate_room ]

       ↓

[ final_response ]

       ↓

    [ END ]
