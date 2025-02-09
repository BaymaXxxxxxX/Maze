def recursive_sum(lst):
    if len(lst) == 0:
        return 0  
    return lst[0] + recursive_sum(lst[1:])  

if __name__ == '__main__':
    a = [10, 5, 2, 8, 7]
    x = recursive_sum(a)
    print(x)  
