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