# ---------------------------------------------------------
# Library Inventory Manager — Single File Version
# ---------------------------------------------------------

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional
import json
import logging

# ---------------------------------------------------------
# Book Class
# ---------------------------------------------------------
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"   # available / issued

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return asdict(self)

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"


# ---------------------------------------------------------
# Library Inventory Class
# ---------------------------------------------------------
class LibraryInventory:
    def __init__(self, json_path: str = "catalog.json"):
        self.json_path = Path(json_path)
        self.books: List[Book] = []
        self.load()

    def add_book(self, book: Book):
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError("A book with this ISBN already exists!")
        self.books.append(book)
        self.save()

    def search_by_title(self, query: str):
        q = query.lower().strip()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str):
        b = self.search_by_isbn(isbn)
        if not b:
            raise LookupError("Book not found.")
        res = b.issue()
        self.save()
        return res

    def return_book(self, isbn: str):
        b = self.search_by_isbn(isbn)
        if not b:
            raise LookupError("Book not found.")
        res = b.return_book()
        self.save()
        return res

    # ---------- Persistence ----------
    def save(self):
        data = [b.to_dict() for b in self.books]
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not self.json_path.exists():
            self.books = []
            return

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
        except Exception:
            self.books = []


# ---------------------------------------------------------
# CLI Helper Functions
# ---------------------------------------------------------
def input_nonempty(prompt: str):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("⚠ Input cannot be empty!")


# ---------------------------------------------------------
# CLI Menu
# ---------------------------------------------------------
def menu():
    logging.basicConfig(level=logging.INFO)
    inv = LibraryInventory("catalog.json")

    while True:
        print("\n=== Library Inventory Manager ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Books")
        print("6. Exit")

        choice = input("Enter option (1-6): ").strip()

        try:
            if choice == "1":
                title = input_nonempty("Title: ")
                author = input_nonempty("Author: ")
                isbn = input_nonempty("ISBN: ")
                inv.add_book(Book(title, author, isbn))
                print("✔ Book added.")

            elif choice == "2":
                isbn = input_nonempty("ISBN to issue: ")
                if inv.issue_book(isbn):
                    print("✔ Book issued.")
                else:
                    print("✖ Book already issued.")

            elif choice == "3":
                isbn = input_nonempty("ISBN to return: ")
                if inv.return_book(isbn):
                    print("✔ Book returned.")
                else:
                    print("✖ Book was already available.")

            elif choice == "4":
                books = inv.display_all()
                if not books:
                    print("No books in inventory.")
                else:
                    for b in books:
                        print(b)

            elif choice == "5":
                mode = input("Search by (t)itle or (i)sbn? ").strip().lower()
                if mode == "t":
                    q = input_nonempty("Title: ")
                    results = inv.search_by_title(q)
                    if results:
                        for b in results:
                            print(b)
                    else:
                        print("No matching books found.")

                elif mode == "i":
                    isbn = input_nonempty("ISBN: ")
                    b = inv.search_by_isbn(isbn)
                    print(b if b else "No book found.")

                else:
                    print("Invalid search type.")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Enter 1–6.")

        except Exception as e:
            print("Error:", e)


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    menu()
