class Library:
    def __init__(self, id: int, book_amount: int, book_list: list, signup_days: int, ship_per_day: int):
        self.id = id
        self.book_amount = book_amount
        self.book_list = book_list
        self.ship_per_day = ship_per_day
        self.signup_days = signup_days
        self.signed_up = False
        self.total_score = sum([book.score for book in self.book_list])

    def __str__(self):
        books = []
        for book in self.book_list:
            books.append(str(book))

        return f"""id: {self.id}
            book_amount: {self.book_amount}
            signup_days: {self.signup_days}
            ship_per_day: {self.ship_per_day}
            book_list: {books}
        """