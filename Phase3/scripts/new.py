
# # scripts/fill_ifb_form.py
# import json
# from pathlib import Path
# from pypdf import PdfReader, PdfWriter
# from pypdf.generic import BooleanObject, NameObject

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

#     # --- Extract sections ---
#     company = data["company_info"]
#     background = data["background_info"]
#     refs = data["references"]
#     naics = data["naics"]
#     pricing = data.get("pricing", {})

#     # --- Build form_data with ALL fields ---
#                             #  old form data
#     # form_data = {
#     #     # Vendor Information Form
#     #     "VIF Company Legal Name": company["legal_name"],
#     #     "VIF Doing Business As if different from above": company["dba"],
#     #     "VIF Company EMail Address": company["email"],
#     #     "VIF US Mail Street Address": company["address"],
#     #     "VIF CityState": company["city_state"],
#     #     "VIF Zip Code": company["zip_code"],
#     #     "VIF Company Telephone Number": company["phone"],
#     #     "VIF State": company["state_domiciled"],
#     #     "VIF MBE": "Yes" if company["mbe_wbe"] else "Off",
#     #     "VIF WBE": "Yes" if company["mbe_wbe"] else "Off",
#     #     "VIF Certifying Agency": company["certifying_agency"],
#     #     "VIF Name": company["name"],
#     #     "VIF Title": company["title"],
#     #     "VIF Direct EMail Address": company["direct_email"],
#     #     "VIF Vendor Contact Name": company["vendor_contact_name"],
#     #     "VIF Vendor Contact Direct Phone Number": company["vendor_contact_phone"],
#     #     "VIF Vendor Contact Direct Email Address": company["vendor_contact_email"],

#     #     # Background Info
#     #     "How many years has your company been in business": str(background["years_in_business"]),
#     #     "What was your average annual revenue for the last 3 years": background["average_annual_revenue"],
#     #     "If yes, explain why filed for bankruptcy": background.get("bankruptcy_explanation", ""),
#     #     "If yes, explain why your company had a contract terminated by government or public entity?": background.get("contract_termination_explanation", ""),
#     #     "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": background.get("fined_explanation", ""),
#     #     "If yes, explain why your company or a manager was indicted or convicted of a crime": background.get("crime_explanation", ""),
#     #     "If yes, explain why your company failed to complete the work it was contracted to do": background.get("failed_work_explanation", ""),
#     #     "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": background.get("lawsuit_explanation", ""),

#     #     # Projects (6 rows)
#     #     "Project DescriptionRow1": background["projects"][0]["description"] if len(background["projects"]) > 0 else "",
#     #     "ValueRow1": background["projects"][0]["value"] if len(background["projects"]) > 0 else "",
#     #     "Start DateRow1": background["projects"][0]["start_date"] if len(background["projects"]) > 0 else "",
#     #     "Expected End DateRow1": background["projects"][0]["end_date"] if len(background["projects"]) > 0 else "",

#     #     "Project DescriptionRow2": background["projects"][1]["description"] if len(background["projects"]) > 1 else "",
#     #     "ValueRow2": background["projects"][1]["value"] if len(background["projects"]) > 1 else "",
#     #     "Start DateRow2": background["projects"][1]["start_date"] if len(background["projects"]) > 1 else "",
#     #     "Expected End DateRow2": background["projects"][1]["end_date"] if len(background["projects"]) > 1 else "",

#     #     "Project DescriptionRow3": background["projects"][2]["description"] if len(background["projects"]) > 2 else "",
#     #     "ValueRow3": background["projects"][2]["value"] if len(background["projects"]) > 2 else "",
#     #     "Start DateRow3": background["projects"][2]["start_date"] if len(background["projects"]) > 2 else "",
#     #     "Expected End DateRow3": background["projects"][2]["end_date"] if len(background["projects"]) > 2 else "",

#     #     "Project DescriptionRow4": background["projects"][3]["description"] if len(background["projects"]) > 3 else "",
#     #     "ValueRow4": background["projects"][3]["value"] if len(background["projects"]) > 3 else "",
#     #     "Start DateRow4": background["projects"][3]["start_date"] if len(background["projects"]) > 3 else "",
#     #     "Expected End DateRow4": background["projects"][3]["end_date"] if len(background["projects"]) > 3 else "",

