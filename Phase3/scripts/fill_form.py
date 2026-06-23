# # scripts/fill_ifb_form.py
# import json
# from pathlib import Path
# from PyPDF2 import PdfReader, PdfWriter

# def main():
#     # --- Paths ---
#     SCRIPT_DIR = Path(__file__).parent
#     ROOT_DIR = SCRIPT_DIR.parent
#     INPUT_DIR = ROOT_DIR / "input"
#     TEMPLATE_DIR = ROOT_DIR / "templates"
#     OUTPUT_DIR = ROOT_DIR / "output"

#     BID_DATA_FILE = INPUT_DIR / "bid_data1.json"
#     TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"  # Your fillable PDF
#     OUTPUT_FILE = OUTPUT_DIR / "Filled_IFB.pdf"

#     OUTPUT_DIR.mkdir(exist_ok=True)

#     # --- Load bid data ---
#     with open(BID_DATA_FILE, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     # --- Define field mappings for Saint Louis County IFB ---
#     # Get exact field names using: reader.get_fields().keys()
#     form_data = {
#         # Vendor Information Form (Page 1)
#         "Company Legal Name": data["company_info"]["legal_name"],
#         "Doing Business As (if different from above)": data["company_info"]["dba"],
#         "Company E-Mail Address": data["company_info"]["email"],
#         "U.S. Mail Street Address": data["company_info"]["address"],
#         "City/State Zip Code": data["company_info"]["address"],  # Adjust if needed
#         "Company Telephone Number": data["company_info"]["phone"],
#         "State in Which Company is Domiciled": data["company_info"]["state_domiciled"],
#         "Minority-Owned Business Enterprise (MBE)": "Off" if not data["company_info"]["mbe_wbe"] else "Yes",
#         "Woman-Owned Business Enterprise (WBE)": "Off" if not data["company_info"]["mbe_wbe"] else "Yes",

#         # Bid Form (Page 2 of 2? - adjust page index if needed)
#         "Lump Sum Bid": f"${data['pricing']['lump_sum']:,.2f}",
#         "GRAND TOTAL": f"${data['pricing']['grand_total']:,.2f}",
#         "Allowance": f"${data['pricing']['allowance']:,.2f}"
#     }

#     # --- Fill PDF ---
#     reader = PdfReader(TEMPLATE_FILE)
#     writer = PdfWriter()

#     # Copy all pages
#     for page in reader.pages:
#         writer.add_page(page)

#     # Fill form fields
#     try:
#         writer.update_page_form_field_values(
#             writer.pages[0],  # Fields are on page 0 (adjust if needed)
#             form_data
#         )
#     except Exception as e:
#         print(f"⚠️ Field filling failed: {e}")
#         # Fallback: Try page 1
#         if len(writer.pages) > 1:
#             writer.update_page_form_field_values(
#                 writer.pages[1],
#                 form_data
#             )

#     # Flatten form (optional — makes fields non-editable)
#     # writer.flatten()

#     # Save
#     with open(OUTPUT_FILE, "wb") as f:
#         writer.write(f)

#     print(f"✅ Filled IFB saved to: {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()

# # scripts/fill_form.py
# import json
# from pathlib import Path
# from PyPDF2 import PdfReader, PdfWriter

# def main():
#     # --- Paths ---
#     SCRIPT_DIR = Path(__file__).parent
#     ROOT_DIR = SCRIPT_DIR.parent
#     INPUT_DIR = ROOT_DIR / "input"
#     TEMPLATE_DIR = ROOT_DIR / "templates"
#     OUTPUT_DIR = ROOT_DIR / "output"

#     BID_DATA_FILE = INPUT_DIR / "bid_data1.json"  # Your new data
#     TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
#     OUTPUT_FILE = OUTPUT_DIR / "Filled_IFB.pdf"

#     OUTPUT_DIR.mkdir(exist_ok=True)

