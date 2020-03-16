import json
import datetime 

with open("browser-history.json", 'r') as file:
    data = json.load(file)

browser_history = data['Browser History']

file_data = []
for i in range(len(browser_history)):
    time_usec = browser_history[i]['time_usec']
    timestamp = (time_usec/1000000)

    date_obj = datetime.datetime.fromtimestamp(timestamp)
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    if year == 2020 and month == 3 and day == 10:
        url = browser_history[i]['url']
        if url.startswith('https://www.youtube.com/watch?v='):
            test_string = f"{url}\n"
            file_data.append(test_string)

with open('output.txt', 'w') as file:
    file.writelines(file_data)

