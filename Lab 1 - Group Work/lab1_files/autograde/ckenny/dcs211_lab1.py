def compute_sum(list_: list[int]) -> int:
    ''' function to compute the sum of a list of integers
    Parameters:
        list_: a list of integers
    Returns:
        the integer sum of the list of integers
    '''
    sum_ = 0
    for i in list_:
        sum_ += i
    return sum_

print(compute_sum([0]))

print(compute_sum([1,2]))

print(compute_sum([3,4,5,6,7]))

print(compute_sum([-3,4,5,6,7]))

def compute_product(list_: list[int]) -> int | None:
    ''' function to compute the product of a list of integers
    Parameters:
        list_: a list of integers
    Returns:
        the product sum of the list of integers; if the list is
        empty, we return None
    '''
    if len(list_) == 0: return None
    product = 1
    for i in list_:
        product *= i
    return product

print(compute_product([0]))

print(compute_product([1,2]))

print(compute_product([3,4,5,6,7]))

print(compute_product([-3,4,5,6,7]))