#     # --- Load bid data ---
#     with open(BID_DATA_FILE, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     # --- Map data to PDF field names ---
#     # Use the exact field names from list_fields.py
#     form_data = {
#         # Vendor Information Form
#         "VIF Company Legal Name": data["company_info"]["legal_name"],
#         "VIF Doing Business As if different from above": data["company_info"]["dba"],
#         "VIF Company EMail Address": data["company_info"]["email"],
#         "VIF US Mail Street Address": data["company_info"]["address"],
#         "VIF CityState": data["company_info"]["city_state"],
#         "VIF Zip Code": data["company_info"]["zip_code"],
#         "VIF Company Telephone Number": data["company_info"]["phone"],
#         "VIF State": data["company_info"]["state_domiciled"],
#         "VIF MBE": "Yes" if data["company_info"]["mbe_wbe"] else "Off",
#         "VIF WBE": "Yes" if data["company_info"]["mbe_wbe"] else "Off",
#         "VIF Certifying Agency": data["company_info"]["certifying_agency"],
#         "VIF Name": data["company_info"]["name"],
#         "VIF Title": data["company_info"]["title"],
#         "VIF Direct EMail Address": data["company_info"]["direct_email"],
#         "VIF Vendor Contact Name": data["company_info"]["vendor_contact_name"],
#         "VIF Vendor Contact Direct Phone Number": data["company_info"]["vendor_contact_phone"],
#         "VIF Vendor Contact Direct Email Address": data["company_info"]["vendor_contact_email"],

#         # Background Info
#         "How many years has your company been in business": str(data["background_info"]["years_in_business"]),
#         "What was your average annual revenue for the last 3 years": data["background_info"]["average_annual_revenue"],
#         "If yes, explain why filed for bankruptcy": data["background_info"]["bankruptcy_explanation"],
#         "If yes, explain why your company had a contract terminated by government or public entity?": data["background_info"]["contract_termination_explanation"],
#         "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": data["background_info"]["fined_explanation"],
#         "If yes, explain why your company or a manager was indicted or convicted of a crime": data["background_info"]["crime_explanation"],
#         "If yes, explain why your company failed to complete the work it was contracted to do": data["background_info"]["failed_work_explanation"],
#         "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": data["background_info"]["lawsuit_explanation"],

#         # Projects (first 2 rows)
#         "Project DescriptionRow1": data["background_info"]["projects"][0]["description"] if len(data["background_info"]["projects"]) > 0 else "",
#         "ValueRow1": data["background_info"]["projects"][0]["value"] if len(data["background_info"]["projects"]) > 0 else "",
#         "Start DateRow1": data["background_info"]["projects"][0]["start_date"] if len(data["background_info"]["projects"]) > 0 else "",
#         "Expected End DateRow1": data["background_info"]["projects"][0]["end_date"] if len(data["background_info"]["projects"]) > 0 else "",
#         "Project DescriptionRow2": data["background_info"]["projects"][1]["description"] if len(data["background_info"]["projects"]) > 1 else "",
#         "ValueRow2": data["background_info"]["projects"][1]["value"] if len(data["background_info"]["projects"]) > 1 else "",
#         "Start DateRow2": data["background_info"]["projects"][1]["start_date"] if len(data["background_info"]["projects"]) > 1 else "",
#         "Expected End DateRow2": data["background_info"]["projects"][1]["end_date"] if len(data["background_info"]["projects"]) > 1 else "",

#         # References (first 2)
#         "Name of Entity": data["references"][0]["name"] if len(data["references"]) > 0 else "",
#         "Description of Service": data["references"][0]["service"] if len(data["references"]) > 0 else "",
#         "Dollar Value of Contract": data["references"][0]["value"] if len(data["references"]) > 0 else "",
#         "Contact Person": data["references"][0]["contact"] if len(data["references"]) > 0 else "",
#         "Contact EMail": data["references"][0]["email"] if len(data["references"]) > 0 else "",
#         "Business Phone": data["references"][0]["phone"] if len(data["references"]) > 0 else "",
#         "Mobile Phone": data["references"][0]["mobile"] if len(data["references"]) > 0 else "",

#         "Name of Entity_2": data["references"][1]["name"] if len(data["references"]) > 1 else "",
#         "Description of Service_2": data["references"][1]["service"] if len(data["references"]) > 1 else "",
#         "Dollar Value of Contract_2": data["references"][1]["value"] if len(data["references"]) > 1 else "",
#         "Contact Person_2": data["references"][1]["contact"] if len(data["references"]) > 1 else "",
#         "Contact EMail_2": data["references"][1]["email"] if len(data["references"]) > 1 else "",
#         "Business Phone_2": data["references"][1]["phone"] if len(data["references"]) > 1 else "",
#         "Mobile Phone_2": data["references"][1]["mobile"] if len(data["references"]) > 1 else "",

