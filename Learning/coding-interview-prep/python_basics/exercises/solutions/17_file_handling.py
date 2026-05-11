# SOLUTIONS: File Handling
# These are reference solutions — there are often multiple valid ways to solve each problem!

# ===========================================================================
# Problem 1 Solution: Write and Read a File
# ===========================================================================

def write_and_read_file():
    # Write
    with open("/tmp/notes.txt", "w") as f:
        f.write("This is the first note.\n")
        f.write("This is the second note.\n")
        f.write("This is the third note.\n")

    # Read
    with open("/tmp/notes.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            print(f"Line {i}: {line.strip()}")

write_and_read_file()


# ===========================================================================
# Problem 2 Solution: Append to a Log File
# ===========================================================================

from datetime import datetime

def append_to_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

append_to_log("Message 1")
append_to_log("Message 2")
append_to_log("Message 3")

with open("/tmp/log.txt", "r") as f:
    print(f.read())


# ===========================================================================
# Problem 3 Solution: Count Words in a File
# ===========================================================================

def count_words(filename):
    with open(filename, "r") as f:
        text = f.read()
        words = text.split()
        return len(words)

# Create test file
with open("/tmp/test.txt", "w") as f:
    f.write("The quick brown fox jumps over the lazy dog. " +
            "The dog was sleeping in the shade. " +
            "A bird was singing above the tree.")

word_count = count_words("/tmp/test.txt")
print(f"Total words: {word_count}")


# ===========================================================================
# Problem 4 Solution: Search Lines Containing a Keyword
# ===========================================================================

def search_in_file(filename, keyword):
    with open(filename, "r") as f:
        for line in f:
            if keyword.lower() in line.lower():
                print(line.strip())

# Create test file
with open("/tmp/search.txt", "w") as f:
    f.write("I love python\n")
    f.write("Python is great\n")
    f.write("Java is also good\n")
    f.write("python is powerful\n")

search_in_file("/tmp/search.txt", "python")


# ===========================================================================
# Problem 5 Solution: Read and Display CSV Data as Table
# ===========================================================================

def create_and_display_csv():
    # Create CSV file
    with open("/tmp/data.csv", "w") as f:
        f.write("Name,Age,City\n")
        f.write("Alice,25,New York\n")
        f.write("Bob,30,Los Angeles\n")
        f.write("Carol,28,Chicago\n")

    # Read and display as table
    with open("/tmp/data.csv", "r") as f:
        lines = f.readlines()

    # Parse and display
    rows = [line.strip().split(",") for line in lines]

    # Print header with padding
    header = rows[0]
    print(f"{header[0]:<10} {header[1]:>3}  {header[2]}")

    # Print data rows
    for row in rows[1:]:
        print(f"{row[0]:<10} {row[1]:>3}  {row[2]}")

create_and_display_csv()


if __name__ == "__main__":
    print("=== Running all solutions ===")

    print("\nProblem 1:")
    def write_and_read_file():
        with open("/tmp/notes.txt", "w") as f:
            f.write("This is the first note.\n")
            f.write("This is the second note.\n")
            f.write("This is the third note.\n")

        with open("/tmp/notes.txt", "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                print(f"Line {i}: {line.strip()}")

    write_and_read_file()

    print("\nProblem 2:")
    from datetime import datetime

    def append_to_log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/log.txt", "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    append_to_log("Message 1")
    append_to_log("Message 2")
    append_to_log("Message 3")

    with open("/tmp/log.txt", "r") as f:
        print(f.read())

    print("\nProblem 3:")
    def count_words(filename):
        with open(filename, "r") as f:
            text = f.read()
            words = text.split()
            return len(words)

    with open("/tmp/test.txt", "w") as f:
        f.write("The quick brown fox jumps over the lazy dog. " +
                "The dog was sleeping in the shade. " +
                "A bird was singing above the tree.")

    word_count = count_words("/tmp/test.txt")
    print(f"Total words: {word_count}")

    print("\nProblem 4:")
    def search_in_file(filename, keyword):
        with open(filename, "r") as f:
            for line in f:
                if keyword.lower() in line.lower():
                    print(line.strip())

    with open("/tmp/search.txt", "w") as f:
        f.write("I love python\n")
        f.write("Python is great\n")
        f.write("Java is also good\n")
        f.write("python is powerful\n")

    search_in_file("/tmp/search.txt", "python")

    print("\nProblem 5:")
    def create_and_display_csv():
        with open("/tmp/data.csv", "w") as f:
            f.write("Name,Age,City\n")
            f.write("Alice,25,New York\n")
            f.write("Bob,30,Los Angeles\n")
            f.write("Carol,28,Chicago\n")

        with open("/tmp/data.csv", "r") as f:
            lines = f.readlines()

        rows = [line.strip().split(",") for line in lines]

        header = rows[0]
        print(f"{header[0]:<10} {header[1]:>3}  {header[2]}")

        for row in rows[1:]:
            print(f"{row[0]:<10} {row[1]:>3}  {row[2]}")

    create_and_display_csv()
