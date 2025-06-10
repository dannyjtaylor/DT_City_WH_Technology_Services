
📦 PDF Converter Bundle (All-In-One)

This folder includes:
- `lab_parser_gui.py` — the main Python script
- `tesseract/` — contains tesseract.exe and tessdata (OCR engine)
- `poppler/` — contains Poppler's binaries for PDF image conversion

To bundle this as a .exe that requires NO installations for the end user:

1. Ensure you have tesseract.exe in /tesseract and poppler/bin in /poppler/Library/bin
2. Run this PyInstaller command from this folder:

   pyinstaller ^
     --onefile ^
     --windowed ^
     --icon=morgana.ico ^
     --add-binary "tesseract\tesseract.exe;tesseract" ^
     --add-binary "tesseract\tessdata;tesseract\tessdata" ^
     --add-binary "poppler\Library\bin;poppler\Library\bin" ^
     lab_parser_gui.py

---

💡 What is a Compiled Binary?

A compiled binary (like `tesseract.exe` or `pdfinfo.exe`) is a machine-level program built from source code using a compiler. Python can only *call* these binaries — it can't run or emulate them on its own. That's why we include them directly.

---

This approach makes it possible for users to run a single `.exe` without installing anything else.