#         # NAICS
#         "NAICS Codes": data["naics"]["codes"],
#         "NAICS titles": data["naics"]["titles"]
#     }

#     # --- Fill PDF ---
#     reader = PdfReader(TEMPLATE_FILE)
#     writer = PdfWriter()

#     # Copy all pages
#     for page in reader.pages:
#         writer.add_page(page)

#     # Fill form fields
#     try:
#         writer.update_page_form_field_values(
#             writer.pages[0],  # Fields are on first page
#             form_data
#         )
#     except Exception as e:
#         print(f"⚠️ Field filling failed: {e}")
#         # Fallback: Try page 1
#         if len(writer.pages) > 1:
#             writer.update_page_form_field_values(
#                 writer.pages[1],
#                 form_data
#             )

#     # Flatten form (optional but recommended for submission)
#     # writer.flatten()

#     # Save
#     with open(OUTPUT_FILE, "wb") as f:
#         writer.write(f)

#     print(f"✅ Filled IFB saved to: {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()


# # scripts/fill_form.py
# import json
# from pathlib import Path
# from pypdf import PdfReader, PdfWriter

# def main():
#     # --- Paths ---
#     SCRIPT_DIR = Path(__file__).parent
#     ROOT_DIR = SCRIPT_DIR.parent
#     INPUT_DIR = ROOT_DIR / "input"
#     TEMPLATE_DIR = ROOT_DIR / "templates"
#     OUTPUT_DIR = ROOT_DIR / "output"

#     BID_DATA_FILE = INPUT_DIR / "bid_data1.json"
#     TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
#     OUTPUT_FILE = OUTPUT_DIR / "Filled_IFB.pdf"

#     OUTPUT_DIR.mkdir(exist_ok=True)

#     # --- Load bid data ---
#     with open(BID_DATA_FILE, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     # --- Map data to PDF field names ---
#     fields = data["company_info"]
#     bg = data["background_info"]
#     refs = data["references"]

#     form_data = {
#         # Vendor Information Form
#         "VIF Company Legal Name": fields["legal_name"],
#         "VIF Doing Business As if different from above": fields["dba"],
#         "VIF Company EMail Address": fields["email"],
#         "VIF US Mail Street Address": fields["address"],
#         "VIF CityState": fields["city_state"],
#         "VIF Zip Code": fields["zip_code"],
#         "VIF Company Telephone Number": fields["phone"],
#         "VIF State": fields["state_domiciled"],
#         "VIF MBE": "Yes" if fields["mbe_wbe"] else "Off",
#         "VIF WBE": "Yes" if fields["mbe_wbe"] else "Off",
#         "VIF Certifying Agency": fields["certifying_agency"],
#         "VIF Name": fields["name"],
#         "VIF Title": fields["title"],
#         "VIF Direct EMail Address": fields["direct_email"],
#         "VIF Vendor Contact Name": fields["vendor_contact_name"],
#         "VIF Vendor Contact Direct Phone Number": fields["vendor_contact_phone"],
#         "VIF Vendor Contact Direct Email Address": fields["vendor_contact_email"],

#         # Background Info
#         "How many years has your company been in business": str(bg["years_in_business"]),
#         "What was your average annual revenue for the last 3 years": bg["average_annual_revenue"],
#         "If yes, explain why filed for bankruptcy": bg["bankruptcy_explanation"],
#         "If yes, explain why your company had a contract terminated by government or public entity?": bg["contract_termination_explanation"],
#         "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": bg["fined_explanation"],
#         "If yes, explain why your company or a manager was indicted or convicted of a crime": bg["crime_explanation"],
#         "If yes, explain why your company failed to complete the work it was contracted to do": bg["failed_work_explanation"],
#         "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": bg["lawsuit_explanation"],