#     #     "Project DescriptionRow5": background["projects"][4]["description"] if len(background["projects"]) > 4 else "",
#     #     "ValueRow5": background["projects"][4]["value"] if len(background["projects"]) > 4 else "",
#     #     "Start DateRow5": background["projects"][4]["start_date"] if len(background["projects"]) > 4 else "",
#     #     "Expected End DateRow5": background["projects"][4]["end_date"] if len(background["projects"]) > 4 else "",

#     #     "Project DescriptionRow6": background["projects"][5]["description"] if len(background["projects"]) > 5 else "",
#     #     "ValueRow6": background["projects"][5]["value"] if len(background["projects"]) > 5 else "",
#     #     "Start DateRow6": background["projects"][5]["start_date"] if len(background["projects"]) > 5 else "",
#     #     "Expected End DateRow6": background["projects"][5]["end_date"] if len(background["projects"]) > 5 else "",

#     #     # References (3 entities)
#     #     "Name of Entity": refs[0]["name"] if len(refs) > 0 else "",
#     #     "Description of Service": refs[0]["service"] if len(refs) > 0 else "",
#     #     "Dollar Value of Contract": refs[0]["value"] if len(refs) > 0 else "",
#     #     "Contact Person": refs[0]["contact"] if len(refs) > 0 else "",
#     #     "Contact EMail": refs[0]["email"] if len(refs) > 0 else "",
#     #     "Business Phone": refs[0]["phone"] if len(refs) > 0 else "",
#     #     "Mobile Phone": refs[0]["mobile"] if len(refs) > 0 else "",

#     #     "Name of Entity_2": refs[1]["name"] if len(refs) > 1 else "",
#     #     "Description of Service_2": refs[1]["service"] if len(refs) > 1 else "",
#     #     "Dollar Value of Contract_2": refs[1]["value"] if len(refs) > 1 else "",
#     #     "Contact Person_2": refs[1]["contact"] if len(refs) > 1 else "",
#     #     "Contact EMail_2": refs[1]["email"] if len(refs) > 1 else "",
#     #     "Business Phone_2": refs[1]["phone"] if len(refs) > 1 else "",
#     #     "Mobile Phone_2": refs[1]["mobile"] if len(refs) > 1 else "",

#     #     "Name of Entity_3": refs[2]["name"] if len(refs) > 2 else "",
#     #     "Description of Service_3": refs[2]["service"] if len(refs) > 2 else "",
#     #     "Dollar Value of Contract_3": refs[2]["value"] if len(refs) > 2 else "",
#     #     "Contact Person_3": refs[2]["contact"] if len(refs) > 2 else "",
#     #     "Contact EMail_3": refs[2]["email"] if len(refs) > 2 else "",
#     #     "Business Phone_3": refs[2]["phone"] if len(refs) > 2 else "",
#     #     "Mobile Phone_3": refs[2]["mobile"] if len(refs) > 2 else "",

#     #     # NAICS
#     #     "NAICS Codes": naics["codes"],
#     #     "NAICS titles": naics["titles"],

#     #     # Bid Form
#     #     "Lump Sum Bid": f"${pricing.get('lump_sum', 0):,.2f}",
#     #     "GRAND TOTAL": f"${pricing.get('grand_total', 0):,.2f}",
#     #     "Allowance": f"${pricing.get('allowance', 0):,.2f}",
#     # }


# #           new form data

#     # --- Build form_data with ALL fields ---
#     form_data = {
#         # Vendor Information Form
#         "VIF Company Legal Name": company["legal_name"],
#         "VIF Doing Business As if different from above": company["dba"],
#         "VIF Company EMail Address": company["email"],
#         "VIF US Mail Street Address": company["address"],
#         "VIF CityState": company["city_state"],
#         "VIF Zip Code": company["zip_code"],
#         "VIF Company Telephone Number": company["phone"],
#         "VIF State": company["state_domiciled"],

#         # ✅ MBE/WBE checkboxes — using NameObject for PDF compatibility
#         "VIF MBE": NameObject("/Off"),
#         "VIF WBE": NameObject("/Off"),
#         "VIF Certifying Agency": company["certifying_agency"],
#         "VIF Name": company["name"],
#         "VIF Title": company["title"],
#         "VIF Direct EMail Address": company["direct_email"],
#         "VIF Vendor Contact Name": company["vendor_contact_name"],
#         "VIF Vendor Contact Direct Phone Number": company["vendor_contact_phone"],
#         "VIF Vendor Contact Direct Email Address": company["vendor_contact_email"],

