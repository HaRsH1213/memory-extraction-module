import os
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

import google.generativeai as gemini

gemini.configure(api_key=os.environ["API_KEY"])


class GeminiLLM:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = gemini.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()


@dataclass
class Memory:
    user_preferences: List[Dict[str, Any]]
    user_emotional_patterns: List[Dict[str, Any]]
    user_facts: List[Dict[str, Any]]

    def to_json(self):
        return json.dumps(asdict(self), indent=2)



class MemoryExtractor:
    def __init__(self, llm: GeminiLLM, schema_path: str):
        self.llm = llm
        self.output_schema = self._read_prompt_file(schema_path)

    def _read_prompt_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise RuntimeError(f"Prompt file error: {e}")

    def extract(self, user_messages: List[str]) -> Memory:
        conversation = "\n".join(
            [f"{i}. {msg}" for i, msg in enumerate(user_messages)]
        )

    

        prompt = f"""
SYSTEM:
You are a memory extraction module for a companion AI.

Your ONLY job is to read the last 30 USER messages and extract:
1) User preferences
2) User emotional patterns
3) Stable facts about the user

RULES:
- Output MUST be valid JSON and match the provided {self.output_schema} exactly.
- Do NOT invent information.
- Only include items that are likely to remain useful for future conversations.
- If no information exists for a field, return an empty array [] for that field.
- Use 0–1 floating-point numbers for "confidence".
- "evidence_messages" are indexes of the messages you used (0-based).

USER MESSAGES (0 is oldest):
{conversation}

ASSISTANT:
Return ONLY JSON in this format:
'''
{{
  "user_preferences": [{{
      "id": "pref_001",
      "type": "content_style | topics | tools | schedule | misc",
      "statement": "User prefers concise, bullet-point answers.",
      "evidence_messages": [3, 7],
      "confidence": 0.88,
      "last_seen": "2025-12-01"
    }},...],
  "user_emotional_patterns": [ {{
      "id": "emo_001",
      "pattern": "User often feels anxious before interviews.",
      "triggers": ["upcoming interview", "job applications"],
      "typical_intensity": "medium",
      "preferred_support_style": "reassurance + concrete, step-by-step advice",
      "evidence_messages": [5, 12, 19],
      "confidence": 0.83
    }}, ...],
  "user_facts": [ {{
      "id": "fact_001",
      "category": "bio | work | study | health | relationships | misc",
      "statement": "User is a final-year computer science student.",
      "evidence_messages": [0],
      "confidence": 0.9,
      "last_seen": "2025-12-01"
    }}, ...]
}}

"""

        response = self.llm.generate(prompt)
        json_str = self._extract_json(response)
        data = json.loads(json_str)

        return Memory(
            user_preferences=data.get("user_preferences", []),
            user_emotional_patterns=data.get("user_emotional_patterns", []),
            user_facts=data.get("user_facts", []),
        )

    @staticmethod
    def _extract_json(text: str) -> str:
        if not text.strip():
            raise ValueError("Empty LLM response")

        if text.startswith("```"):
            lines = text.splitlines()[1:-1]
            text = "\n".join(lines).strip()

        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("JSON not found in LLM output")

        return text[start:end + 1]
    def build_memory_summary(self,memory: Memory) -> str:
        prefs = [p["statement"] for p in memory.user_preferences]
        emos = [e["pattern"] for e in memory.user_emotional_patterns]
        facts = [f["statement"] for f in memory.user_facts]

        parts = []
        if prefs:
            parts.append("Preferences: " + "; ".join(prefs[:3]))
        if emos:
            parts.append("Emotional patterns: " + "; ".join(emos[:2]))
        if facts:
            parts.append("Facts: " + "; ".join(facts[:3]))
        return "\n".join(parts)


if __name__ == "__main__":
    user_messages = [
        "I have an interview tomorrow and I'm really nervous.",
        "Please keep answers short and clear with examples.",
        "I like learning new tech skills and going to the gym.",
        "I'm a computer science student applying for ML roles."
    ]

    llm = GeminiLLM()
    extractor = MemoryExtractor(
        llm,
        r"memory_extraction_output_schema.txt" 
    )

    memory = extractor.extract(user_messages)
    response = extractor.build_memory_summary(memory)
    print("\n========== MEMORY Extractor ==========")
    print(response)

