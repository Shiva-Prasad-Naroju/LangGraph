## 🧭 Multi-Branch Vaasthu Classifier (LangGraph)

This LangGraph example demonstrates a **multi-branch decision graph** that classifies and routes user queries related to Vaasthu elements like **kitchen**, **toilet**, **pooja room**, and more.

### ✅ What This Example Does

- Takes user input (a Vaasthu-related question)

- Uses keyword matching to classify the input into one of four categories:

  - `kitchen`

  - `toilet`

  - `pooja`

  - `general` (fallback)

- Routes to the appropriate node

- Responds with a relevant Vaasthu tip or fallback message

### ⚙️ Components Used

| Component                | Purpose                                                   |
|--------------------------|-----------------------------------------------------------|
| `TypedDict`              | Defines structured state with `user_input`, `response`    |
| `StateGraph`             | Core graph class from LangGraph                           |
| `add_node()`             | Adds nodes for logic execution                            |
| `set_entry_point()`      | Specifies starting node (`classify`)                      |
| `add_conditional_edges()`| Routes based on decision logic (`classify_decision`)      |
| `set_finish_point()`     | Marks end of execution for each path                      |
| `invoke()`               | Executes graph with input                                 |

### 🧠 How Routing Works

- A **classifier node** returns the state without modification.

- A **decision function** (`classify_decision`) checks for keywords:

  - `"kitchen"` → kitchen node

  - `"toilet"`, `"bathroom"`, `"washroom"` → toilet node

  - `"pooja"`, `"puja"`, `"temple"` → pooja node

  - anything else → general node

### 🧪 Example Inputs & Responses

| Input                                   | Routed To | Response                                                           |
|----------------------------------------|-----------|--------------------------------------------------------------------|
| `Where should I keep the kitchen?`     | kitchen   | ✅ Place the kitchen in the southeast.                             |
| `Is toilet in northeast good?`         | toilet    | 🚫 Avoid toilet in northeast.                                      |
| `Best direction for pooja room?`       | pooja     | 🛕 Place pooja room in the northeast.                              |
| `What’s your name?`                    | general   | ℹ️ Echo: What’s your name?                                         |

### 🚀 Sample Output

$ python main.py

Ask a Vaasthu question: Where can I place the pooja room?

🛕 Best to place pooja room in the northeast. Avoid above toilets.