#         # Background Info
#         "How many years has your company been in business": str(background["years_in_business"]),
#         "What was your average annual revenue for the last 3 years": background["average_annual_revenue"],

#         # ✅ Background Yes/No checkboxes — all "No" (explanations are empty)
#         # Format: [Yes Box, No Box] → ["/Off", "/On"]
#         "Check Box1": NameObject("/Off"),   # Bankruptcy: Yes
#         "Check Box7": NameObject("/On"),    # Bankruptcy: No

#         "Check Box2": NameObject("/Off"),   # Contract terminated: Yes
#         "Check Box8": NameObject("/On"),    # Contract terminated: No

#         "Check Box3": NameObject("/Off"),   # Fined: Yes
#         "Check Box9": NameObject("/On"),    # Fined: No

#         "Check Box4": NameObject("/Off"),   # Crime: Yes
#         "Check Box10": NameObject("/On"),   # Crime: No

#         "Check Box5": NameObject("/Off"),   # Failed work: Yes
#         "Check Box11": NameObject("/On"),   # Failed work: No

#         "Check Box6": NameObject("/Off"),   # Lawsuit: Yes
#         "Check Box12": NameObject("/On"),   # Lawsuit: No

#         # Explanation fields (all empty in demo)
#         "If yes, explain why filed for bankruptcy": background.get("bankruptcy_explanation", ""),
#         "If yes, explain why your company had a contract terminated by government or public entity?": background.get("contract_termination_explanation", ""),
#         "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": background.get("fined_explanation", ""),
#         "If yes, explain why your company or a manager was indicted or convicted of a crime": background.get("crime_explanation", ""),
#         "If yes, explain why your company failed to complete the work it was contracted to do": background.get("failed_work_explanation", ""),
#         "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": background.get("lawsuit_explanation", ""),

#         # Projects (6 rows)
#         "Project DescriptionRow1": background["projects"][0]["description"] if len(background["projects"]) > 0 else "",
#         "ValueRow1": background["projects"][0]["value"] if len(background["projects"]) > 0 else "",
#         "Start DateRow1": background["projects"][0]["start_date"] if len(background["projects"]) > 0 else "",
#         "Expected End DateRow1": background["projects"][0]["end_date"] if len(background["projects"]) > 0 else "",

#         "Project DescriptionRow2": background["projects"][1]["description"] if len(background["projects"]) > 1 else "",
#         "ValueRow2": background["projects"][1]["value"] if len(background["projects"]) > 1 else "",
#         "Start DateRow2": background["projects"][1]["start_date"] if len(background["projects"]) > 1 else "",
#         "Expected End DateRow2": background["projects"][1]["end_date"] if len(background["projects"]) > 1 else "",

#         "Project DescriptionRow3": background["projects"][2]["description"] if len(background["projects"]) > 2 else "",
#         "ValueRow3": background["projects"][2]["value"] if len(background["projects"]) > 2 else "",
#         "Start DateRow3": background["projects"][2]["start_date"] if len(background["projects"]) > 2 else "",
#         "Expected End DateRow3": background["projects"][2]["end_date"] if len(background["projects"]) > 2 else "",

#         "Project DescriptionRow4": background["projects"][3]["description"] if len(background["projects"]) > 3 else "",
#         "ValueRow4": background["projects"][3]["value"] if len(background["projects"]) > 3 else "",
#         "Start DateRow4": background["projects"][3]["start_date"] if len(background["projects"]) > 3 else "",
#         "Expected End DateRow4": background["projects"][3]["end_date"] if len(background["projects"]) > 3 else "",

#         "Project DescriptionRow5": background["projects"][4]["description"] if len(background["projects"]) > 4 else "",
#         "ValueRow5": background["projects"][4]["value"] if len(background["projects"]) > 4 else "",
#         "Start DateRow5": background["projects"][4]["start_date"] if len(background["projects"]) > 4 else "",
#         "Expected End DateRow5": background["projects"][4]["end_date"] if len(background["projects"]) > 4 else "",

