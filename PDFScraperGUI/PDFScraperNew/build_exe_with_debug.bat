@echo off
pyinstaller ^
--onefile ^
--windowed ^
--icon="morgana.ico" ^
--add-binary "tesseract\tesseract.exe;tesseract" ^
--add-binary "tesseract\tessdata;tesseract\tessdata" ^
--add-binary "poppler\Library\bin;poppler\Library\bin" ^
"lab_parser_gui_multi_debug_autorotate_commented.py"
