
import json

#with open('check.json', 'r', encoding='utf-8') as file:

#        data = json.load(file)  # Загружаем JSON данные из файла

def pars_check(data):
    data_time = data['ticket']['transactionDate']
    fiscal = data['ticket']['fiscalDocumentNumber']
    sum_check = int(data['ticket']['totalSum'] * 100)
    qr = data['ticket']['qrCode']
    payments = data['ticket']['payments']
    for payment in payments:
         if payment['sum'] != 0.0:
              pay = payment['paymentType']
              break

    return {'data_time': data_time, 'fiscal': fiscal, 'sum_check': sum_check,"qr": qr, "paymont": pay}

def pars_pos(data):
    positions = []
    num_position = 0
    for position in data['ticket']['items']:
        position_name = position['options']['name']
        num_position += 1
        num_pos = num_position
        nds = int(position['taxes'][0]['layout']['rate'] * 100)
        ndssumm = price_1_pos = position['options']['ndsSum']
        price_1_pos = position['options']['price']
        price_sum = position['options']['sum']
        lot = int(position['quantity'] * 1000)
        code = "null"
        subject_code = position.get('subjectCode')
        if subject_code and 'ktGS1M' in subject_code:
            code = subject_code['ktGS1M']
        positions.append({'position_name': position_name, 'num_pos': num_pos, 'nds': nds, 'ndssumm': ndssumm, 'col': lot, 'price': price_1_pos, 'summ': price_sum, 'subjectCode': code})
    
    return positions