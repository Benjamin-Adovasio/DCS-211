import string
import random
def randomString(min_length: int, max_length: int) -> str:
    new_string = ""
    length = random.randint(min_length, max_length)
    for i in range(length):
        index = random.randint(0, len(string.ascii_letters)-1)
        new_string = new_string+string.ascii_letters[index]
    return new_string
def listOfRandomStrings(list_min: int, list_max: int) -> list[str]:
    new_list = []
    num_items = random.randint(list_min, list_max)
    for i in range(num_items):
        min_length = random.randint(3,5)
        max_length = random.randint(15,20)
        new_string = randomString(min_length, max_length)
        new_list.append(new_string)
    return new_list
def main():
    print("Testing randomString function:")
    print(randomString(3,10))
    print(randomString(5,12))
    print(randomString(2,14))
    print("Testing listOfRandomStrings function:")
    print(listOfRandomStrings(1,5))
    print(listOfRandomStrings(5,6))
    print(listOfRandomStrings(4,8))