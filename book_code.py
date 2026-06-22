def max(array):
    if not array:
        print(array)
        return None
    if len(array) == 1:
        print(array)
        print('cal:', array[0])
        return array[0]
    if array[0] > max(array[1:]):
        print(array)
        print('cal:', array[0])
        return array[0]
    else:
        print(array)
        print('cal:', array[1:])
        return max(array[1:])

array = [1, 2, 3, 4]

print(max(array))