#         # Projects (first 2 rows)
#         "Project DescriptionRow1": bg["projects"][0]["description"] if len(bg["projects"]) > 0 else "",
#         "ValueRow1": bg["projects"][0]["value"] if len(bg["projects"]) > 0 else "",
#         "Start DateRow1": bg["projects"][0]["start_date"] if len(bg["projects"]) > 0 else "",
#         "Expected End DateRow1": bg["projects"][0]["end_date"] if len(bg["projects"]) > 0 else "",
#         "Project DescriptionRow2": bg["projects"][1]["description"] if len(bg["projects"]) > 1 else "",
#         "ValueRow2": bg["projects"][1]["value"] if len(bg["projects"]) > 1 else "",
#         "Start DateRow2": bg["projects"][1]["start_date"] if len(bg["projects"]) > 1 else "",
#         "Expected End DateRow2": bg["projects"][1]["end_date"] if len(bg["projects"]) > 1 else "",

#         # References (first 2)
#         "Name of Entity": refs[0]["name"] if len(refs) > 0 else "",
#         "Description of Service": refs[0]["service"] if len(refs) > 0 else "",
#         "Dollar Value of Contract": refs[0]["value"] if len(refs) > 0 else "",
#         "Contact Person": refs[0]["contact"] if len(refs) > 0 else "",
#         "Contact EMail": refs[0]["email"] if len(refs) > 0 else "",
#         "Business Phone": refs[0]["phone"] if len(refs) > 0 else "",
#         "Mobile Phone": refs[0]["mobile"] if len(refs) > 0 else "",

#         "Name of Entity_2": refs[1]["name"] if len(refs) > 1 else "",
#         "Description of Service_2": refs[1]["service"] if len(refs) > 1 else "",
#         "Dollar Value of Contract_2": refs[1]["value"] if len(refs) > 1 else "",
#         "Contact Person_2": refs[1]["contact"] if len(refs) > 1 else "",
#         "Contact EMail_2": refs[1]["email"] if len(refs) > 1 else "",
#         "Business Phone_2": refs[1]["phone"] if len(refs) > 1 else "",
#         "Mobile Phone_2": refs[1]["mobile"] if len(refs) > 1 else "",

#         # NAICS
#         "NAICS Codes": data["naics"]["codes"],
#         "NAICS titles": data["naics"]["titles"],

#         # --- BID FORM FIELDS (Page 34) ---
#         "Lump Sum Bid": f"${data['pricing']['lump_sum']:,.2f}",
#         "GRAND TOTAL": f"${data['pricing']['grand_total']:,.2f}",
#         "Allowance": f"${data['pricing']['allowance']:,.2f}"
#     }

#     # --- Fill PDF ---
#     reader = PdfReader(TEMPLATE_FILE)
#     writer = PdfWriter()

#     # Copy all pages
#     for page in reader.pages:
#         writer.add_page(page)

#     # Fill form fields on EVERY page (fields may be on page 33 = index 32)
#     for page in writer.pages:
#         writer.update_page_form_field_values(page, form_data)

#     # Flatten form (optional but recommended for submission)
#     # writer.flatten()

#     # Save
#     with open(OUTPUT_FILE, "wb") as f:
#         writer.write(f)

#     print(f"✅ Filled IFB saved to: {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()



