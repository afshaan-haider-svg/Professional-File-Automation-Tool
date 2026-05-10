import os
import shutil

def organize_files():
    source_folder = "input_files/mixed_files"
    output_folder = "output_files/organized_files"

    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".webp"],
        "PDFs": [".pdf"],
        "Documents": [".docx", ".doc", ".txt"],
        "Excel": [".xlsx", ".xls", ".csv"],
        "Videos": [".mp4", ".mkv", ".avi"]
    }

    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            moved = False

            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(output_folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    shutil.copy(file_path, os.path.join(target_folder, file))
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(output_folder, "Others")
                os.makedirs(other_folder, exist_ok=True)
                shutil.copy(file_path, os.path.join(other_folder, file))

    print("Files organized successfully.")