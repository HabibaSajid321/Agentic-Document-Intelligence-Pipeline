# scripts/json_sanitizer.py
from modules.llm_client import query_llm

def vlm_to_json(vlm_description: str, page_number: int) -> dict:
    prompt = f"""
Convert this drawing description into valid JSON:

"{vlm_description}"

Output ONLY:
{{
  "page_number": {page_number},
  "rooms_with_lead_doors": [string],
  "room_numbers": [string],
  "lead_shielding_indicators": [string]
}}
"""
    return query_llm(prompt)