class UserInterface:
    def get_category_choice(self, categories):
        print("Available Categories:")
        for idx, category in enumerate(categories, 1):
            print(f"{idx}. {category}")
        choice = int(input("Enter the number of the category you want to inspect: "))
        return choice

    def get_book_choice(self, books):
        print("Available books:")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book}")
        choice = int(input("Enter the number of the book you want to inspect: "))
        return choice

    def get_user_action(self):
        print("\nWhat would you like to do?")
        print("1. Find Table of Contents")
        print("2. Read a range of pages and dump to JSON")
        action = int(input("Enter your choice: "))
        return action
