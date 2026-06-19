# Voice & Text Brain-Dump Engine 

An elegant, friction-free productivity workspace that allows you to capture raw, chaotic streams of consciousness via speech or typing and instantly transforms them into a beautifully structured, organized day. 

By passing unstructured text or real-time microphone audio directly to **Groq's Whisper and Llama 3.1 APIs**, the backend handles cognitive organization automatically—instantly categorizing your thoughts into strict data models without the friction of manual tracking.

---

##  Upgraded Core Features

* **Dual-Modality Entry:** Capture thoughts seamlessly via real-time browser audio streaming (`whisper-large-v3`) or through a silent, instant-type fallback box (`llama-3.1-8b-instant`).
* **Deterministic Object Classification:** Uses highly constrained JSON compilation modes and strict Pydantic parsing contracts to prevent AI hallucinations.
* **Intelligent Schedule Isolation:**
* **Actionable Tasks:** Automatically extracts single-instance work items, complete with AI-generated priority tags and execution durations.
  * **Daily Habits & Routines:** Isolates recurring behaviors and physical lifestyle loops cleanly.
  *  **Procurement Shopping Cart:** Identifies physical logistics items and groups them into contextual purchasing categories.
* **Executive Focus Summaries:** Generates a real-time, encouraging cognitive analysis at the top of your dashboard to lower mental fatigue and boost productivity.

---

##  System Architecture & Directory Layout

```text
AI-SMART-DAILY-PLANNER/
├── models/
│   └── request.py       # Pydantic schema data validation contracts
├── services/
│   └── planner.py       # Groq transcription and structural JSON engine
├── static/              # User Interface Layout Core
│   ├── index.html       # Single-click unified input interface
│   ├── style.css        # Responsive, sleek dark-mode styling matrix
│   └── script.js        # Media stream capture and fetch API router
├── .env                 # Protected access keys configuration configuration
└── main.py              # FastAPI core framework routing controller