"""
PDF Form Filler with Error Handling
Fills fillable PDF forms with data from JSON
"""
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def load_json_data(file_path):
    """Load and return JSON data"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_field_mapping(data):
    """Create mapping between JSON data and PDF field names"""
    fields = data["company_info"]
    bg = data["background_info"]
    refs = data["references"]
    naics = data["naics"]
    pricing = data.get("pricing", {})
    
    # Map your data to PDF field names
    # NOTE: These field names MUST match exactly what's in the PDF
    # Run the inspector script first to get exact field names
    
    form_data = {
        # ============== VENDOR INFORMATION FORM ==============
        "VIF Company Legal Name": fields.get("legal_name", ""),
        "VIF Doing Business As if different from above": fields.get("dba", ""),
        "VIF Company EMail Address": fields.get("email", ""),
        "VIF US Mail Street Address": fields.get("address", ""),
        "VIF CityState": fields.get("city_state", ""),
        "VIF Zip Code": fields.get("zip_code", ""),
        "VIF Company Telephone Number": fields.get("phone", ""),
        "VIF State": fields.get("state_domiciled", ""),
        "VIF MBE": "Yes" if fields.get("mbe_wbe", False) else "Off",
        "VIF WBE": "Yes" if fields.get("mbe_wbe", False) else "Off",
        "VIF Certifying Agency": fields.get("certifying_agency", ""),
        "VIF Name": fields.get("name", ""),
        "VIF Title": fields.get("title", ""),
        "VIF Direct EMail Address": fields.get("direct_email", ""),
        "VIF Vendor Contact Name": fields.get("vendor_contact_name", ""),
        "VIF Vendor Contact Direct Phone Number": fields.get("vendor_contact_phone", ""),
        "VIF Vendor Contact Direct Email Address": fields.get("vendor_contact_email", ""),
        
        # ============== BACKGROUND INFORMATION ==============
        "How many years has your company been in business": str(bg.get("years_in_business", "")),
        "What was your average annual revenue for the last 3 years": bg.get("average_annual_revenue", ""),
        
        # Yes/No explanations
        "If yes, explain why filed for bankruptcy": bg.get("bankruptcy_explanation", ""),
        "If yes, explain why your company had a contract terminated by government or public entity?": bg.get("contract_termination_explanation", ""),
        "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": bg.get("fined_explanation", ""),
        "If yes, explain why your company or a manager was indicted or convicted of a crime": bg.get("crime_explanation", ""),
        "If yes, explain why your company failed to complete the work it was contracted to do": bg.get("failed_work_explanation", ""),
        "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": bg.get("lawsuit_explanation", ""),
        
        # ============== PROJECTS ==============
        "Project DescriptionRow1": bg["projects"][0]["description"] if len(bg.get("projects", [])) > 0 else "",
        "ValueRow1": bg["projects"][0]["value"] if len(bg.get("projects", [])) > 0 else "",
        "Start DateRow1": bg["projects"][0]["start_date"] if len(bg.get("projects", [])) > 0 else "",
        "Expected End DateRow1": bg["projects"][0]["end_date"] if len(bg.get("projects", [])) > 0 else "",
        
        "Project DescriptionRow2": bg["projects"][1]["description"] if len(bg.get("projects", [])) > 1 else "",
        "ValueRow2": bg["projects"][1]["value"] if len(bg.get("projects", [])) > 1 else "",
        "Start DateRow2": bg["projects"][1]["start_date"] if len(bg.get("projects", [])) > 1 else "",
        "Expected End DateRow2": bg["projects"][1]["end_date"] if len(bg.get("projects", [])) > 1 else "",
        
        # ============== REFERENCES ==============
        # Reference 1
        "Name of Entity": refs[0]["name"] if len(refs) > 0 else "",
        "Description of Service": refs[0]["service"] if len(refs) > 0 else "",
        "Dollar Value of Contract": refs[0]["value"] if len(refs) > 0 else "",
        "Contact Person": refs[0]["contact"] if len(refs) > 0 else "",
        "Contact EMail": refs[0]["email"] if len(refs) > 0 else "",
        "Business Phone": refs[0]["phone"] if len(refs) > 0 else "",
        "Mobile Phone": refs[0]["mobile"] if len(refs) > 0 else "",
        
        # Reference 2
        "Name of Entity_2": refs[1]["name"] if len(refs) > 1 else "",
        "Description of Service_2": refs[1]["service"] if len(refs) > 1 else "",
        "Dollar Value of Contract_2": refs[1]["value"] if len(refs) > 1 else "",
        "Contact Person_2": refs[1]["contact"] if len(refs) > 1 else "",
        "Contact EMail_2": refs[1]["email"] if len(refs) > 1 else "",
        "Business Phone_2": refs[1]["phone"] if len(refs) > 1 else "",
        "Mobile Phone_2": refs[1]["mobile"] if len(refs) > 1 else "",
        
        # Reference 3 (if exists)
        "Name of Entity_3": refs[2]["name"] if len(refs) > 2 else "",
        "Description of Service_3": refs[2]["service"] if len(refs) > 2 else "",
        "Dollar Value of Contract_3": refs[2]["value"] if len(refs) > 2 else "",
        "Contact Person_3": refs[2]["contact"] if len(refs) > 2 else "",
        "Contact EMail_3": refs[2]["email"] if len(refs) > 2 else "",
        "Business Phone_3": refs[2]["phone"] if len(refs) > 2 else "",
        "Mobile Phone_3": refs[2]["mobile"] if len(refs) > 2 else "",
        
        # ============== NAICS CODES ==============
        "NAICS Codes": naics.get("codes", ""),
        "NAICS titles": naics.get("titles", ""),
        
        # ============== PRICING (if applicable) ==============
        "Lump Sum Bid": f"${pricing.get('lump_sum', 0):,.2f}" if pricing else "",
        "Allowance": f"${pricing.get('allowance', 0):,.2f}" if pricing else "",
        "GRAND TOTAL": f"${pricing.get('grand_total', 0):,.2f}" if pricing else "",
    }
    
    return form_data

def fill_pdf_form(template_path, output_path, form_data, flatten=False):
    """Fill PDF form fields and save to output file"""
    reader = PdfReader(template_path)
    writer = PdfWriter()
    
    # First, let's see what fields exist in the PDF
    pdf_fields = reader.get_fields()
    
    if not pdf_fields:
        print("⚠️  WARNING: No fillable fields found in PDF!")
        print("   This PDF might not have interactive form fields.")
        return False
    
    print(f"✅ Found {len(pdf_fields)} fields in PDF")
    
    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)
    
    # Track which fields were filled and which weren't found
    filled_count = 0
    not_found = []
    
    # Fill form fields
    for field_name, value in form_data.items():
        if value:  # Only fill if there's a value
            try:
                if field_name in pdf_fields:
                    writer.update_page_form_field_values(
                        writer.pages[0], 
                        {field_name: value},
                        auto_regenerate=False
                    )
                    filled_count += 1
                else:
                    not_found.append(field_name)
            except Exception as e:
                print(f"⚠️  Error filling field '{field_name}': {e}")
    
    print(f"✅ Filled {filled_count} fields")
    
    if not_found:
        print(f"\n⚠️  {len(not_found)} fields from mapping not found in PDF:")
        for field in not_found[:10]:  # Show first 10
            print(f"   - {field}")
        if len(not_found) > 10:
            print(f"   ... and {len(not_found) - 10} more")
    
    # Flatten form if requested (makes fields non-editable)
    if flatten:
        print("📋 Flattening form fields...")
        for page in writer.pages:
            writer.flatten_annotations()
    
    # Save the filled PDF
    with open(output_path, "wb") as f:
        writer.write(f)
    
    return True

def main():
    # ============== PATHS ==============
    SCRIPT_DIR = Path(__file__).parent
    ROOT_DIR = SCRIPT_DIR.parent
    INPUT_DIR = ROOT_DIR / "input"
    TEMPLATE_DIR = ROOT_DIR / "templates"
    OUTPUT_DIR = ROOT_DIR / "output"
    
    BID_DATA_FILE = INPUT_DIR / "bid_data1.json"
    TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
    OUTPUT_FILE = OUTPUT_DIR / "Filled_IFB.pdf"
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # ============== MAIN PROCESS ==============
    print("=" * 70)
    print("PDF FORM FILLER")
    print("=" * 70)
    print(f"Input JSON: {BID_DATA_FILE}")
    print(f"Template:   {TEMPLATE_FILE}")
    print(f"Output:     {OUTPUT_FILE}")
    print("=" * 70)
    
    # Check if files exist
    if not BID_DATA_FILE.exists():
        print(f"❌ Input JSON not found: {BID_DATA_FILE}")
        return
    
    if not TEMPLATE_FILE.exists():
        print(f"❌ Template PDF not found: {TEMPLATE_FILE}")
        return
    
    # Load data
    print("\n📂 Loading JSON data...")
    data = load_json_data(BID_DATA_FILE)
    print("✅ Data loaded successfully")
    
    # Create field mapping
    print("\n📋 Creating field mapping...")
    form_data = create_field_mapping(data)
    print(f"✅ Mapped {len(form_data)} fields")
    
    # Fill the PDF
    print("\n✏️  Filling PDF form...")
    success = fill_pdf_form(
        template_path=TEMPLATE_FILE,
        output_path=OUTPUT_FILE,
        form_data=form_data,
        flatten=False  # Set to True if you want non-editable output
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Filled PDF saved to:")
        print(f"   {OUTPUT_FILE}")
        print("=" * 70)
    else:
        print("\n❌ Failed to fill PDF form")

if __name__ == "__main__":
    main()