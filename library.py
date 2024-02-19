class Library:
    def __init__(self, id: int, book_amount: int, book_list: list, signup_days: int, ship_per_day: int):
        self.id = id
        self.book_amount = book_amount
        self.book_list = book_list
        self.signup_days = signup_days
        self.ship_per_day = ship_per_day

    def __str__(self):
        library_print = f"""id: {self.id}
                            book_amount: {self.book_amount}
                            signup_days: {self.signup_days}
                            ship_per_day: {self.ship_per_day}
                        """
        print_books = []
        for book in self.book_list:
            print_books.append(str(book))
        
        library_print += f"    book_list: {print_books}"
        return library_print