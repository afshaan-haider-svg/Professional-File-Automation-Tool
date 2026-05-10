import os
import shutil
import hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfMerger
import threading

images_renamed_count = 0
files_organized_count = 0
pdfs_merged_count = 0
files_searched_count = 0
duplicates_found_count = 0

APP_WIDTH = 1180
APP_HEIGHT = 760
FONT = "Segoe UI"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def update_progress(value, text):
    progress_bar.set(value)
    status_label.configure(text=text)
    percent_label.configure(text=f"{int(value * 100)}%")
    app.update_idletasks()

def run_in_thread(target_function):
    thread = threading.Thread(target=target_function)
    thread.daemon = True
    thread.start()
    
    
def rename_images():
    global images_renamed_count

    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")]
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

    total_files = len(files)
    update_progress(0, "Starting image rename...")

    for index, file in enumerate(files, start=1):
        ext = os.path.splitext(file)[1]
        new_path = os.path.join(output_folder, f"{prefix}_{index}{ext}")
        shutil.copy2(file, new_path)
        update_progress(index / total_files, f"Renaming {index} / {total_files}")

    images_renamed_count += total_files
    images_counter.configure(text=str(images_renamed_count))
    update_progress(1, "Images Renamed Successfully ✅")
    messagebox.showinfo("Success", f"{total_files} images renamed successfully!")


def organize_files():
    global files_organized_count

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

    all_files = []
    for root_dir, folders, files in os.walk(source_folder):
        for file in files:
            all_files.append(os.path.join(root_dir, file))

    if not all_files:
        messagebox.showwarning("No Files", "No files found in selected folder.")
        return

    organized_count = 0
    total_files = len(all_files)
    update_progress(0, "Organizing files...")

    for index, file_path in enumerate(all_files, start=1):
        file = os.path.basename(file_path)
        ext = os.path.splitext(file)[1].lower()
        moved = False

        for folder_name, extensions in file_types.items():
            if ext in extensions:
                target_folder = os.path.join(output_folder, folder_name)
                os.makedirs(target_folder, exist_ok=True)

                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    name, extension = os.path.splitext(file)
                    target_path = os.path.join(target_folder, f"{name}_copy{extension}")

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
                target_path = os.path.join(other_folder, f"{name}_copy{extension}")

            shutil.copy2(file_path, target_path)
            organized_count += 1

        update_progress(index / total_files, f"Organizing {index} / {total_files}")

    files_organized_count += organized_count
    files_counter.configure(text=str(files_organized_count))
    update_progress(1, "Files Organized Successfully ✅")
    messagebox.showinfo("Success", f"{organized_count} files organized successfully!")


