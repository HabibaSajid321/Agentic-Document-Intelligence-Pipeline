# scripts/main.py
import sys
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure 'scripts/' is in path so 'modules.x' works
SCRIPTS_DIR = Path(__file__).parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Import modules
from modules.text_extraction import parse_pdf_comprehensive
from modules.llm_client import query_llm
from modules.vlm_client import query_vlm
from modules.json_sanitizer import vlm_to_json


# --- VLM Prompt (Optimized for Shielding Plans) ---
VLM_PROMPT = """
You are a radiation shielding engineer analyzing a technical floor plan of a medical LINAC bunker.

Extract ONLY the following from the image:

1. **Barrier Labels & Specifications**:
   - List each barrier (e.g., "Barrier 1", "Barrier 3") and its shielding material/thickness as written.
   - Example: "Barrier 1: 3\" lead + 2\" BPE"
   - Include notes like "2-1/8\" lead"

2. **Room Labels**:
   - Identify: "TREATMENT", "CONTROL", "OFFICE", "CORRIDOR"

3. **Construction Notes**:
   - Extract text like "Install 147 lbs/ft² concrete..."

4. **Color Coding**:
   - Only if labeled (e.g., "blue = lead")

⚠️ DO NOT guess. If no text, skip it.
⚠️ Output ONLY a clean, factual one-paragraph description. No markdown.
"""


def analyze_image(img_info):
    """Helper for parallel VLM calls."""
    img_path = img_info["path"]
    page_num = img_info["page"]
    try:
        desc = query_vlm(img_path, VLM_PROMPT)
        return vlm_to_json(desc, page_num)
    except Exception as e:
        print(f"⚠️ VLM failed on {img_path}: {e}")
        return {"error": str(e), "image_path": img_path, "page": page_num}


def generate_human_summary_from_json(structured_data: dict) -> str:
    """Use LLM to turn structured JSON into readable summary."""
    try:
        context = json.dumps(structured_data, indent=2, ensure_ascii=False)
    except:
        context = str(structured_data)

    prompt = f"""
You are a radiation safety expert and technical writer.

Convert the following shielding analysis into a concise, professional, human-readable executive summary for architects and project managers.

Guidelines:
- Use headings: ## Key Updates, ## Barrier Summary, ## Door Specs, etc.
- Mention facility, LINAC model, and NCRP 151 compliance
- Highlight the Barrier 5 change (2" → 2-1/8" lead)
- Keep under 500 words
- Do NOT invent data
- Format in Markdown

Structured Data:
{context}
"""
    try:
        return query_llm(prompt)
    except Exception as e:
        return f"⚠️ Human summary generation failed: {e}"


def main(input_pdf: str):
    # --- Resolve paths relative to project root ---
    BASE_DIR = Path(__file__).parent.parent  # DocBuilder/
    OUTPUT_SPECS_DIR = BASE_DIR / "output" / "specs"
    OUTPUT_SPECS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"📄 Processing: {input_pdf}")
    pdf_path = Path(input_pdf)

    # Parse PDF
    try:
        data = parse_pdf_comprehensive(str(pdf_path))
    except Exception as e:
        print(f"❌ Failed to parse PDF: {e}")
        return

    # --- LLM: Structured JSON Summary ---
    table_str = json.dumps([t["data"] for t in data["tables"]], indent=2)
    summary_prompt = f"""
You are a radiation shielding physicist. Summarize the document.

Extract:
- facility_name: PAC Health Medical Center
- linac_model: Varian True Beam
- beam_energies_mv: [15 MV, 10 MV, 10 FFF, 6 MV, 6 FFF]
- primary_workload_gy_per_week: {{ "15_MV": 150, ... }}
- leakage_workload_gy_per_week: {{ "15_MV": 450, ... }}
- imrt_factor: 3
- patients_per_day: 45
- xray_head_leakage_percent: 0.1
- neutron_head_leakage_percent: 0.05
- revision_notes: "Barrier 5 lead increased from 2\" to 2-1/8\" due to occupancy change."
- door_shielding: {{
    "total_lead_thickness_inch": 1.0,
    "total_bpe_thickness_inch": 3.0,
    "steel_encasement_inch": 0.25,
    "construction": "¼” steel + ½” lead + 3” BPE + ½” lead + ¼” steel",
    "adjacent_wall_concrete_inch": 12
  }}
- barriers: list of objects with keys: barrier_number, type, existing_concrete_thickness_inch, additional_shielding_required, additional_shielding, comments
- key_assumptions: list of strings

Use this text:
{data['full_text'][:10000]}

And these tables:
{table_str}

Output ONLY valid JSON.
"""

    try:
        summary = query_llm(summary_prompt)
    except Exception as e:
        print(f"⚠️ LLM call failed: {e}")
        summary = {"error": str(e)}

    # --- VLM: Parallel Image Analysis ---
    drawing_results = []
    images = data["images"]
    if images:
        print(f"🖼️  Analyzing {len(images)} image(s) in parallel...")
        with ThreadPoolExecutor(max_workers=min(4, len(images))) as executor:
            future_to_img = {executor.submit(analyze_image, img): img for img in images}
            for future in as_completed(future_to_img):
                drawing_results.append(future.result())
    else:
        print("🖼️  No images to analyze.")

    # --- Final Structured Result ---
    result = {
        "input_pdf": pdf_path.name,
        "document_summary": summary,
        "drawing_analysis": drawing_results
    }

    # --- Save Structured JSON ---
    json_output_file = OUTPUT_SPECS_DIR / f"{pdf_path.stem}_stage1_results.json"
    with open(json_output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Structured JSON saved to: {json_output_file}")

    # --- Generate and Save Human Summary ---
    print("✍️ Generating human-readable summary...")
    human_text = generate_human_summary_from_json(result)
    human_output_file = OUTPUT_SPECS_DIR / f"{pdf_path.stem}_HUMAN_SUMMARY.md"
    with open(human_output_file, "w", encoding="utf-8") as f:
        f.write(human_text)
    print(f"📄 Human summary saved to: {human_output_file}")


# --- Batch Processing ---
def process_all_pdfs():
    BASE_DIR = Path(__file__).parent.parent
    spec_folder = BASE_DIR / "data" / "specs"
    pdf_files = list(spec_folder.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No PDFs found in {spec_folder}")
        return
    print(f"📁 Found {len(pdf_files)} PDF(s) in {spec_folder}")
    for pdf_path in pdf_files:
        main(str(pdf_path))


# --- CLI ---
if __name__ == "__main__":
    if len(sys.argv) == 2:
        pdf_path = sys.argv[1]
        if not Path(pdf_path).exists():
            print(f"❌ PDF not found: {pdf_path}")
            sys.exit(1)
        main(pdf_path)
    elif len(sys.argv) == 1:
        print("🔄 No PDF specified. Processing all PDFs in data/specs/...")
        process_all_pdfs()
    else:
        print("Usage:")
        print("  python scripts/main.py                    → Process all PDFs")
        print("  python scripts/main.py path/to/file.pdf   → Process single PDF")
        sys.exit(1)