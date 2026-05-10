import os
import shutil

def organize_images_by_format():
    source_folder = "input_files/images"
    output_folder = "output_files/organized_files/Images_By_Format"

    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower().replace(".", "")

            if ext in ["jpg", "jpeg", "png", "webp"]:
                format_folder = os.path.join(output_folder, ext.upper())
                os.makedirs(format_folder, exist_ok=True)

                shutil.copy(file_path, os.path.join(format_folder, file))

    print("Images organized by format successfully.")