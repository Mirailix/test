def summa(a,b):
    print(a+b)

def summa(a,b,c):
    print(a*b*c)


# summa(5,6)
summa(5,6,2)

def total(*numbers, extra_numbers): # *args и *kwargs
    count = 0
    for number in numbers:
        count += number
    count += extra_numbers
    print(count)
    
total(1,2,5,23,56,65,2323,1, extra_numbers = 50)

def print_user_info(**kwargs):
    print(kwargs)
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_user_info(name={"Иван","Леха","Яромир"}, age={25,23,13})