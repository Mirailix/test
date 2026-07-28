# def factorial(n):
#     if n == 0:
#         return 1

#     return n * factorial(n - 1)

# print(factorial(5))


def quick_sort(arr):   # O(n*log(n))
    if len(arr) <= 1:
        return arr
    
    anchor = arr[len(arr) // 2]

    left = [x for x in arr if x < anchor]
    middle = [x for x in arr if x == anchor]
    right = [x for x in arr if x > anchor]

    return quick_sort(left) + middle + quick_sort(right)


numbers = [8, 3, 1, 7, 0, 10, 2, 6 ]

print(quick_sort(numbers))