import os
from groq import Groq
from models.request import OrganizedBrainDump

# Initialize the Groq client securely from your environment variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_INSTRUCTION = (
    "You are an elite productivity and cognitive organization engine.\n"
    "Your job is to parse a chaotic, raw stream-of-consciousness input "
    "and organize it perfectly into a raw JSON object.\n\n"
    "CRITICAL: You MUST use the exact key names specified below. Do not use camelCase or make up your own keys.\n\n"
    "REQUIRED JSON STRUCTURE AND EXACT KEYS:\n"
    "{\n"
    '  "tasks": [\n'
    '    {"title": "string", "priority": "High, Medium, or Low", "estimated_minutes": integer}\n'
    '  ],\n'
    '  "habits": [\n'
    '    {"habit_name": "string", "frequency": "string"}\n'
    '  ],\n'
    '  "shopping_cart": [\n'
    '    {"item_name": "string", "category": "string"}\n'
    '  ],\n'
    '  "contextual_summary": "A brief, encouraging string summary here (MUST BE A STRING, NOT AN OBJECT)"\n'
    "}\n\n"
    "Do NOT include markdown syntax like ```json. Return ONLY the raw, verified JSON object structure."
)

def process_voice_brain_dump(audio_file_path: str) -> OrganizedBrainDump:
    """Ingests an audio file, transcribes it via Whisper, and structures it using Llama."""
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Target audio file at {audio_file_path} does not exist.")

    with open(audio_file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_file_path), file.read()),
            model="whisper-large-v3"
        )
    
    raw_text = transcription.text
    if not raw_text.strip():
        raise ValueError("Audio transcription returned empty text payload.")

    return process_text_brain_dump(raw_text)


def process_text_brain_dump(raw_text: str) -> OrganizedBrainDump:
    """Directly inputs a raw string into Llama 3.1 JSON mode and validates against Pydantic."""
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": f"Here is my raw brain-dump text:\n\"{raw_text}\""}
        ],
        response_format={"type": "json_object"},
        temperature=0.1  # Dropping temperature to 0.1 maximizes schema compliance stiffness
    )
    
    response_content = completion.choices[0].message.content.strip()
    
    # Defensive programming block: strip markdown backticks if model acts up
    if response_content.startswith("```"):
        response_content = response_content.strip("```").strip("json").strip()
        
    try:
        return OrganizedBrainDump.model_validate_json(response_content)
    except Exception as validation_error:
        print(f"--- FAILED RAW RESPONSE FROM LLM ---\n{response_content}\n----------------------------------")
        raise validation_error