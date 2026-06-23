# # scripts/list_fields.py
# from PyPDF2 import PdfReader
# from pathlib import Path

# TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
# PDF_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"

# pdf = PdfReader(PDF_FILE)
# fields = pdf.get_fields()

# for name in fields:
#     print(name)


# """
# PDF Form Field Inspector
# This script lists all fillable fields in a PDF form
# """
# import json
# from pathlib import Path
# from pypdf import PdfReader

# def inspect_pdf_fields(pdf_path):
#     """Extract and display all form field names from a PDF"""
#     reader = PdfReader(pdf_path)
    
#     all_fields = {}
    
#     # Check each page for fields
#     for page_num, page in enumerate(reader.pages, start=1):
#         if "/Annots" in page:
#             for annot in page["/Annots"]:
#                 obj = annot.get_object()
#                 if obj.get("/T"):
#                     field_name = obj.get("/T")
#                     field_type = obj.get("/FT", "Unknown")
#                     field_value = obj.get("/V", "")
                    
#                     all_fields[field_name] = {
#                         "page": page_num,
#                         "type": str(field_type),
#                         "current_value": str(field_value)
#                     }
    
#     # Also try to get fields from the form
#     if reader.get_fields():
#         for field_name, field_info in reader.get_fields().items():
#             if field_name not in all_fields:
#                 all_fields[field_name] = {
#                     "page": "Multiple/Unknown",
#                     "type": field_info.get("/FT", "Unknown"),
#                     "current_value": field_info.get("/V", "")
#                 }
    
#     return all_fields

# def main():
#     # Setup paths
#     SCRIPT_DIR = Path(__file__).parent
#     ROOT_DIR = SCRIPT_DIR.parent
#     TEMPLATE_DIR = ROOT_DIR / "templates"
#     OUTPUT_DIR = ROOT_DIR / "output"
    
#     TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
#     OUTPUT_JSON = OUTPUT_DIR / "pdf_fields.json"
    
#     OUTPUT_DIR.mkdir(exist_ok=True)
    
#     print("=" * 70)
#     print("PDF FORM FIELD INSPECTOR")
#     print("=" * 70)
#     print(f"Inspecting: {TEMPLATE_FILE}\n")
    
#     if not TEMPLATE_FILE.exists():
#         print(f"❌ Template PDF not found: {TEMPLATE_FILE}")
#         return
    
#     # Extract fields
#     fields = inspect_pdf_fields(TEMPLATE_FILE)
    
#     if not fields:
#         print("❌ No fillable fields found in this PDF!")
#         print("   This PDF might not have interactive form fields.")
#         return
    
#     # Display results
#     print(f"✅ Found {len(fields)} fillable fields:\n")
#     print("-" * 70)
    
#     for i, (field_name, info) in enumerate(sorted(fields.items()), start=1):
#         print(f"{i}. Field Name: '{field_name}'")
#         print(f"   Page: {info['page']}")
#         print(f"   Type: {info['type']}")
#         if info['current_value']:
#             print(f"   Current Value: {info['current_value']}")
#         print()
    
#     # Save to JSON
#     with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
#         json.dump(fields, f, indent=2, ensure_ascii=False)
    
#     print("-" * 70)
#     print(f"✅ Field list saved to: {OUTPUT_JSON}")
#     print("\nUse these exact field names in your fill_form.py script!")

# if __name__ == "__main__":
#     main()




# from pypdf import PdfReader
# reader = PdfReader("doc\highlighted_pdf.pdf")
# fields = reader.get_fields()
# print("Real form?" if fields else "Static PDF")



from pypdf import PdfReader

reader = PdfReader(r"doc\highlighted_pdf.pdf")
fields = reader.get_fields()

if fields:
    print("This is an AcroForm PDF with the following fields:")
    for field_name, field_data in fields.items():
        print(f"  - {field_name}: {field_data.get('/FT', 'Unknown type')}")
else:
    print("This is a static PDF (no form fields)")