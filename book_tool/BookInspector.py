import pdfplumber
import json
import os
import re


# Define the BookInspector class
class BookInspector:
    # Initialize the BookInspector object with necessary attributes
    def __init__(self, pdf_path, category, book_title, librarian, parsed_toc=None):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pdf_path = pdf_path  # Path to the PDF book
        self.category = category  # Category of the book (e.g., "Math", "Science")
        self.book_title = book_title  # Title of the book
        self.librarian = (
            librarian  # Instance of Librarian class responsible for book management
        )
        self.parsed_toc = parsed_toc  # Parsed Table of Contents (if available)

    def _get_json_path(self, page_num):
        return os.path.join(
            self.root_dir,
            "book_searches",
            "book_shelves",
            self.category,
            self.book_title,
            f"page_range_{page_num}_to_{page_num}.json",
        )

    def read_pdf_page(self, page_num):
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[page_num - 1]  # 0-based index
            content = page.extract_text()
        return content if content else "No text found"
    
    def create_json_from_page_range(self, start_page, end_page):
        page_content = {}
        for i in range(start_page, end_page + 1):
            page_content[f"Page_{i}"] = self.read_pdf_page(i)
        json_path = os.path.join(
            self.root_dir,
            "book_searches",
            "book_shelves",
            self.category,
            self.book_title,
            f"page_range_{start_page}_to_{end_page}.json",
        )
        self._save_json(page_content, json_path)

    def _save_json(self, data, json_file):
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
    

    # Method to find the Table of Contents (TOC) in the PDF
    # I need to make the inspect definition accept a page and then I check that page for the TOC
    # if the page doesn't have the TOC then I move on to the next page and I assume the first 25 pages have the TOC
    # def find_table_of_contents(self, category, book_title):
    #     directory = (
    #         f"{self.root_dir}/book_searches/book_shelves/{category}/{book_title}"
    #     )
    #     toc = {}
    #     toc_pages = []  # To store the numbers of pages likely to contain TOC

    #     for page_num in range(1, 26):  # Looping through the first 25 pages
    #         json_file = f"{directory}/page_range_{page_num}_to_{page_num}.json"

    #         print(f"Checking JSON file: {json_file}")  # Debug print

    #         if os.path.exists(json_file):
    #             with open(json_file, "r") as f:
    #                 content = json.load(f)

    #             print(f"Page {page_num} content: {content}")  # Debug print

    #             # Extracting the content of the specific page from the JSON
    #             page_content = content.get(f"Page_{page_num}", "")

    #             # Splitting the content into lines
    #             lines = page_content.split("\\n")

    #             # Filtering lines that contain a series of dots
    #             dot_lines = [line for line in lines if "...." in line]

    #             print(f"Lines with dots on page {page_num}: {dot_lines}")  # Debug print

    #             # Check if majority of lines contain dots
    #             if len(dot_lines) > len(lines) * 0.5:
    #                 print(f"Page {page_num} likely contains TOC")  # Debug print

    #                 # Regular expression pattern to capture TOC entries
    #                 pattern = r"([\w\s\:\-\.]+)\.{2,}(\d+)"

    #                 # Finding all matches of the pattern in the page content
    #                 matches = re.findall(pattern, page_content)

    #                 if matches:
    #                     toc_pages.append(
    #                         page_num
    #                     )  # Record this page as likely TOC page

    #                     # Initialize variable to keep track of last page number found
    #                     prev_start = 0

    #                     # Loop through each match to extract and validate TOC data
    #                     for match in matches:
    #                         chapter_title, page_start = match
    #                         page_start = int(page_start)

    #                         # Check if page numbers are in increasing order
    #                         if page_start >= prev_start:
    #                             toc[chapter_title.strip()] = page_start
    #                             prev_start = page_start

    #     print(f"Likely TOC found on pages: {toc_pages}")  # Debug print
    #     print(f"Extracted TOC: {toc}")  # Debug print
    #     self.librarian.save_toc(self.category, self.book_title, toc)

    # Method to inspect the entire PDF and return its content as JSON
    # I need to edit this to just check pages it is given and I can use this as a small routine
    def inspect_pdf_content(self):
        pdf_content = {}  # To store the content of each page
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)  # Get the total number of pages in the PDF
            for i in range(total_pages):
                page = pdf.pages[i]
                content = page.extract_text()  # Extract text content from the page
                pdf_content[f"Page_{i + 1}"] = content if content else "No text found"

        # Save the extracted PDF content to a JSON file
        json_file_name = os.path.join(
            "book_json", f"{os.path.basename(self.pdf_path)}.json"
        )
        with open(json_file_name, "w") as f:
            json.dump(pdf_content, f, indent=4)

        return pdf_content

    # Method to read a specific range of pages and save their content to JSON
    # I can use the inspect definition and this can be more custom version that helps other routines
    # it does not need to save the librian can check it and decide to save it
    def read_page_range_to_json(self, start_page, end_page):
        page_content = {}  # To store the content of each page in the range
        with pdfplumber.open(self.pdf_path) as pdf:
            for i in range(start_page, end_page + 1):  # Iterate through the page range
                if i <= len(pdf.pages):
                    page = pdf.pages[i - 1]  # 0-based index
                    page_content[f"Page_{i}"] = page.extract_text()

        # Create directory for saving JSON if it doesn't exist
        directory = (
            f"book_case/book_searches/book_shelves/{self.category}/{self.book_title}"
        )
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the extracted content to a JSON file
        json_file_name = f"{directory}/page_range_{start_page}_to_{end_page}.json"
        with open(json_file_name, "w") as f:
            json.dump(page_content, f, indent=4)

        print(f"Content dumped to {json_file_name}")

    # Method to set a parsed TOC (useful if TOC is parsed externally)
    # Don't know if I need this but I can move something like the TOC parser to do the TOC finding there and this book inspector just inspect things
    def set_parsed_toc(self, parsed_toc):
        self.parsed_toc = parsed_toc

    # Internal method to extract TOC text from the PDF
    def _extract_toc_text(self):
        toc_text = ""  # To store extracted TOC text
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)  # Get the total number of pages in the PDF
            for i in range(total_pages):
                page = pdf.pages[i]
                content = page.extract_text()  # Extract text content from the page
                toc_text += content if content else ""

        return toc_text
