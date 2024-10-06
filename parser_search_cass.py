import json

## Открываем файл search_cass.json для чтения с указанием кодировки
#with open('search_cass.json', 'r', encoding='utf-8') as file:
#    data = json.load(file)  # Загружаем JSON данные из файла

with open('shift.json', 'r', encoding='utf-8') as file:
    data = json.load(file)  # Загружаем JSON данные из файла


# Печатаем загруженные данные
for i in range(28):
    print(data['transactions'][i]['shiftNumber'])

