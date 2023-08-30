from BookInspector import BookInspector
from BookShelfManager import BookShelfManager
from UserInterface import UserInterface
from Librarian import Librarian  # Import Librarian class
import os


def main():
    # Initialize root directory and manager for bookshelves
    base_path = "book_case/book_shelves/"
    manager = BookShelfManager(base_path)

    # Initialize User Interface for interactions
    ui = UserInterface()

    # Initialize Librarian for organizing book searches and directories
    librarian = Librarian("book_case")

    # Step 1: List categories and get user's choice
    categories = manager.list_categories()
    chosen_category = categories[
        ui.get_category_choice(categories) - 1
    ]  # Adjusting for zero-based index

    # Step 2: List available books in chosen category and get user's choice
    pdf_files = manager.list_books_in_category(chosen_category)
    chosen_pdf = pdf_files[
        ui.get_book_choice(pdf_files) - 1
    ]  # Adjusting for zero-based index

    # Step 3: Initialize BookInspector
    pdf_path = os.path.join(base_path, chosen_category, chosen_pdf)
    inspector = BookInspector(
        pdf_path, chosen_category, chosen_pdf.replace(".pdf", ""), librarian
    )  # Pass the librarian object here

    # Step 4: Perform actions based on user's choice
    action = ui.get_user_action()
    if action == 1:
        print(f"Searching for Table of Contents in {chosen_pdf}...")
        toc = inspector.find_table_of_contents(chosen_category, chosen_pdf.replace(".pdf", ""))
        if toc:
            print("Extracted Table of Contents:")
            print(toc[:500])  # Displaying a truncated preview
    elif action == 2:
        start_page = int(input("Enter the start page number: "))
        end_page = int(input("Enter the end page number: "))
        print(
            f"Reading and dumping pages from {start_page} to {end_page} in {chosen_pdf}..."
        )
        inspector.read_page_range_to_json(start_page, end_page)


if __name__ == "__main__":
    main()
