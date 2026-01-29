def countWords(filename: str) -> dict[str, int]:
    word_counts: dict[str, int] = {}
    file = open(filename, "r")
    line = file.readline()

    while line != "":
        line = line.strip()
        words = line.split()
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        line = file.readline()

    file.close()
    return word_counts


def main() -> None:
    filename = "data/words.txt"
    counts = countWords(filename)
    print(counts)


if __name__ == "__main__":
    main()

"""
1. Copying a file created 2 identical coppies so the funciton can still read the data.
2. cp is safer because it leave the original file untouched.
3. If the data folder is deleted, the program will not be able to find the file and will raise a FileNotFoundError.
4. The dictionary keys represent words, which are strings. If they were stored as integers, boolens, floats, etc, it would create errors.
"""