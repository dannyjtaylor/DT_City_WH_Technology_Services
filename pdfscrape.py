import re
import csv
import PyPDF2

# Updated CSV headers with case sensitivity as provided
csv_headers = [
    "Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
    "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
    "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit",
    "No analysis was performed"
]

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract key measurement values from text
def parse_measurements(text):
    def extract_value(pattern, default=""):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    return {
        "pH (Field Measurement)": extract_value(r"pH[^0-9]{0,10}([\d.]+)"),
        "EC (Field Measurement)": extract_value(r"(?:EC|Conductivity)[^0-9]{0,10}([\d.]+)"),
        "ORP (Field Measurement)": extract_value(r"ORP[^0-9]{0,10}([\d.]+)"),
        "Temperature (Field Measurement)": extract_value(r"(?:Temperature|Temp)[^0-9]{0,10}([\d.]+)")
    }

# Function to build a row using extracted data
def generate_csv_row(parsed_data):
    row = [
        "Client Name Placeholder",  # Client Name
        "Area Name Placeholder",    # Area Name
        "Site Name Placeholder",    # Site Name
        "Manhole Name Placeholder", # Manhole Name
        "Sample001",                # sample id
        "2025-06-06",               # Sampling Date
        "12:00",                    # Collection Time
        "Sector A",                 # Sector
        "No",                       # Automated S.
        "Grab",                     # Sampling Type
        "ABC Labs",                 # Lab Name
        parsed_data["pH (Field Measurement)"],
        parsed_data["EC (Field Measurement)"],
        parsed_data["ORP (Field Measurement)"],
        parsed_data["Temperature (Field Measurement)"],
        "Ammonia",                 # name/Parameter (example)
        "No",                      # is_exceeded
        "0.15",                    # value
        "mg/L",                    # units
        "1.0",                     # NVL (Log10)
        "MH001",                   # Manhole ID
        "GIS-0001",                # Gis ID
        "East WWTP",               # WWTP
        "No",                      # Below detection limit
        "No"                       # No analysis was performed
    ]
    return row

# Main function to run the script
def convert_pdf_to_csv(pdf_path, output_csv_path):
    text = extract_pdf_text(pdf_path)
    parsed = parse_measurements(text)
    row = generate_csv_row(parsed)

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        writer.writerow(row)

    print(f"CSV file saved to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = "test2.pdf"  # Replace with your actual file
    output_csv = "output_lab_data.csv"
    convert_pdf_to_csv(pdf_path, output_csv)











# from PyPDF2 import PdfReader
# import csv

# reader = PdfReader("test.pdf")
# numPages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()


# # print(reader)
# print(numPages)
# # print(page)
# print(text)

# data = [
#     ["Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
#      "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
#      "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit", 
#      "No analysis was performed"]
# ]