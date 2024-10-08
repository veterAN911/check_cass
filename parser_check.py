import json

def pars_check():
    with open('check.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  # Загружаем JSON данные из файла
    print("\nСумма чека ", data['ticket']['totalSum'])
    print("\nДата чека ", data['ticket']['transactionDate'])
    for payment in data['ticket']['payments']:
        if payment['sum'] != 0.0:
            print(f"Сумма: {payment['sum']}, Тип оплаты: {payment['paymentType']}")
pars_check()