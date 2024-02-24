class Book:
    def __init__(self, id: int, score: int):
        self.id = id
        self.score = score
        self.library_id = None
        self.scanned = False

    def reset(self):
        self.library_id = None
        self.scanned = False

    def __str__(self):
        return f"(id: {self.id}, score: {self.score}, library_id: {self.library_id}, scanned: {self.scanned})"
    
    def __eq__(self, other_book) -> bool:
        return self.id == other_book.id

