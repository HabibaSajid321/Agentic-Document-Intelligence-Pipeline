
# # scripts/modules/text_extraction.py
# import fitz
# import pdfplumber
# from pathlib import Path
# import os

# # --- Use same path logic as spec_retrieval.py ---
# # __file__ = .../scripts/modules/text_extraction.py
# # .parent = .../scripts/modules
# # .parent.parent = .../DocBuilder (project root)
# BASE_DIR = Path(__file__).parent.parent.parent
# SPEC_FOLDER = BASE_DIR / "data" / "specs"
# OUTPUT_IMAGES_DIR = BASE_DIR / "output" / "images"

# # Ensure output dir exists
# OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# # Find all PDFs
# pdf_files = list(SPEC_FOLDER.glob("*.pdf"))

# if not pdf_files:
#     print(f" No PDFs found in {SPEC_FOLDER}")
#     exit(1)

# print(f" Found {len(pdf_files)} PDF(s) in {SPEC_FOLDER}")

# for pdf_path in pdf_files:
#     print(f"\n Processing: {pdf_path.name}")

#     # === 1. Extract full text with fitz ===
#     print("=== FULL TEXT (First 500 chars) ===")
#     try:
#         doc = fitz.open(pdf_path)
#         text = "".join(page.get_text() for page in doc)
#         doc.close()
#         print(text[:500].strip() or "(No text found)")
#     except Exception as e:
#         print(f"Text extraction failed: {e}")

#     # === 2. Extract tables with pdfplumber ===
#     print("\n=== TABLES (first 3 rows of each large table) ===")
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for i, page in enumerate(pdf.pages):
#                 tables = page.extract_tables()
#                 for table_idx, table in enumerate(tables):
#                     if table and len(table) > 3:  # Only show tables with >3 rows
#                         print(f"→ Table {table_idx + 1} on page {i + 1}")
#                         for row in table[:3]:
#                             print(row)
#     except Exception as e:
#         print(f"Table extraction failed: {e}")

#     # === 3. Extract images ===
#     print("\n=== IMAGES ===")
#     try:
#         doc = fitz.open(pdf_path)
#         image_count = 0
#         for page_num, page in enumerate(doc):
#             image_list = page.get_images()
#             for img_index, img in enumerate(image_list):
#                 xref = img[0]
#                 pix = fitz.Pixmap(doc, xref)
#                 if pix.n - pix.alpha < 4:  # Skip CMYK
#                     img_path = OUTPUT_IMAGES_DIR / f"{pdf_path.stem}_p{page_num}_img{img_index}.png"
#                     pix.save(str(img_path))
#                     print(f"Saved: {img_path.name}")
#                     image_count += 1
#                 pix = None
#         doc.close()
#         if image_count == 0:
#             print("(No images extracted)")
#     except Exception as e:
#         print(f" Image extraction failed: {e}")

# print(f"\n All done! Images saved to: {OUTPUT_IMAGES_DIR}")



# scripts/modules/text_extraction.py
import fitz
import pdfplumber
import os
from pathlib import Path
from typing import Dict, List, Any

def parse_pdf_comprehensive(pdf_path: str) -> Dict[str, Any]:
    """
    Parse a single PDF and return full text, structured tables, and image paths.
    Does NOT handle file discovery — that's the caller's job.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Ensure output/images exists (relative to CWD, but safe)
    image_dir = Path("output") / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    # --- 1. Extract Full Text ---
    full_text = ""
    try:
        doc = fitz.open(pdf_path)
        full_text = "".join(page.get_text() for page in doc)
        doc.close()
    except Exception as e:
        print(f"⚠️  Text extraction failed for {pdf_path.name}: {e}")

    # --- 2. Extract Structured Tables ---
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                for table in page.extract_tables():
                    if not table or len(table) < 3:
                        continue
                    headers = ["barrier_number", "type", "width_ft", "concrete_inch", "additional_required", "comments"]
                    for row in table:
                        if not row or not row[0]:
                            continue
                        first_cell = str(row[0]).strip()
                        if first_cell.isdigit():
                            clean_row = {}
                            for i, key in enumerate(headers):
                                val = row[i] if i < len(row) else ""
                                clean_row[key] = str(val).strip() if val else ""
                            tables.append({"page": page_num, "data": clean_row})
    except Exception as e:
        print(f"⚠️  Table extraction failed for {pdf_path.name}: {e}")

    # --- 3. Extract Images ---
    image_refs = []
    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc):
            for img_idx, img in enumerate(page.get_images()):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:  # Skip CMYK
                    img_name = f"{pdf_path.stem}_p{page_num}_img{img_idx}.png"
                    img_path = image_dir / img_name
                    pix.save(str(img_path))
                    image_refs.append({"page": page_num, "path": str(img_path)})
                pix = None
        doc.close()
    except Exception as e:
        print(f"⚠️  Image extraction failed for {pdf_path.name}: {e}")

    return {
        "full_text": full_text,
        "tables": tables,
        "images": image_refs
    }


# --- Optional: Direct test mode ---
if __name__ == "__main__":
    # Same logic as main.py's auto mode
    BASE_DIR = Path(__file__).parent.parent.parent
    spec_folder = BASE_DIR / "data" / "specs"
    pdfs = list(spec_folder.glob("*.pdf"))
    if not pdfs:
        print(f" No PDFs in {spec_folder}")
        exit(1)
    for p in pdfs:
        result = parse_pdf_comprehensive(p)
        print(f"Parsed {p.name}: {len(result['tables'])} table rows, {len(result['images'])} images")