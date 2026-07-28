from datetime import datetime
current_time = datetime.now()

print("Текущее время:", current_time)

formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
print("Форматированное время:", formatted_time)
print("Год:", current_time.year)
print("Месяц:", current_time.month)
print("День:", current_time.day)
print("Часы:", current_time.hour)
print("Минуты:", current_time.minute)
print("Секунды:", current_time.second)
print("Микросекунды:", current_time.microsecond)
print("Номер недели: ", current_time.isocalendar()[1])