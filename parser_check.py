import logging
from logging_config import setup_logging

setup_logging()

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

    return {
        'data_time': data_time,
        'fiscal': fiscal,
        'sum_check': sum_check,
        "qr": qr,
        "paymont": pay}


def pars_pos(data):
    logging.info(f'Parse check in ofd and database {data}\n')
    positions = []
    num_position = 0
    try:
        for position in data['ticket']['items']:
            position_name = position['options']['name'].replace('"', '').replace("'", '')
            num_position += 1
            num_pos = num_position
            nds = int(position['taxes'][0]['layout']['rate'] * 100)
            price_1_pos = position['options']['price']
            price_sum = position['options']['sum']
            lot = int(position['quantity'] * 1000)
            ndssumm_1_pos = int(int(price_1_pos) * int(position['taxes'][0]['layout']['rate'] * 100) / (int(position['taxes'][0]['layout']['rate'] * 100) + 100))
            code = "null"
            subject_code = position.get('subjectCode')
            if subject_code and 'ktGS1M' in subject_code:
                code = subject_code['ktGS1M']
            positions.append({'position_name': position_name,
                              'num_pos': num_pos,
                              'nds': nds,
                              'ndssumm': ndssumm_1_pos,
                              'col': lot,
                              'price': price_1_pos,
                              'summ': price_sum,
                              'subjectCode': code})
    except Exception:
        logging.exception(f"Error {positions}")
    logging.info(f'Parse check GOOD {positions}')
    return positions