#         "Project DescriptionRow6": background["projects"][5]["description"] if len(background["projects"]) > 5 else "",
#         "ValueRow6": background["projects"][5]["value"] if len(background["projects"]) > 5 else "",
#         "Start DateRow6": background["projects"][5]["start_date"] if len(background["projects"]) > 5 else "",
#         "Expected End DateRow6": background["projects"][5]["end_date"] if len(background["projects"]) > 5 else "",

#         # References (3 entities)
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

#         "Name of Entity_3": refs[2]["name"] if len(refs) > 2 else "",
#         "Description of Service_3": refs[2]["service"] if len(refs) > 2 else "",
#         "Dollar Value of Contract_3": refs[2]["value"] if len(refs) > 2 else "",
#         "Contact Person_3": refs[2]["contact"] if len(refs) > 2 else "",
#         "Contact EMail_3": refs[2]["email"] if len(refs) > 2 else "",
#         "Business Phone_3": refs[2]["phone"] if len(refs) > 2 else "",
#         "Mobile Phone_3": refs[2]["mobile"] if len(refs) > 2 else "",

#         # NAICS
#         "NAICS Codes": naics["codes"],
#         "NAICS titles": naics["titles"],

#         # Bid Form
#         "Lump Sum Bid": f"${pricing.get('lump_sum', 0):,.2f}",
#         "GRAND TOTAL": f"${pricing.get('grand_total', 0):,.2f}",
#         "Allowance": f"${pricing.get('allowance', 0):,.2f}",
#     }
#     # --- Load PDF ---
#     reader = PdfReader(TEMPLATE_FILE)
#     writer = PdfWriter()

#     # Preserve AcroForm structure
#     if "/AcroForm" in reader.trailer["/Root"]:
#         writer._root_object[NameObject("/AcroForm")] = reader.trailer["/Root"]["/AcroForm"]
#         acroform = writer._root_object["/AcroForm"].get_object()
#         acroform[NameObject("/NeedAppearances")] = BooleanObject(True)

#     # Copy all pages
#     for page in reader.pages:
#         writer.add_page(page)

#     # Fill form on every page
#     for page in writer.pages:
#         writer.update_page_form_field_values(page, form_data)

#     # Save filled PDF
#     with open(OUTPUT_FILE, "wb") as f:
#         writer.write(f)

#     print(f"✅ Filled IFB saved to: {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()


#  code for checkboxes
# scripts/fill_ifb_form.py
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, NameObject, IndirectObject

def set_checkbox_value(writer, page, field_name, should_check):
    """
    Directly set checkbox value by accessing the field's widget annotation.
    Tries multiple common checkbox value patterns.
    """
    if "/Annots" not in page:
        return False
    
    annots = page["/Annots"]
    if annots is None:
        return False
    
    for annot_ref in annots:
        if isinstance(annot_ref, IndirectObject):
            annot = annot_ref.get_object()
        else:
            annot = annot_ref
            
        if annot is None or "/T" not in annot:
            continue
            
        if str(annot["/T"]) == field_name:
            # Found the field - now set its value
            if should_check:
                # Try common "checked" values in order of likelihood
                check_values = ["/Yes", "/On", "/1", NameObject("/Yes"), NameObject("/On")]
            else:
                # Unchecked is almost always /Off
                check_values = ["/Off", NameObject("/Off")]
            
            # Set the value
            value = check_values[0] if isinstance(check_values[0], NameObject) else NameObject(check_values[0])
            annot[NameObject("/V")] = value
            annot[NameObject("/AS")] = value  # Appearance state
            
            return True
    
    return False

