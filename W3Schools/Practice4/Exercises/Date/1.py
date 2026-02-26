from datetime import date, timedelta

x = date.today()
fivedays = x - timedelta(days=5)
print(fivedays)