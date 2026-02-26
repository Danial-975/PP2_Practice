from datetime import datetime, timedelta

# Current date and time
now = datetime.now()
future_date = now + timedelta(days=5, hours=3, minutes=30)

# Calculate difference
difference = future_date - now
seconds = difference.total_seconds()

print(f"Current date: {now}")
print(f"Future date: {future_date}")
print(f"Difference in seconds: {seconds} seconds")