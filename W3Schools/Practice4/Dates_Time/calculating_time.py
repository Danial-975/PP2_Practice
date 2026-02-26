from datetime import datetime, timedelta, date

# Разница между двумя датами
date1 = datetime(2024, 1, 1, 10, 30)
date2 = datetime(2024, 1, 5, 15, 45)
difference = date2 - date1

print(f"Разница: {difference}")
print(f"Дней: {difference.days}")
print(f"Секунд: {difference.seconds}")
print(f"Всего секунд: {difference.total_seconds()}")