from classes.library import Library
from classes.book import Book
import math

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
    
    def exceeding_days(self, total_days):
        days = 0
        for library in self.libraries:
            n_library_scanned_books = len(set([book.id for book in library.book_list]) &
                            set([book.id for book in self.books if book.library_id == library.id]))
            if n_library_scanned_books > 0:
                days += library.signup_days
                days += (n_library_scanned_books/library.ship_per_day)
        if days <= total_days:
            return int(0)
        else:
            return days - total_days
    
    def is_feasible(self, total_days):
        if self.exceeding_days(total_days) > 0:
            return False
        else:
            return True

    def _remove_last_books(self, exceeding_days):
        removed_books = exceeding_days/int(self.libraries[-1].ship_per_day)
        updated_books = self.books[:-(math.ceil(removed_books))]
        self.books = updated_books

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
    