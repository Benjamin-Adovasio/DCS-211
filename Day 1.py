def addInts(num: int) -> int:
    total = 0
    for i in range(num):
        total += (i+1)
    return total
    
#addInts(5)

import random
from random import randint
from random import randomString
def listOfRandomStrings() -> list[str]:
    new_list = []
    num_items = random.randint(1,5)
    for i in range(num_items):
        string = randomString()
        new_list.append(string)
    return new_list



