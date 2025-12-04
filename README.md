# memory-extraction-module
# Companion AI Memory & Personality Engine

This project provides two main modules for building a personalized AI companion:
- **Memory Extraction**: Extracts structured user memories (preferences, emotional patterns, facts) from conversation history.
- **Personality Engine**: Rewrites AI responses in different conversational styles (personas) such as mentor, witty friend, or therapist.

## Features

- Extracts user preferences, emotional patterns, and facts from chat history using an LLM.
- Outputs memory in a structured JSON format ([see schema](memory_extraction_output_schema.txt)).
- Supports multiple AI reply styles: calm mentor, witty friend, therapist-style listener, and a neutral baseline.
- Uses Google Gemini API for all LLM tasks.

## File Overview

- [`memory_extractor.py`](memory_extractor.py): Extracts structured user memory from a list of user messages.
- [`personality_engine.py`](personality_engine.py): Rewrites responses in a chosen persona style or neutral tone.
- [`memory_extraction_output_schema.txt`](memory_extraction_output_schema.txt): Example schema for the memory extraction output.
- `readme`: This file.

## Requirements

- Python 3.8+
- `google-generativeai` Python package
- Google Gemini API key (set as `API_KEY` in your environment variables)

## Usage

### Memory Extraction

Run:
```sh
python memory_extractor.py
```
- Edits the `user_messages` list in the script to test with your own conversation history.
- Outputs a summary of extracted preferences, emotional patterns, and facts.

### Personality Engine

Run:
```sh
python personality_engine.py
```
- Enter your question at the prompt.
- Choose a persona style for the AI's reply.

## Customization

- Add or modify personas in the `PERSONAS` dictionary in [`personality_engine.py`](personality_engine.py).
- Adjust the memory schema in [`memory_extraction_output_schema.txt`](memory_extraction_output_schema.txt) as needed.


## Credits

- Uses Google Gemini LLM via the `google-generativeai` package.
