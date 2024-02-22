from classes.book import Book
from classes.library import Library

class FileReader:

    def read(self, input_file: str):
        with open(input_file, 'r') as file: 
            line = file.readline().split()
            total_books = int(line[0])
            total_libraries = int(line[1])
            total_days = int(line[2])

            book_scores = list(map(int, file.readline().split()))
            books = []
            for id, score in enumerate(book_scores):
                book = Book(id, score)
                books.append(book)

            libraries = {}
            for library_id in range(total_libraries):
                library_params = file.readline().split()
                book_amount = int(library_params[0])
                signup_days = int(library_params[1])
                ship_per_day = int(library_params[2])

                library_books = list(map(int, file.readline().split()))
                book_list = [books[book_id] for book_id in library_books]
                book_list.sort(key=lambda book: book.score, reverse=True)
                
                library = Library(library_id, book_amount, book_list, signup_days, ship_per_day)
                libraries[library_id] = library
        
        return total_books, libraries, total_days
        




    