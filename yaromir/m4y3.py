cache = {1:"леха"}
print(cache)
# multiplier = 2

# def create_tasks():
#     tasks = []
    
#     # Цикл, в котором переменная перекрывает глобальную
#     for multiplier in range(3):
#         def task(x):
#             return x * multiplier  
#         tasks.append(task)

#     def processor(funcs, _cache=cache):
#         results = []
#         for f in funcs:
#             # Вызов функции с аргументом
#             res = f(multiplier)
#             _cache[f.__name__] = res
#             results.append(res)
#         return results

#     return processor(tasks)


# class DataHandler:
#     multiplier = 10
    
#     def __init__(self):
#         self.multiplier = 100

#     def process(self):
#         global multiplier
#         multiplier += 1
#         return self.multiplier + multiplier


# def scope_nesting_trap():
#     val = 10
#     class Nested:
#         val = 20
#         def method(self):
#             nonlocal val  
#             val += 5
#             return val
#     return Nested().method()


# # --- Выполнение кода ---
# print("1. Tasks:", create_tasks())
# print("2. Cache:", cache)

# handler = DataHandler()
# print("3. Handler 1:", handler.process())
# print("4. Handler 2:", handler.process())
# print("5. Global mult:", multiplier)

# print("6. Nesting trap:", scope_nesting_trap())

