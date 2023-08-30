import os
import json
import glob


class Librarian:
    def __init__(self, root_dir):
        """Initialize with the root directory where book information is stored."""
        self.root_dir = root_dir

    def create_directory(self, path):
        """Create a directory if it doesn't exist."""
        if not os.path.exists(path):
            os.makedirs(path)

    def save_search(self, category, book_title, start_page, end_page, content):
        """Save the searched content in JSON format."""
        # Create the directory path
        directory = (
            f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}"
        )
        self.create_directory(directory)

        # Generate the file name
        json_file_name = f"{directory}/page_range_{start_page}_to_{end_page}.json"

        # Save the content as a JSON file
        with open(json_file_name, "w") as f:
            json.dump(content, f, indent=4)
        print(f"Librarian: Your search has been saved to {json_file_name}")

    def search_exists(self, category, book_title, start_page, end_page):
        """Check if a search for a given page range already exists."""
        json_file_name = f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}/page_range_{start_page}_to_{end_page}.json"
        if os.path.exists(json_file_name):
            print(
                f"Librarian: You've already searched for pages {start_page} to {end_page} in {book_title}."
            )
            return True
        return False

    def save_chapter(self, category, book_title, chapter, content):
        """Save a chapter's content as a JSON file."""
        directory = f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}/chapters"
        self.create_directory(directory)
        json_file_name = f"{directory}/{chapter}.json"

        with open(json_file_name, "w") as f:
            json.dump(content, f, indent=4)
        print(f"Librarian: Chapter {chapter} has been saved in {json_file_name}")

    def organize_into_chapters(self, category, book_title, toc):
        """Combine existing JSONs into chapter-based JSONs using the Table of Contents (TOC)."""
        directory = (
            f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}"
        )
        chapter_directory = f"{directory}/chapters"
        self.create_directory(chapter_directory)

        for chapter, page_range in toc.items():
            chapter_content = {}
            for page_num in range(page_range[0], page_range[1] + 1):
                json_file = f"{directory}/page_range_{page_num}_to_{page_num}.json"
                if os.path.exists(json_file):
                    with open(json_file, "r") as f:
                        content = json.load(f)
                        chapter_content.update(content)

            if chapter_content:
                chapter_file = f"{chapter_directory}/{chapter}.json"
                with open(chapter_file, "w") as f:
                    json.dump(chapter_content, f, indent=4)
                print(f"Librarian: Chapter {chapter} has been organized.")

    def clean_up_book(self, category, book_title):
        """Delete overlapping JSONs that have been organized into chapters."""
        directory = (
            f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}"
        )

        # Loop through all the chapter files to find overlapping pages
        chapter_files = glob.glob(f"{directory}/chapters/*.json")
        for chapter_file in chapter_files:
            with open(chapter_file, "r") as f:
                chapter_content = json.load(f)

            for page_key in chapter_content.keys():
                page_num = int(page_key.replace("Page_", ""))
                json_file = f"{directory}/page_range_{page_num}_to_{page_num}.json"
                if os.path.exists(json_file):
                    os.remove(json_file)
                    print(
                        f"Librarian: Removed overlapping JSON file for Page {page_num}."
                    )

    def save_toc(self, category, book_title, toc):
        """Save the Table of Contents (TOC) as a JSON file."""
        directory = f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}"
        self.create_directory(directory)
        toc_file_name = f"{directory}/TOC_{book_title}.json"
        with open(toc_file_name, "w") as f:
            json.dump(toc, f, indent=4)
        print(f"Librarian: TOC has been saved in {toc_file_name}")