def merge_pdfs():
    global pdfs_merged_count

    pdf_files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
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
    total_files = len(pdf_files)

    try:
        update_progress(0, "Merging PDFs...")

        for index, pdf in enumerate(pdf_files, start=1):
            merger.append(pdf)
            update_progress(index / total_files, f"Merging PDF {index} / {total_files}")

        output_path = os.path.join(output_folder, output_name + ".pdf")
        merger.write(output_path)
        merger.close()

        pdfs_merged_count += len(pdf_files)
        pdf_counter.configure(text=str(pdfs_merged_count))
        update_progress(1, "PDF Merge Completed ✅")

        messagebox.showinfo("Success", f"PDFs merged successfully!\n\nSaved as:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"PDF merge failed:\n{e}")


def search_files():
    global files_searched_count

    source_folder = filedialog.askdirectory(title="Select Folder to Search")
    if not source_folder:
        return

    keyword = simpledialog.askstring("Search Keyword", "Enter file name keyword, example: invoice")
    if not keyword:
        messagebox.showwarning("Warning", "Search keyword required!")
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder for Search Results")
    if not output_folder:
        return

    search_result_folder = os.path.join(output_folder, "Search_Results")
    os.makedirs(search_result_folder, exist_ok=True)

    all_files = []
    for root_dir, folders, files in os.walk(source_folder):
        for file in files:
            all_files.append(os.path.join(root_dir, file))

    if not all_files:
        messagebox.showwarning("No Files", "No files found in selected folder.")
        return

    keyword = keyword.lower()
    matched_count = 0
    total_files = len(all_files)

    update_progress(0, "Searching files...")

    for index, file_path in enumerate(all_files, start=1):
        file_name = os.path.basename(file_path)

        if keyword in file_name.lower():
            target_path = os.path.join(search_result_folder, file_name)

            if os.path.exists(target_path):
                name, extension = os.path.splitext(file_name)
                target_path = os.path.join(search_result_folder, f"{name}_copy{extension}")

            shutil.copy2(file_path, target_path)
            matched_count += 1

        update_progress(index / total_files, f"Searching {index} / {total_files}")

    files_searched_count += matched_count
    search_counter.configure(text=str(files_searched_count))
    update_progress(1, "Search Completed ✅")

    messagebox.showinfo(
        "Search Completed",
        f"{matched_count} matching files found.\n\nOutput:\n{search_result_folder}"
    )


def get_file_hash(file_path):
    hash_md5 = hashlib.md5()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    except Exception:
        return None


def duplicate_file_finder():
    global duplicates_found_count

    source_folder = filedialog.askdirectory(title="Select Folder to Find Duplicates")
    if not source_folder:
        return

    action = simpledialog.askstring(
        "Action",
        "Type move or delete\n\nmove = move duplicates to folder\ndelete = delete duplicates"
    )

    if not action:
        return

    action = action.lower().strip()

    if action not in ["move", "delete"]:
        messagebox.showwarning("Invalid Action", "Please type only move or delete.")
        return

    move_folder = None

    if action == "move":
        move_folder = filedialog.askdirectory(title="Select Folder to Move Duplicates")
        if not move_folder:
            return

        move_folder = os.path.join(move_folder, "Duplicate_Files")
        os.makedirs(move_folder, exist_ok=True)

    all_files = []
    for root_dir, folders, files in os.walk(source_folder):
        for file in files:
            all_files.append(os.path.join(root_dir, file))

    if not all_files:
        messagebox.showwarning("No Files", "No files found in selected folder.")
        return

    file_hashes = {}
    duplicate_count = 0
    total_files = len(all_files)

    update_progress(0, "Scanning duplicate files...")

    for index, file_path in enumerate(all_files, start=1):
        file_hash = get_file_hash(file_path)

        if file_hash:
            if file_hash in file_hashes:
                duplicate_count += 1

                if action == "delete":
                    os.remove(file_path)

                elif action == "move":
                    file_name = os.path.basename(file_path)
                    target_path = os.path.join(move_folder, file_name)

                    if os.path.exists(target_path):
                        name, extension = os.path.splitext(file_name)
                        target_path = os.path.join(
                            move_folder,
                            f"{name}_duplicate_{duplicate_count}{extension}"
                        )

                    shutil.move(file_path, target_path)

            else:
                file_hashes[file_hash] = file_path

        update_progress(index / total_files, f"Scanning {index} / {total_files}")

    duplicates_found_count += duplicate_count
    duplicate_counter.configure(text=str(duplicates_found_count))
    update_progress(1, "Duplicate Scan Completed ✅")

    messagebox.showinfo(
        "Completed",
        f"{duplicate_count} duplicate files found.\n\nAction performed: {action}"
    )


def clear_status():
    progress_bar.set(0)
    percent_label.configure(text="0%")
    status_label.configure(text="Ready")


def create_stat_card(parent, icon, number, title, color):
    card = ctk.CTkFrame(
        parent,
        width=165,
        height=150,
        corner_radius=16,
        border_width=1,
        border_color="#2b3a4a",
        fg_color="#121b27"
    )
    card.pack(side="left", padx=8)
    card.pack_propagate(False)

    icon_label = ctk.CTkLabel(
        card,
        text=icon,
        width=48,
        height=48,
        corner_radius=24,
        fg_color=color,
        font=(FONT, 22, "bold")
    )
    icon_label.pack(pady=(16, 8))

    number_label = ctk.CTkLabel(
        card,
        text=str(number),
        font=(FONT, 28, "bold"),
        text_color=color
    )
    number_label.pack()

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=(FONT, 13, "bold")
    )
    title_label.pack(pady=(4, 8))

    line = ctk.CTkFrame(card, height=3, fg_color=color, corner_radius=10)
    line.pack(fill="x", padx=10, side="bottom", pady=8)

    return number_label


