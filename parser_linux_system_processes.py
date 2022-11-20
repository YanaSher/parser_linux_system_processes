import subprocess
from datetime import datetime
from collections import defaultdict

process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, universal_newlines=True).stdout.readlines()

users = set()
memory_result = 0
cpu_result = 0
highest_memory = 0
highest_cpu_load = 0
highest_memory_name = ""
highest_cpu_load_name = ""
users_process = defaultdict(int)

for row in process[1:]:
    if row[0] not in users:
        users.add(row.split()[0])
    user_item = row.split()[0]
    users_process[user_item] += 1
    cpu_number = float(row.split()[2])
    memory_number = float(row.split()[3])
    memory_result += memory_number
    cpu_result += cpu_number

    if float(row.split()[3]) >= highest_memory:
        highest_memory = float(row.split()[3])
        highest_memory_name = row.split()[10:][:20]
        highest_memory_name = ' '.join(highest_memory_name)
    if float(row.split()[2]) >= highest_cpu_load:
        highest_cpu_load = float(row.split()[2])
        highest_cpu_load_name = row.split()[10:][:20]
        highest_cpu_load_name = ' '.join(highest_cpu_load_name)

memory_result = round(memory_result, 2)
cpu_result = round(cpu_result, 2)
process_count = sum(dict(users_process).values())

report = [
    f"Отчет о состоянии системы:\n"
    f"Пользователи системы: {users}\n",
    f"Процессов запущенно: {process_count}\n",
    f"Пользовательских процессов: {dict(users_process)}\n",
    f"Всего памяти используется: {memory_result}\n",
    f"Всего CPU используется: {cpu_result}\n",
    f"Больше всего памяти использует: {highest_memory_name}\n",
    f"Больше всего CPU использует: {highest_cpu_load_name}"
]
with open(f"{datetime.today():%d-%m-%Y-%H:%M}-scan.txt", 'w') as fp:
    fp.writelines(report)
for item in report:
    print(item)
