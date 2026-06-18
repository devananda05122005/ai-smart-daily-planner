# AI Smart Daily Planner 📅🤖

An AI-powered daily schedule optimization engine that takes an unstructured list of tasks, available open time slots, and peak focus hours to construct a realistic, balanced, and overload-protected daily agenda. 

Built with **FastAPI**, **Pydantic v2 data layers**, and **Groq (`llama-3.1-8b-instant`)** leveraging native structural streaming tokens.

---

## 🔥 Key Architectural Features

* **Deterministic Data Integrity:** Leverages modern Pydantic schema validation to catch malformed front-end inputs before hitting the scheduling layer.
* **Hardened Native JSON Mode:** Utilizes Groq structural execution parameters (`response_format={"type": "json_object"}`), entirely eliminating raw string regex parsing or LLM format hallucinations.
* **Cognitive Energy Balancing:** The engine matches incoming task priorities (`High`, `Medium`, `Low`) directly against the user's defined peak focus blocks.
* **Proactive Burnout Prevention:** Automatically injects calculated break windows between high-duration or intense cognitive task sprints.
* **Overflow Failure Protection:** Intelligently identifies when total task duration outstrips total available free time, flagging overload states and identifying tasks to postpone.

---

## 🛠️ Project Directory Structure

```text
AI-SMART-DAILY-PLANNER/
│
├── models/
│   └── request.py       # Pydantic data contract models
│
├── services/
│   └── planner.py       # Groq AI structural optimization engine
│
├── static/              # UI Presentation Tier
│   ├── index.html       # Client interface view 
│   ├── style.css        # Responsive layout components
│   └── script.js        # Async UI Event Orchestrator
│
├── .env                 # Local secrets configuration (Ignored by Git)
├── .gitignore           # Smart rule file patterns for runtime exclusion
└── main.py              # FastAPI application gateway instance