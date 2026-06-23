# scripts/inspect_checkboxes.py
from pathlib import Path
from pypdf import PdfReader

def inspect_checkboxes():
    SCRIPT_DIR = Path(__file__).parent
    ROOT_DIR = SCRIPT_DIR.parent
    TEMPLATE_DIR = ROOT_DIR / "templates"
    TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
    
    reader = PdfReader(TEMPLATE_FILE)
    
    print("=" * 80)
    print("CHECKBOX FIELD INSPECTION")
    print("=" * 80)
    
    if "/AcroForm" not in reader.trailer["/Root"]:
        print("No AcroForm found in PDF")
        return
    
    acroform = reader.trailer["/Root"]["/AcroForm"]
    
    if "/Fields" not in acroform:
        print("No Fields found in AcroForm")
        return
    
    fields = acroform["/Fields"]
    checkbox_count = 0
    
    for field_ref in fields:
        field = field_ref.get_object()
        
        if "/T" not in field:
            continue
            
        field_name = str(field["/T"])
        field_type = str(field.get("/FT", "Unknown"))
        
        # Only inspect button fields (checkboxes/radio buttons)
        if field_type == "/Btn":
            checkbox_count += 1
            print(f"\n{'─' * 80}")
            print(f"Field Name: {field_name}")
            print(f"Field Type: {field_type}")
            
            # Get current value
            if "/V" in field:
                current_value = str(field["/V"])
                print(f"Current Value: {current_value}")
            else:
                print("Current Value: (not set)")
            
            # Get appearance states
            if "/AP" in field:
                ap = field["/AP"]
                if "/N" in ap:
                    appearances = ap["/N"].get_object()
                    if isinstance(appearances, dict):
                        states = list(appearances.keys())
                        print(f"Available States: {[str(s) for s in states]}")
                        
                        # Determine which is "checked" vs "unchecked"
                        if len(states) == 2:
                            off_state = next((s for s in states if "Off" in str(s)), None)
                            on_state = next((s for s in states if s != off_state), None)
                            print(f"  → Unchecked state: {off_state}")
                            print(f"  → Checked state: {on_state}")
            
            # Check for any default value
            if "/DV" in field:
                default_value = str(field["/DV"])
                print(f"Default Value: {default_value}")
            
            # Check field flags
            if "/Ff" in field:
                flags = field["/Ff"]
                print(f"Field Flags: {flags}")
                # Common flags:
                # 32768 = Radio button (not checkbox)
                # Other values indicate various properties
    
    print(f"\n{'=' * 80}")
    print(f"Total checkbox/button fields found: {checkbox_count}")
    print("=" * 80)
    
    # Also print field values from pages
    print("\n\nFIELD VALUES FROM PAGES:")
    print("=" * 80)
    for page_num, page in enumerate(reader.pages, 1):
        if "/Annots" in page:
            print(f"\nPage {page_num}:")
            annots = page["/Annots"]
            for annot_ref in annots:
                annot = annot_ref.get_object()
                if "/T" in annot and "/FT" in annot:
                    field_name = str(annot["/T"])
                    field_type = str(annot["/FT"])
                    if field_type == "/Btn":
                        current = str(annot.get("/V", "(not set)"))
                        print(f"  {field_name}: {current}")

if __name__ == "__main__":
    inspect_checkboxes()