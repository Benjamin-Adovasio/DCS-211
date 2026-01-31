def parseWords(filename: str) -> Dict[str, List[int]]:
    words_dict: Dict[str, List[int]] = {}

    with open(filename, "r") as input_file:
        line = input_file.readline()
        while line != "":
            for char in string.punctuation:
                line = line.replace(char, "")
            words = line.split()
            for word in words:
                key = word.lower()

                if key not in word_dict:
                    word_dict[key] = [0, 0]

                if word[0].isupper():
                    word_dict[key][0] += 1
                
                else:
                    word_dict[key][1] += 1

            line = input_file.readline()

    return word_dict

def histCaseSensitive(word_dict: Dict[str, List[int]]) -> None:

    keys = list(word_dict.keys())
    uppers = [word_dict[word][0] for word in keys]
    lowers = [word_dict[word][1] for word in keys]

    plt.simple_stacked_bar(keys, [uppers, lowers], width=80)
    plt.show()

def histCaseInsensitive(word_dict: Dict[str, List[int]]) -> None:

    keys = list(word_dict.keys())
    totals = [sum(word_dict[word]) for word in keys]

    plt.simple_bar(keys, totals, width=80)
    plt.show()


def main() -> None:

    """
    Main function to call other functions. Functions can also be called directly from terminal.
    """

    print("=== Test File 1 ===")
    d1 = parseWords("test1.txt")
    print(d1)
    histCaseSensitive(d1)
    histCaseInsensitive(d1)

    print("=== Test File 2 ===")
    d2 = parseWords("test2.txt")
    print(d2)
    histCaseSensitive(d2)
    histCaseInsensitive(d2)

    print("=== Test File 3 ===")
    d3 = parseWords("test3.txt")
    print(d3)
    histCaseSensitive(d3)
    histCaseInsensitive(d3)


if __name__ == "__main__":
    main()