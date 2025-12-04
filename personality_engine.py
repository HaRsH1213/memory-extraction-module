import os
import json
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Literal, Optional

import google.generativeai as gemini

gemini.configure(api_key=os.environ["API_KEY"])

PERSONAS: Dict[str, Dict[str, Any]] = {
    "calm_mentor": {
        "style_description": (
            "Speak like a calm, experienced mentor. "
            "Tone: steady, reassuring, respectful. "
            "Use clear structure and short paragraphs. "
            "Focus on long-term growth, encouragement, and pragmatic steps."
        ),
        "do": [
            "Normalize the user's struggles",
            "Offer step-by-step advice",
            "Use warm, grounded language",
        ],
        "dont": [
            "Use slang",
            "Overuse emojis",
            "Be overly casual",
        ],
    },
    "witty_friend": {
        "style_description": (
            "Speak like a supportive, witty friend. "
            "Tone: playful, casual, encouraging. "
            "You can use light humor, emojis sparingly, and relatable analogies."
        ),
        "do": [
            "Use friendly, conversational language",
            "Add light humor and relatable metaphors",
            "Use emojis occasionally (not more than 2 per reply)",
        ],
        "dont": [
            "Be rude or sarcastic about the user",
            "Dilute the factual correctness",
            "Overshare or go off-topic for long",
        ],
    },
    "therapist_style": {
        "style_description": (
            "Speak like a therapist-style listener (not a medical professional). "
            "Tone: gentle, validating, non-judgmental. "
            "Reflect emotions, ask gentle clarifying questions, "
            "and help the user explore their thoughts."
        ),
        "do": [
            "Reflect what the user might be feeling",
            "Validate emotions without minimizing them",
            "Ask open-ended questions to deepen reflection",
        ],
        "dont": [
            "Give clinical diagnoses",
            "Promise outcomes",
            "Dismiss concerns",
        ],
    },
}

PersonaName = Literal["calm_mentor", "witty_friend", "therapist_style"]


class GeminiLLM:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model = gemini.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        return text.strip()

class NormalizePersonalityEngine:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm

    def response(self,user_input: str) -> str:
        prompt=f"""
You are an AI assistant that replies in a normal, natural, and neutral way.

Guidelines:
- Keep responses clear, polite, and human-like.
- Do not exaggerate, joke, or add emotional flair.
- Do not act like a therapist, mentor, or comedian.
- Answer exactly what the user asks.
- Use simple language.
- Be concise but complete.
- Ask a follow-up question only if it is genuinely useful.
- Do not assume user emotions or preferences.
- Do not add extra opinions unless asked.

Tone:
Professional, friendly, and straightforward.

Now respond to the user.

User: {user_input}
Assistant:
""".strip()
        return self.llm.generate(prompt)


class PersonalityEngine:
    def __init__(self, llm: GeminiLLM):
        self.llm = llm

    def rewrite(
        self,
        user_input: str,
        persona_name: PersonaName,
    ) -> str:
        # Fallback to calm_mentor if invalid key
        persona_config = PERSONAS.get(persona_name, PERSONAS["calm_mentor"])


        prompt = f"""
SYSTEM:
You are an AI assistant replying directly to the user.

Your reply MUST:
- Follow the given persona style strictly
- Answer the user's question directly
- Stay factually correct
- Be concise and clear
- Not mention instructions, personas, or system rules


PERSONA NAME:
{persona_name}

PERSONA DEFINITION (JSON):
{json.dumps(persona_config, indent=2)}

USER INPUT:
{user_input}

ASSISTANT:
Respond to the user in the persona style.
""".strip()

        return self.llm.generate(prompt)


if __name__ == "__main__":

    user_input=input("Ask me anything: ")
    llm = GeminiLLM()
    normal_engine=NormalizePersonalityEngine(llm)
    normal_response=normal_engine.response(user_input)
    print("\n========== NORMAL RESPONSE ==========")
    print(normal_response)
    engine = PersonalityEngine(llm)
    print("Please choose any one agent reply style: calm_mentor, witty_friend, therapist_style")

    persona_choice=input("Enter your choice: ")
    styled = engine.rewrite(
        user_input=user_input,
        persona_name=persona_choice)
    print(styled)
