# LangGraph for Beginners

This repository explores building intelligent agents using [LangGraph](https://github.com/vipinvsist/LangGraph#), demonstrating a range of architectures such as:

- Sequential agents  
- Conditional flows  
- ReAct agents  
- RAG-based agents  
- Drafting and memory-enhanced bots  

> 📊 Most agent folders contain `graph.png` and `graph_test.png` showing the LangGraph workflows.

This project is ideal for learning how to design, chain, and evaluate intelligent agents in modular steps.

---

## 🧠 Key Components

### Agents
Each folder (`agent_1/` to `agent5/`) contains:
- Agent implementation logic
- LangGraph visualizations (`graph.png`, `graph_test.png`)
- Test scripts for validating agent behavior

### Other Modules
- `chatbot/`: Implements memory and logging for conversational agents.
- `drafter/`: Drafting agent for automated writing/content generation.
- `rag/`: Retrieval-Augmented Generation with ChromaDB and persistent vector store.
- `react_agent/`: Simple ReAct agent based on reasoning and tool use.
- `simple_bot/`: A minimal chatbot using LangGraph state flows.

### Shared Utilities
- `type_annotations.py`: Common type hints shared across agent implementations.

---

## 🚀 Quick Start

To run a specific agent (e.g., `agent_1`):

```bash
cd agent_1
python agent_1.py