def create_feature_button(parent, icon, title, desc, color, command):
    btn = ctk.CTkButton(
        parent,
        text=f"{icon}   {title}\n{desc}",
        width=360,
        height=80,
        corner_radius=14,
        fg_color=color,
        hover_color="#2b3a4a",
        anchor="w",
        font=(FONT, 16, "bold"),
        command=command
    )
    btn.pack(padx=10, pady=8)
    return btn


app = ctk.CTk()
app.title("File Automation Tool")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = int((screen_width / 2) - (APP_WIDTH / 2))
y = int((screen_height / 2) - (APP_HEIGHT / 2))
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

app.minsize(1100, 720)
app.resizable(True, True)

main_container = ctk.CTkFrame(app, fg_color="#07111f", corner_radius=0)
main_container.pack(fill="both", expand=True)

sidebar = ctk.CTkFrame(
    main_container,
    width=240,
    corner_radius=0,
    fg_color="#081827"
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = ctk.CTkFrame(
    main_container,
    corner_radius=22,
    fg_color="#101925",
    border_width=1,
    border_color="#243448"
)
content.pack(side="right", fill="both", expand=True, padx=18, pady=18)

logo = ctk.CTkLabel(
    sidebar,
    text="File\nAutomation",
    font=(FONT, 26, "bold")
)
logo.pack(pady=(35, 10))

tagline = ctk.CTkLabel(
    sidebar,
    text="Python Desktop Tool",
    font=(FONT, 15),
    text_color="#8aa8ff"
)
tagline.pack(pady=(0, 25))

nav_items = [
    "🏠  Dashboard",
    "🖼️  Rename Images",
    "📁  Organize Files",
    "📄  Merge PDFs",
    "🔍  Search Files",
    "🛡️  Duplicate Finder",
]

for i, item in enumerate(nav_items):
    nav = ctk.CTkButton(
        sidebar,
        text=item,
        height=46,
        width=200,
        corner_radius=10,
        anchor="w",
        fg_color="#123a8c" if i == 0 else "transparent",
        hover_color="#174ea6",
        font=(FONT, 15, "bold" if i == 0 else "normal")
    )
    nav.pack(pady=5)

about_box = ctk.CTkFrame(
    sidebar,
    corner_radius=16,
    fg_color="#0d2237",
    border_width=1,
    border_color="#1b3f65"
)
about_box.pack(side="bottom", fill="x", padx=18, pady=20)

about_title = ctk.CTkLabel(
    about_box,
    text="ℹ About",
    font=(FONT, 15, "bold"),
    text_color="#4da3ff"
)
about_title.pack(anchor="w", padx=15, pady=(15, 8))

about_text = ctk.CTkLabel(
    about_box,
    text="A Python Desktop Automation\nTool to save your time and\nboost productivity.",
    font=(FONT, 12),
    justify="left"
)
about_text.pack(anchor="w", padx=15, pady=5)

built = ctk.CTkLabel(
    about_box,
    text="Built with ❤️ Python | Tkinter",
    font=(FONT, 11)
)
built.pack(anchor="w", padx=15, pady=(12, 15))

heading = ctk.CTkLabel(
    content,
    text="Welcome to File Automation Tool",
    font=(FONT, 30, "bold")
)
heading.pack(pady=(25, 5))

subtitle = ctk.CTkLabel(
    content,
    text="◆  Select an automation feature below  ◆",
    font=(FONT, 15),
    text_color="#d6e6ff"
)
subtitle.pack(pady=(0, 20))

stats_frame = ctk.CTkFrame(content, fg_color="transparent")
stats_frame.pack(pady=5)

images_counter = create_stat_card(stats_frame, "🖼️", 0, "Images Renamed", "#25c76f")
files_counter = create_stat_card(stats_frame, "📁", 0, "Files Organized", "#2d8cff")
pdf_counter = create_stat_card(stats_frame, "📄", 0, "PDFs Merged", "#8b5cf6")
search_counter = create_stat_card(stats_frame, "🔍", 0, "Search Results", "#ff9900")
duplicate_counter = create_stat_card(stats_frame, "🛡️", 0, "Duplicates Found", "#ff3b6b")

section_title = ctk.CTkLabel(
    content,
    text="◇  Choose an Automation Feature  ◇",
    font=(FONT, 20, "bold")
)
section_title.pack(pady=(28, 10))

feature_grid = ctk.CTkFrame(content, fg_color="transparent")
feature_grid.pack()

left_col = ctk.CTkFrame(feature_grid, fg_color="transparent")
left_col.pack(side="left")

right_col = ctk.CTkFrame(feature_grid, fg_color="transparent")
right_col.pack(side="right")

create_feature_button(
    left_col,
    "🖼️",
    "Rename Images",
    "Bulk rename images with custom name",
    "#1f5fa8",
    command=rename_images
)

create_feature_button(
    right_col,
    "📁",
    "Organize Files",
    "Organize files into folders by type",
    "#188544",
    command=organize_files
)

create_feature_button(
    left_col,
    "📄",
    "Merge PDFs",
    "Merge multiple PDF files into one",
    "#5b2ca0",
    command=merge_pdfs
)

create_feature_button(
    right_col,
    "🔍",
    "Search Files",
    "Search files by name in selected folder",
    "#9a620f",
    command=search_files
)

duplicate_btn = ctk.CTkButton(
    content,
    text="🛡️   Duplicate Finder\nFind duplicate files and choose delete or move",
    width=740,
    height=80,
    corner_radius=14,
    fg_color="#9f173f",
    hover_color="#2b3a4a",
    anchor="w",
    font=(FONT, 16, "bold"),
    command=duplicate_file_finder
)
duplicate_btn.pack(pady=(8, 15))

separator = ctk.CTkFrame(content, height=1, fg_color="#2b3a4a")
separator.pack(fill="x", padx=25, pady=(5, 12))

progress_row = ctk.CTkFrame(content, fg_color="transparent")
progress_row.pack(fill="x", padx=35)

progress_text = ctk.CTkLabel(
    progress_row,
    text="Progress",
    font=(FONT, 14, "bold")
)
progress_text.pack(side="left", padx=(0, 20))

progress_bar = ctk.CTkProgressBar(progress_row, width=650)
progress_bar.pack(side="left", fill="x", expand=True)
progress_bar.set(0)

percent_label = ctk.CTkLabel(
    progress_row,
    text="0%",
    font=(FONT, 14, "bold")
)
percent_label.pack(side="right", padx=(20, 0))

bottom_row = ctk.CTkFrame(content, fg_color="transparent")
bottom_row.pack(fill="x", padx=35, pady=(12, 10))

status_title = ctk.CTkLabel(
    bottom_row,
    text="Status:",
    font=(FONT, 14, "bold")
)
status_title.pack(side="left")

status_label = ctk.CTkLabel(
    bottom_row,
    text="Ready",
    font=(FONT, 14, "bold"),
    text_color="#4ade80"
)
status_label.pack(side="left", padx=10)

clear_btn = ctk.CTkButton(
    bottom_row,
    text="🗑 Clear Status",
    width=140,
    height=38,
    corner_radius=10,
    fg_color="#1f2937",
    hover_color="#374151",
    command=clear_status
)
clear_btn.pack(side="right")

app.mainloop()