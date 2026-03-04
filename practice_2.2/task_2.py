import psutil
import time

for _ in range(1, 5):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/")
    print(f"1. Загруженность CPU: {cpu}%")
    print(f"2. Использование RAM: {ram}%")
    print(f"3. Загруженность диска: {disk.percent}%")
    time.sleep(1.2)

print("Конец измерения")
