import os
from pathlib import Path
from PyPDF2 import PdfReader
from tqdm import tqdm
# 將 PDF 轉換為 TXT
PDF_DIR = "data/student_pdf"
TXT_DIR = "data/student_txt"

pdf_files = list(Path(PDF_DIR).glob("*.pdf"))
print(f"找到 {len(pdf_files)} 個 PDF 文件，正在轉換為 TXT...")

for pdf_file in tqdm(pdf_files, desc="轉換 PDF 為 TXT"):
    try:
        reader = PdfReader(str(pdf_file))
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        output_path = Path(TXT_DIR) / (pdf_file.stem + ".txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"❌ 無法處理 {pdf_file.name}: {e}")