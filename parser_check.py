import json

with open('check.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  # Загружаем JSON данные из файла

def pars_check(data):
    data_time = data['ticket']['transactionDate']
    fiscal = data['ticket']['fiscalDocumentNumber']
    sum_check = int(data['ticket']['totalSum'] * 100)
    qr = data['ticket']['qrCode']

    return {'data_time': data_time, 'fiscal': fiscal, 'sum_check': sum_check,"qr": qr}

def pars_pos(data):
    positions = []
    num_position = 0
    for position in data['ticket']['items']:
        position_name = position['options']['name']
        nds = int(position['taxes'][0]['layout']['rate'] * 100)
        positions.append({'position_name': position_name, 'nds': nds})
    
    return positions
      

    #print("\nСумма чека ", int(data['ticket']['totalSum'] * 100))
    #print("\nNDS чека 10% ", data['ticket']['nds10'])
    #print("\nNDS чека 20% ", data['ticket']['nds20'])
    #print("\nQR чека: ", data['ticket']['qrCode'])
    #for payment in data['ticket']['payments']:
    #    if payment['sum'] != 0.0:
    #        print(f"Сумма: {payment['sum']}, Тип оплаты: {payment['paymentType']}")
    #num_position = 0
    #for position in data['ticket']['items']:
    #    num_position += 1
    #    print(f"Позиция №{num_position}: {position['options']['name']}")

print(pars_pos(data))
