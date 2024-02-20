from helpers.file_reader import FileReader


def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)

    print("total books:", total_books)
    print("libraries:")
    for id in libraries:
        print(f"\t {libraries[id]}")
    print("total days:", total_days)

if __name__ == "__main__":
    solve("data/a_example.in")