def parseFile(filename):
    word_counts = {}
    file = open(filename, 'r')
    line = file.readline()
    while line != "":
        word=line.strip()
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
        line = file.readline()
    file.close()
    return word_counts
def main():
    print("Test 1: test1.txt")
    print(parseFile("test1.txt"))
    print()

    print("Test 2: test2.txt")
    print(parseFile("test2.txt"))
    print()

    print("Test 3: test3.txt")
    print(parseFile("test3.txt"))
    print()
   
if __name__ == "__main__":
    main()