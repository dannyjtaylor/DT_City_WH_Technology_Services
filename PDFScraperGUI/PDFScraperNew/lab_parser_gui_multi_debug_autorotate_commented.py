
import re
import csv
import os
import sys
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import tempfile
import shutil

# Set up Tesseract and Poppler paths depending on whether running as executable or script
tesseract_path = os.path.join(sys._MEIPASS, 'tesseract', 'tesseract.exe') if hasattr(sys, '_MEIPASS') else './tesseract/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path
poppler_path = os.path.join(sys._MEIPASS, 'poppler', 'Library', 'bin') if hasattr(sys, '_MEIPASS') else './poppler/Library/bin'

# Define the output CSV headers
csv_headers = ["Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
               "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
               "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit", "No analysis was performed"]

# Try to extract text using PyPDF2 (works only for text-based PDFs)
def extract_text(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        return text if text.strip() else None
    except Exception as e:
        print(f"[ERROR] Failed to extract text using PyPDF2: {e}")
        return None

# Use OCR via Tesseract to extract text from images if direct extraction fails
def parse_ocr(pdf_path, temp_dir):
    print("[INFO] Falling back to OCR...")
    images = convert_from_path(pdf_path, poppler_path=poppler_path, output_folder=temp_dir)
    text = ""
    for i, img in enumerate(images):
        try:
            # Detect text orientation
            osd = pytesseract.image_to_osd(img)
            rotate_angle = int(re.search(r'Rotate: (\d+)', osd).group(1))
            if rotate_angle != 0:
                img = img.rotate(360 - rotate_angle, expand=True)
                print(f"[INFO] Rotated page {i+1} by {rotate_angle}° for OCR alignment.")
        except Exception as e:
            print(f"[WARNING] Orientation detection failed on page {i+1}: {e}")

        # Save debug image
        img_path = os.path.join(temp_dir, f"page_{i+1}.png")
        img.save(img_path)
        print(f"[DEBUG] Saved page image for OCR: {img_path}")

        # Perform OCR
        ocr_text = pytesseract.image_to_string(img)
        print(f"[DEBUG] OCR output from page {i+1}:
{ocr_text}
{'-'*60}")
        text += ocr_text + "\n"
    return text

# Extract metadata like client/site names and basic measurements
def extract_metadata(text):
    def find(label, fallback="Unknown"):
        match = re.search(rf"{label}[:\s]*([\w\s.-]+)", text, re.IGNORECASE)
        return match.group(1).strip() if match and match.group(1) else fallback

    return {
        "Client Name": find("Client Name"),
        "Area Name": find("Area Name"),
        "Site Name": find("Site Name"),
        "Manhole Name": find("Manhole Name"),
        "pH": find("pH", ""),
        "EC": find("EC|Conductivity", ""),
        "ORP": find("ORP", ""),
        "Temp": find("Temperature|Temp", "")
    }

# Identify multiple parameters from OCR text
def extract_parameters(text):
    param_lines = re.findall(r"(\w+)\s+([\d.]+)\s+(\w+/\w+|\w+)(.*)", text)
    parameters = []
    for line in param_lines:
        name, value, units, flags = line
        is_exceeded = "yes" if "exceed" in flags.lower() else "no"
        below_detect = "yes" if "below" in flags.lower() else "no"
        no_analysis = "yes" if "no analysis" in flags.lower() else "no"
        parameters.append({
            "name": name,
            "value": value,
            "units": units,
            "is_exceeded": is_exceeded,
            "below_detection_limit": below_detect,
            "no_analysis": no_analysis
        })
    print(f"[DEBUG] Found {len(parameters)} parameters.")
    return parameters

# Main function to extract data and write to CSV
def convert_to_csv(pdf_path, csv_path):
    temp_dir = tempfile.mkdtemp()
    try:
        text = extract_text(pdf_path)
        if not text:
            text = parse_ocr(pdf_path, temp_dir)

        print(f"[INFO] Final text used for parsing:
{text[:1000]}...
{'='*80}")

        meta = extract_metadata(text)
        print(f"[DEBUG] Metadata: {meta}")

        param_entries = extract_parameters(text)

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            for param in param_entries:
                row = [
                    meta["Client Name"], meta["Area Name"], meta["Site Name"], meta["Manhole Name"],
                    "Sample001", "2025-06-06", "12:00", "Sector", "No", "Grab", "ABC Labs",
                    meta["pH"], meta["EC"], meta["ORP"], meta["Temp"],
                    param["name"], param["is_exceeded"], param["value"], param["units"], "1.0",
                    "MH001", "GIS-0001", "East WWTP",
                    param["below_detection_limit"], param["no_analysis"]
                ]
                print(f"[DEBUG] Writing row: {row}")
                writer.writerow(row)
        print(f"[SUCCESS] CSV saved to: {csv_path}")
        os.startfile(csv_path)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[INFO] Temp directory cleaned up: {temp_dir}")

# GUI for user to select PDF and where to save the CSV
def main():
    root = tk.Tk()
    root.withdraw()
    pdf_path = filedialog.askopenfilename(title="Select Lab Report PDF", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv", initialfile=f"{base}.csv",
        filetypes=[("CSV files", "*.csv")], title="Save CSV As"
    )
    if not save_path:
        return
    convert_to_csv(pdf_path, save_path)

if __name__ == "__main__":
    main()