def main():
    # --- Paths ---
    SCRIPT_DIR = Path(__file__).parent
    ROOT_DIR = SCRIPT_DIR.parent
    INPUT_DIR = ROOT_DIR / "input"
    TEMPLATE_DIR = ROOT_DIR / "templates"
    OUTPUT_DIR = ROOT_DIR / "output"

    BID_DATA_FILE = INPUT_DIR / "bid_data2.json"
    TEMPLATE_FILE = TEMPLATE_DIR / "highlighted_pdf.pdf"
    OUTPUT_FILE = OUTPUT_DIR / "Filled_IFB.pdf"

    OUTPUT_DIR.mkdir(exist_ok=True)

    # --- Load bid data ---
    with open(BID_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Extract sections ---
    company = data["company_info"]
    background = data["background_info"]
    refs = data["references"]
    naics = data["naics"]
    pricing = data.get("pricing", {})

    # --- Load PDF ---
    reader = PdfReader(TEMPLATE_FILE)
    writer = PdfWriter()

    # Preserve AcroForm structure
    if "/AcroForm" in reader.trailer["/Root"]:
        writer._root_object[NameObject("/AcroForm")] = reader.trailer["/Root"]["/AcroForm"]
        acroform = writer._root_object["/AcroForm"].get_object()
        acroform[NameObject("/NeedAppearances")] = BooleanObject(True)

    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)

    # --- Build form_data for text fields ---
    form_data = {
        # Vendor Information Form
        "VIF Company Legal Name": company["legal_name"],
        "VIF Doing Business As if different from above": company["dba"],
        "VIF Company EMail Address": company["email"],
        "VIF US Mail Street Address": company["address"],
        "VIF CityState": company["city_state"],
        "VIF Zip Code": company["zip_code"],
        "VIF Company Telephone Number": company["phone"],
        "VIF State": company["state_domiciled"],
        "VIF Certifying Agency": company["certifying_agency"],
        "VIF Name": company["name"],
        "VIF Title": company["title"],
        "VIF Direct EMail Address": company["direct_email"],
        "VIF Vendor Contact Name": company["vendor_contact_name"],
        "VIF Vendor Contact Direct Phone Number": company["vendor_contact_phone"],
        "VIF Vendor Contact Direct Email Address": company["vendor_contact_email"],

        # Background Info
        "How many years has your company been in business": str(background["years_in_business"]),
        "What was your average annual revenue for the last 3 years": background["average_annual_revenue"],

        # Explanation fields (all empty)
        "If yes, explain why filed for bankruptcy": background.get("bankruptcy_explanation", ""),
        "If yes, explain why your company had a contract terminated by government or public entity?": background.get("contract_termination_explanation", ""),
        "If yes, explain why your company was penalized or fined for a work-related issue associated with a contract": background.get("fined_explanation", ""),
        "If yes, explain why your company or a manager was indicted or convicted of a crime": background.get("crime_explanation", ""),
        "If yes, explain why your company failed to complete the work it was contracted to do": background.get("failed_work_explanation", ""),
        "If yes, explain why there are pending claims or lawsuits that may prevent the completion of the work for this contract": background.get("lawsuit_explanation", ""),

        # Projects
        "Project DescriptionRow1": background["projects"][0]["description"] if len(background["projects"]) > 0 else "",
        "ValueRow1": background["projects"][0]["value"] if len(background["projects"]) > 0 else "",
        "Start DateRow1": background["projects"][0]["start_date"] if len(background["projects"]) > 0 else "",
        "Expected End DateRow1": background["projects"][0]["end_date"] if len(background["projects"]) > 0 else "",

        "Project DescriptionRow2": background["projects"][1]["description"] if len(background["projects"]) > 1 else "",
        "ValueRow2": background["projects"][1]["value"] if len(background["projects"]) > 1 else "",
        "Start DateRow2": background["projects"][1]["start_date"] if len(background["projects"]) > 1 else "",
        "Expected End DateRow2": background["projects"][1]["end_date"] if len(background["projects"]) > 1 else "",

        "Project DescriptionRow3": background["projects"][2]["description"] if len(background["projects"]) > 2 else "",
        "ValueRow3": background["projects"][2]["value"] if len(background["projects"]) > 2 else "",
        "Start DateRow3": background["projects"][2]["start_date"] if len(background["projects"]) > 2 else "",
        "Expected End DateRow3": background["projects"][2]["end_date"] if len(background["projects"]) > 2 else "",

        "Project DescriptionRow4": background["projects"][3]["description"] if len(background["projects"]) > 3 else "",
        "ValueRow4": background["projects"][3]["value"] if len(background["projects"]) > 3 else "",
        "Start DateRow4": background["projects"][3]["start_date"] if len(background["projects"]) > 3 else "",
        "Expected End DateRow4": background["projects"][3]["end_date"] if len(background["projects"]) > 3 else "",

        "Project DescriptionRow5": background["projects"][4]["description"] if len(background["projects"]) > 4 else "",
        "ValueRow5": background["projects"][4]["value"] if len(background["projects"]) > 4 else "",
        "Start DateRow5": background["projects"][4]["start_date"] if len(background["projects"]) > 4 else "",
        "Expected End DateRow5": background["projects"][4]["end_date"] if len(background["projects"]) > 4 else "",

        "Project DescriptionRow6": background["projects"][5]["description"] if len(background["projects"]) > 5 else "",
        "ValueRow6": background["projects"][5]["value"] if len(background["projects"]) > 5 else "",
        "Start DateRow6": background["projects"][5]["start_date"] if len(background["projects"]) > 5 else "",
        "Expected End DateRow6": background["projects"][5]["end_date"] if len(background["projects"]) > 5 else "",

        # References
        "Name of Entity": refs[0]["name"] if len(refs) > 0 else "",
        "Description of Service": refs[0]["service"] if len(refs) > 0 else "",
        "Dollar Value of Contract": refs[0]["value"] if len(refs) > 0 else "",
        "Contact Person": refs[0]["contact"] if len(refs) > 0 else "",
        "Contact EMail": refs[0]["email"] if len(refs) > 0 else "",
        "Business Phone": refs[0]["phone"] if len(refs) > 0 else "",
        "Mobile Phone": refs[0]["mobile"] if len(refs) > 0 else "",

        "Name of Entity_2": refs[1]["name"] if len(refs) > 1 else "",
        "Description of Service_2": refs[1]["service"] if len(refs) > 1 else "",
        "Dollar Value of Contract_2": refs[1]["value"] if len(refs) > 1 else "",
        "Contact Person_2": refs[1]["contact"] if len(refs) > 1 else "",
        "Contact EMail_2": refs[1]["email"] if len(refs) > 1 else "",
        "Business Phone_2": refs[1]["phone"] if len(refs) > 1 else "",
        "Mobile Phone_2": refs[1]["mobile"] if len(refs) > 1 else "",

        "Name of Entity_3": refs[2]["name"] if len(refs) > 2 else "",
        "Description of Service_3": refs[2]["service"] if len(refs) > 2 else "",
        "Dollar Value of Contract_3": refs[2]["value"] if len(refs) > 2 else "",
        "Contact Person_3": refs[2]["contact"] if len(refs) > 2 else "",
        "Contact EMail_3": refs[2]["email"] if len(refs) > 2 else "",
        "Business Phone_3": refs[2]["phone"] if len(refs) > 2 else "",
        "Mobile Phone_3": refs[2]["mobile"] if len(refs) > 2 else "",

        # NAICS
        "NAICS Codes": naics["codes"],
        "NAICS titles": naics["titles"],
    }

    # --- Fill text fields first ---
    for page in writer.pages:
        try:
            writer.update_page_form_field_values(page, form_data)
        except Exception as e:
            print(f"Warning: Error updating text fields: {e}")

    # --- Now handle checkboxes separately with direct manipulation ---
    checkbox_mappings = {
        # Format: field_name: should_be_checked
        "VIF MBE": False,  # Not MBE certified
        "VIF WBE": False,  # Not WBE certified
        
        # Background questions - all "No" (Check Box 7, 8, 9, 10, 11, 12 should be checked)
        "Check Box1": True,   # Bankruptcy: Yes
        "Check Box7": False,    # Bankruptcy: No ✓
        
        "Check Box2": False,   # Contract terminated: Yes
        "Check Box8": True,    # Contract terminated: No ✓
        
        "Check Box3": False,   # Fined: Yes
        "Check Box9": True,    # Fined: No ✓
        
        "Check Box4": False,   # Crime: Yes
        "Check Box10": True,   # Crime: No ✓
        
        "Check Box5": False,   # Failed work: Yes
        "Check Box11": True,   # Failed work: No ✓
        
        "Check Box6": False,   # Lawsuit: Yes
        "Check Box12": True,   # Lawsuit: No ✓
    }

    print("\nSetting checkbox values:")
    for page_num, page in enumerate(writer.pages, 1):
        for field_name, should_check in checkbox_mappings.items():
            result = set_checkbox_value(writer, page, field_name, should_check)
            if result:
                status = "✓ CHECKED" if should_check else "○ UNCHECKED"
                print(f"  Page {page_num}: {field_name} → {status}")

    # --- Save filled PDF ---
    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)

    print(f"\n✅ Filled IFB saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()