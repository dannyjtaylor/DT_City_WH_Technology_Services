
import re
import csv
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

csv_headers = [
    "Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
    "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
    "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit",
    "No analysis was performed"
]

def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

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

def generate_csv_row(parsed_data):
    return [
        "Client Name Placeholder", "Area Name Placeholder", "Site Name Placeholder", "Manhole Name Placeholder",
        "Sample001", "2025-06-06", "12:00", "Sector A", "No", "Grab", "ABC Labs",
        parsed_data["pH (Field Measurement)"],
        parsed_data["EC (Field Measurement)"],
        parsed_data["ORP (Field Measurement)"],
        parsed_data["Temperature (Field Measurement)"],
        "Ammonia", "No", "0.15", "mg/L", "1.0", "MH001", "GIS-0001", "East WWTP", "No", "No"
    ]

def convert_pdf_to_csv(pdf_path, output_csv_path):
    try:
        text = extract_pdf_text(pdf_path)
        parsed = parse_measurements(text)
        row = generate_csv_row(parsed)

        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            writer.writerow(row)

        return output_csv_path
    except Exception as e:
        return str(e)

def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a lab report PDF",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        messagebox.showinfo("Cancelled", "No file was selected.")
        return

    default_name = os.path.splitext(os.path.basename(file_path))[0] + "_converted.csv"
    save_path = filedialog.asksaveasfilename(
        title="Save CSV as...",
        defaultextension=".csv",
        initialfile=default_name,
        filetypes=[("CSV files", "*.csv")]
    )

    if not save_path:
        messagebox.showinfo("Cancelled", "No save location selected.")
        return

    result = convert_pdf_to_csv(file_path, save_path)

    if result.endswith(".csv"):
        messagebox.showinfo("Success", f"CSV created and saved to:\n{result}")
    else:
        messagebox.showerror("Error", f"Failed to convert PDF:\n{result}")

if __name__ == "__main__":
    main()
