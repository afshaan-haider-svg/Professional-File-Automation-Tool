import os
from PyPDF2 import PdfMerger

def merge_pdfs():
    source_folder = "input_files/pdfs"
    output_folder = "output_files/merged_pdf"

    os.makedirs(output_folder, exist_ok=True)

    merger = PdfMerger()

    pdf_files = [
        file for file in os.listdir(source_folder)
        if file.lower().endswith(".pdf")
    ]

    pdf_files.sort()

    if len(pdf_files) == 0:
        print("No PDF files found.")
        return

    for pdf in pdf_files:
        pdf_path = os.path.join(source_folder, pdf)
        merger.append(pdf_path)

    output_path = os.path.join(output_folder, "merged_file.pdf")
    merger.write(output_path)
    merger.close()

    print("PDFs merged successfully.")