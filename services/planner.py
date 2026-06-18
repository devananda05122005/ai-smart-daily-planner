import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def optimize_schedule(tasks, free_time, peak_hours, fixed_tasks):
    try:
        prompt = f"""
You are an advanced AI productivity planner.
Generate a COMPLETE and realistic schedule based on the input data.

User Tasks:
{json.dumps(tasks, indent=2)}

Available Free Time Blocks:
{json.dumps(free_time, indent=2)}

Peak Focus Hours:
{json.dumps(peak_hours, indent=2)}

Fixed Tasks:
{json.dumps(fixed_tasks, indent=2)}

STRICT RULES:
1. Schedule ALL tasks.
2. Every task must have: name, deadline, duration, start_time, end_time.
3. Add breaks between long tasks with start_time, end_time, and reason.
4. Create focus blocks.
5. Use only the given free time slots. Respect fixed tasks.
6. If overloaded, mark postponed tasks.
7. Return exactly a single JSON object matching the schema below.

Expected Schema Structure:
{{
    "optimized_schedule": [
        {{
            "name": "Task Name",
            "deadline": "7 PM",
            "duration": "2 hours",
            "start_time": "4 PM",
            "end_time": "6 PM"
        }}
    ],
    "priority_order": ["Task Name"],
    "focus_blocks": [
        {{
            "name": "Deep Work Block",
            "start_time": "4 PM",
            "end_time": "6 PM"
        }}
    ],
    "break_suggestions": [
        {{
            "start_time": "6 PM",
            "end_time": "6:30 PM",
            "reason": "Rest"
        }}
    ],
    "overload_detected": false,
    "postponed_tasks": [],
    "focus_score_prediction": "85%",
    "productivity_score": "9/10",
    "reasoning": ["Reason 1"]
}}
"""

        # Using native JSON mode for deterministic structure matching
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result_text = response.choices[0].message.content.strip()
        parsed = json.loads(result_text)

        # Fallback values validation block
        if not parsed.get("optimized_schedule"):
            parsed["optimized_schedule"] = tasks

        if not parsed.get("priority_order"):
            parsed["priority_order"] = [task.get("name", "Unnamed Task") for task in tasks]

        if not parsed.get("focus_blocks"):
            parsed["focus_blocks"] = [{
                "name": "Focus Session",
                "start_time": free_time[0] if free_time else "N/A",
                "end_time": free_time[-1] if free_time else "N/A"
            }]

        if not parsed.get("break_suggestions"):
            parsed["break_suggestions"] = [{
                "start_time": "After tasks",
                "end_time": "15 mins later",
                "reason": "Regain mental energy"
            }]

        parsed.setdefault("overload_detected", False)
        parsed.setdefault("postponed_tasks", [])
        parsed.setdefault("focus_score_prediction", "80%")
        parsed.setdefault("productivity_score", "8/10")
        parsed.setdefault("reasoning", ["Schedule automatically balanced by priority criteria."])

        return parsed

    except Exception as e:
        return {"error": f"Optimization engine failure: {str(e)}"}