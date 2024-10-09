import json

def pars_check():
    with open('check.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  # Загружаем JSON данные из файла
    print("\nДата чека ", data['ticket']['transactionDate'])
    print("\nФискальный номер ", data['ticket']['fiscalDocumentNumber'])
    print("\nNDS чека 10% ", data['ticket']['nds10'])
    print("\nNDS чека 20% ", data['ticket']['nds20'])
    for payment in data['ticket']['payments']:
        if payment['sum'] != 0.0:
            print(f"Сумма: {payment['sum']}, Тип оплаты: {payment['paymentType']}")
    num_position = 0
    for position in data['ticket']['items']:
        num_position += 1
        print(f"Позиция №{num_position}: {position['options']['name']}")
pars_check()