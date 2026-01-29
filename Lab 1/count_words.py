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
    filename = "words.txt"
    counts = countWords(filename)
    print(counts)


if __name__ == "__main__":
    main()
