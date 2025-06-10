
import re
import csv
import PyPDF2
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import shutil

# Attempt to import OCR tools
try:
    from pdf2image import convert_from_path
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdf2image"])
    from pdf2image import convert_from_path

try:
    import pytesseract
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])
    import pytesseract

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image

csv_headers = [
    "Client Name", "Area Name", "Site Name", "Manhole Name", "sample id", "Sampling Date", "Collection Time", "Sector", "Automated S.",
    "Sampling Type", "Lab Name", "pH (Field Measurement)", "EC (Field Measurement)", "ORP (Field Measurement)", "Temperature (Field Measurement)",
    "name/Parameter", "is_exceeded", "value", "units", "NVL (Log10)", "Manhole ID", "Gis ID", "WWTP", "Below detection limit",
    "No analysis was performed"
]

def install_tesseract():
    tesseract_installer = "https://github.com/UB-Mannheim/tesseract/wiki/Tesseract-OCR-Setup-v5.3.1.20230401.exe"
    local_path = os.path.join(Path.home(), "Downloads", "tesseract_installer.exe")
    try:
        import urllib.request
        urllib.request.urlretrieve(tesseract_installer, local_path)
        subprocess.Popen([local_path], shell=True)
        messagebox.showinfo("Tesseract Required", "Tesseract-OCR is being installed. After the installer finishes, rerun the program.")
        return False
    except Exception as e:
        messagebox.showerror("Install Failed", f"Failed to download Tesseract: {e}")
        return False

def install_poppler():
    try:
        import zipfile
        import urllib.request

        poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.11.0-0/Release-23.11.0-0.zip"
        zip_path = os.path.join(Path.home(), "Downloads", "poppler.zip")
        extract_dir = os.path.join(Path.home(), "poppler")

        urllib.request.urlretrieve(poppler_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        bin_path = os.path.join(extract_dir, os.listdir(extract_dir)[0], "Library", "bin")
        os.environ["PATH"] += os.pathsep + bin_path
        return True
    except Exception as e:
        messagebox.showerror("Install Failed", f"Failed to download Poppler: {e}")
        return False

def ensure_dependencies():
    # Tesseract check
    if not shutil.which("tesseract"):
        proceed = messagebox.askyesno("Dependency Missing", "Tesseract-OCR is not installed. Do you want to download and install it?")
        if proceed:
            return install_tesseract()
        else:
            return False

    # Poppler check
    if not shutil.which("pdfinfo"):
        proceed = messagebox.askyesno("Dependency Missing", "Poppler is not installed. Do you want to download and install it?")
        if proceed:
            return install_poppler()
        else:
            return False

    return True

def extract_pdf_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PyPDF2 failed: {e}")
        text = ""

    if not text.strip():
        # Fallback to OCR
        try:
            text = ""
            images = convert_from_path(pdf_path)
            for image in images:
                ocr_text = pytesseract.image_to_string(image)
                text += ocr_text + "\n"
        except Exception as e:
            print(f"OCR failed: {e}")
            text = ""

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
        if not text.strip():
            raise ValueError("No text could be extracted from PDF, even with OCR.")

        parsed = parse_measurements(text)
        row = generate_csv_row(parsed)

        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            writer.writerow(row)

        return output_csv_path
    except Exception as e:
        return str(e)

def open_file(path):
    try:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', path))
        elif os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', path))
    except Exception as e:
        print(f"Failed to open file: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    if not ensure_dependencies():
        return

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

    if result.endswith(".csv") and os.path.exists(result):
        messagebox.showinfo("Success", f"CSV created and saved to:\n{result}")
        open_file(result)
    else:
        messagebox.showerror("Error", f"Failed to convert PDF:\n{result}")

if __name__ == "__main__":
    main()
