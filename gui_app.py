import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfMerger


def rename_images():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.webp"),
            ("All Files", "*.*")
        ]
    )

    if not files:
        return

    prefix = simpledialog.askstring("Prefix", "Enter new image name, example: wedding")

    if not prefix:
        messagebox.showwarning("Warning", "Prefix required!")
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")

    if not output_folder:
        return

    count = 1

    for file in files:
        ext = os.path.splitext(file)[1]
        new_name = f"{prefix}_{count}{ext}"
        new_path = os.path.join(output_folder, new_name)

        shutil.copy2(file, new_path)
        count += 1

    messagebox.showinfo("Success", f"{count - 1} images renamed successfully!")


def organize_files():
    source_folder = filedialog.askdirectory(title="Select Main Folder to Organize")

    if not source_folder:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")

    if not output_folder:
        return

    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".webp", ".gif"],
        "PDFs": [".pdf"],
        "Documents": [".doc", ".docx", ".txt", ".ppt", ".pptx"],
        "Excel_Files": [".xls", ".xlsx", ".csv"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Audio": [".mp3", ".wav", ".aac"],
        "Zip_Files": [".zip", ".rar", ".7z"],
        "Python_Files": [".py"],
    }

    organized_count = 0
    found_files = []

    for root_dir, folders, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root_dir, file)
            found_files.append(file_path)

            ext = os.path.splitext(file)[1].lower()
            moved = False

            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(output_folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_path = os.path.join(target_folder, file)

                    # agar same name ki file ho to overwrite issue avoid
                    if os.path.exists(target_path):
                        name, extension = os.path.splitext(file)
                        target_path = os.path.join(
                            target_folder,
                            f"{name}_copy{extension}"
                        )

                    shutil.copy2(file_path, target_path)
                    organized_count += 1
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(output_folder, "Others")
                os.makedirs(other_folder, exist_ok=True)

                target_path = os.path.join(other_folder, file)

                if os.path.exists(target_path):
                    name, extension = os.path.splitext(file)
                    target_path = os.path.join(
                        other_folder,
                        f"{name}_copy{extension}"
                    )

                shutil.copy2(file_path, target_path)
                organized_count += 1

    if organized_count == 0:
        messagebox.showwarning(
            "No Files Found",
            f"No files found in selected folder.\n\nSelected folder:\n{source_folder}"
        )
    else:
        messagebox.showinfo(
            "Success",
            f"{organized_count} files organized successfully!\n\nOutput:\n{output_folder}"
        )

def merge_pdfs():
    pdf_files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        ]
    )

    if not pdf_files:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")

    if not output_folder:
        return

    output_name = simpledialog.askstring(
        "Output File Name",
        "Enter merged PDF name, example: final_report"
    )

    if not output_name:
        output_name = "merged_file"

    merger = PdfMerger()

    try:
        for pdf in pdf_files:
            merger.append(pdf)

        output_path = os.path.join(output_folder, output_name + ".pdf")
        merger.write(output_path)
        merger.close()

        messagebox.showinfo(
            "Success",
            f"PDFs merged successfully!\n\nSaved as:\n{output_path}"
        )

    except Exception as e:
        messagebox.showerror("Error", f"PDF merge failed:\n{e}")
        
        
def main_window():
    root = tk.Tk()
    root.title("File Automation Tool")
    root.geometry("450x330")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="File Automation Tool",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=30)

    btn1 = tk.Button(
        root,
        text="1. Rename Images",
        font=("Arial", 14),
        width=25,
        command=rename_images
    )
    btn1.pack(pady=10)

    btn2 = tk.Button(
        root,
        text="2. Organize Files",
        font=("Arial", 14),
        width=25,
        command=organize_files
    )
    btn2.pack(pady=10)

    btn3 = tk.Button(
        root,
        text="3. Merge PDFs",
        font=("Arial", 14),
        width=25,
        command=merge_pdfs
    )
    btn3.pack(pady=10)

    root.mainloop()


main_window()