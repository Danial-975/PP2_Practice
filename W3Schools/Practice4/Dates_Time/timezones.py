from datetime import datetime, timedelta

# Допустим, в Москве сейчас 14:30
moscow_time = datetime(2024, 1, 15, 14, 30)

# Нью-Йорк отстает от Москвы на 8 часов (зимой)
ny_time = moscow_time - timedelta(hours=8)

print(f"Москва: {moscow_time.strftime('%H:%M')}")
print(f"Нью-Йорк: {ny_time.strftime('%H:%M')}")