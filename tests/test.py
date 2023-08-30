import unittest
import pdfplumber


class TestPDFReader(unittest.TestCase):
    def setUp(self):
        self.pdf_path = "./test_book.pdf"
        self.pdf = pdfplumber.open(self.pdf_path)
        self.total_pages = len(self.pdf.pages)

    def tearDown(self):
        self.pdf.close()

    def test_total_pages(self):
        self.assertEqual(self.total_pages, 19)  # Assuming 19 pages in the PDF

    def test_table_of_contents(self):
        # Here, assuming the table of contents is on the first page (index 0)
        page = self.pdf.pages[0]
        content = page.extract_text()
        self.assertIn("Table of Contents", content)

    def test_headers(self):
        # Assuming headers are consistent throughout the PDF
        for i in range(self.total_pages):
            page = self.pdf.pages[i]
            content = page.extract_text()
            self.assertIn("Chapter ", content)

    # Add similar test functions for other features like graphs, definitions, page numbers, etc.
    # Note: pdfplumber mainly focuses on text extraction, so for graphs and other non-text elements, different methods would be needed.


if __name__ == "__main__":
    unittest.main()
