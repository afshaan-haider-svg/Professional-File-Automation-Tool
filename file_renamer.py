import os
import shutil

def rename_images():
    source_folder = "input_files/images"
    output_folder = "output_files/renamed_images"

    os.makedirs(output_folder, exist_ok=True)

    prefix = input("Enter new image name prefix, example wedding: ")

    image_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    count = 1

    for file in os.listdir(source_folder):
        old_path = os.path.join(source_folder, file)

        if os.path.isfile(old_path):
            ext = os.path.splitext(file)[1].lower()

            if ext in image_extensions:
                new_name = f"{prefix}_{count}{ext}"
                new_path = os.path.join(output_folder, new_name)

                shutil.copy(old_path, new_path)
                count += 1

    print(f"{count - 1} images renamed successfully.")