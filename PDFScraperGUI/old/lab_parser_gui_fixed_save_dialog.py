
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

# CSV headers
csv_headers = ["Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
               "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
               "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit", "No analysis was performed"]

# Functions for parsing and GUI
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
    return "\n".join(pytesseract.image_to_string(img) for img in images)

def parse_values(text):
    def find(pattern): return re.search(pattern, text, re.IGNORECASE)
    return {
        "pH (Field Measurement)": (m := find(r"pH[^0-9]{0,10}([\d.]+)")) and m.group(1) or "",
        "EC (Field Measurement)": (m := find(r"(?:EC|Conductivity)[^0-9]{0,10}([\d.]+)")) and m.group(1) or "",
        "ORP (Field Measurement)": (m := find(r"ORP[^0-9]{0,10}([\d.]+)")) and m.group(1) or "",
        "Temperature (Field Measurement)": (m := find(r"(?:Temperature|Temp)[^0-9]{0,10}([\d.]+)")) and m.group(1) or ""
    }

def generate_row(data):
    return ["Client", "Area", "Site", "Manhole", "Sample001", "2025-06-06", "12:00", "Sector", "No", "Grab", "ABC Labs",
            data["pH (Field Measurement)"], data["EC (Field Measurement)"], data["ORP (Field Measurement)"], data["Temperature (Field Measurement)"],
            "Ammonia", "No", "0.15", "mg/L", "1.0", "MH001", "GIS-0001", "East WWTP", "No", "No"]

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
    if not pdf_path: return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="lab_report.csv",
        title="Save CSV As"
    )
    if not save_path: return
    convert_pdf(pdf_path, save_path)
    os.startfile(save_path)

if __name__ == "__main__":
    main()
