import os


class BookShelfManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def list_categories(self):
        return [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]

    def list_books_in_category(self, category):
        category_path = os.path.join(self.base_path, category)
        return [f for f in os.listdir(category_path) if f.endswith(".pdf")]

    def list_books(self):
        return [f for f in os.listdir(self.directory_path) if f.endswith(".pdf")]

    def create_folder(self, folder_name):
        folder_path = os.path.join(self.directory_path, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
