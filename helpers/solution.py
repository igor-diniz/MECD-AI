from classes.library import Library
from classes.book import Book

class Solution:
    def __init__(self, libraries: list = [], books: list = []):
        self.libraries = libraries
        self.books = books

    def add_library(self, library: Library):
        if not library.signed_up:
            self.libraries.append(library)
            library.signed_up = True
            return True
        return False

    def add_book(self, book: Book):
        if not book.scanned:
            self.books.append(book)
            book.scanned = True
            return True
        return False

    def evaluate(self):
        return sum(map(lambda book: book.score, self.books))
    
    def is_feasible(self):
        return self.libraries[0].signup_days < self.total_days

    def __le__(self, other_solution):
        return self.evaluate() <= other_solution.evaluate()

    def __str__(self):
        result = ""
        for library in self.libraries:
            result += f"\n\t library_id: {library.id}"
            books_from_library = list(map(lambda book: str(book), 
                                          filter(lambda book: book.library_id == library.id, self.books)
                                        ))
            result += f"\n\t\t books:\n"
            for book in books_from_library:
                result += f"\t\t {str(book)}\n"
            
        result += f"\n\t Total Score: {self.evaluate()}"
        return result
    