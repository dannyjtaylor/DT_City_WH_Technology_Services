
import re
import csv
import os
import sys
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# Set paths to local Tesseract and Poppler binaries
tesseract_path = os.path.join(sys._MEIPASS, 'tesseract', 'tesseract.exe') if hasattr(sys, '_MEIPASS') else './tesseract/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

poppler_path = os.path.join(sys._MEIPASS, 'poppler', 'Library', 'bin') if hasattr(sys, '_MEIPASS') else './poppler/Library/bin'

csv_headers = ["Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
               "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
               "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit", "No analysis was performed"]

def extract_text(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text if text.strip() else None
    except:
        return None

def parse_ocr(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    text = ""
    for i, img in enumerate(images):
        if i == len(images) - 1:
            img = img.rotate(-90, expand=True)  # Rotate last page 90 degrees clockwise  # Rotate final page if needed
        text += pytesseract.image_to_string(img) + "\n"
    return text

def extract_value(text, label, fallback=""):
    match = re.search(rf"{label}[:\s]*([\w\s.-]+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else fallback

def parse_values(text):
    return {
        "Client Name": extract_value(text, "Client Name", "Unknown Client"),
        "Area Name": extract_value(text, "Area Name", "Unknown Area"),
        "Site Name": extract_value(text, "Site Name", "Unknown Site"),
        "Manhole Name": extract_value(text, "Manhole Name", "Unknown Manhole"),
        "pH (Field Measurement)": extract_value(text, "pH[^\d]{0,10}([\d.]+)"),
        "EC (Field Measurement)": extract_value(text, "(?:EC|Conductivity)[^\d]{0,10}([\d.]+)"),
        "ORP (Field Measurement)": extract_value(text, "ORP[^\d]{0,10}([\d.]+)"),
        "Temperature (Field Measurement)": extract_value(text, "(?:Temperature|Temp)[^\d]{0,10}([\d.]+)")
    }

def generate_row(data):
    return [
        data["Client Name"], data["Area Name"], data["Site Name"], data["Manhole Name"],
        "Sample001", "2025-06-06", "12:00", "Sector", "No", "Grab", "ABC Labs",
        data["pH (Field Measurement)"], data["EC (Field Measurement)"], data["ORP (Field Measurement)"], data["Temperature (Field Measurement)"],
        "Ammonia", "No", "0.15", "mg/L", "1.0", "MH001", "GIS-0001", "East WWTP", "No", "No"
    ]

def convert_pdf(pdf_path, csv_path):
    text = extract_text(pdf_path) or parse_ocr(pdf_path)
    parsed = parse_values(text)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        writer.writerow(generate_row(parsed))

def main():
    root = tk.Tk()
    root.withdraw()
    pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    default_csv = f"{base_name}.csv"

    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=default_csv,
        title="Save CSV As"
    )
    if not save_path:
        return

    convert_pdf(pdf_path, save_path)
    os.startfile(save_path)

if __name__ == "__main__":
    main()
