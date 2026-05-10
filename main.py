from file_renamer import rename_images
from file_mover import organize_files
from pdf_merger import merge_pdfs
from image_organizer import organize_images_by_format

def main():
    while True:
        print("\n===== File Automation Tool =====")
        print("1. Rename Images")
        print("2. Organize Mixed Files")
        print("3. Merge PDFs")
        print("4. Organize Images by Format")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            rename_images()

        elif choice == "2":
            organize_files()

        elif choice == "3":
            merge_pdfs()

        elif choice == "4":
            organize_images_by_format()

        elif choice == "5":
            print("Program closed.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()