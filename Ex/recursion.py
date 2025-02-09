def recursive_sum(lst):
    if len(lst) == 0:
        return 0  # Base case: If the list is empty, return 0
    return lst[0] + recursive_sum(lst[1:])  # Recursive step

if __name__ == '__main__':
    a = [10, 5, 2, 8, 7]
    x = recursive_sum(a)
    print(x)  # Output: 32
