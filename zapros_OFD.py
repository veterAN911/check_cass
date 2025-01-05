import requests
import logging
from logging_config import setup_logging

setup_logging()

global_session = None


def authorize(log, pas):
    global global_session
    login_url = 'https://org.1-ofd.ru/api/cp-core/user/login'
    payload = {"login": log, "password": pas}
    session = requests.Session()
    response = session.post(login_url, json=payload)

    if response.status_code == 200:
        print("Авторизация успешна")
        global_session = session
        logging.info(f"Connect ofd session: {session}")
        return session
    else:
        logging.info("ERROR connect OFD")
        return None


def search_cass(factorynum, session):
    searck_cass_url = 'https://org.1-ofd.ru/api/cp-ofd/kkm-groups/filter?extraInfo=lastShift'
    logging.debug(f"Request {searck_cass_url}")
    searck_cass_payload = {"criteria": factorynum, "monitoringFilter": ""}
    response = session.post(searck_cass_url, json=searck_cass_payload)

    data = response.json()
    logging.debug(f"Response {searck_cass_url}")
    return data['subgroups'][0]['retailPlaces'][0]['kkms'][0]['id']


def search_shift_cass_30(cass, session):
    search_shift = f'https://org.1-ofd.ru/api/cp-ofd/kkms/{cass}/transactions?shiftNumber=&transactionTypes=OPEN_SHIFT,CLOSE_SHIFT&page=1&pageSize=30'
    logging.debug(f"Request {search_shift}")
    response = session.get(search_shift)
    data = response.json()
    for i in range(28):
        if data['transactions'][i]['transactionType'] == 'CLOSE_SHIFT':
            print(
                "Найдена смена №",
                data['transactions'][i]['shiftNumber'],
                "номер фискального документа закрытия смены ",
                data['transactions'][i]['fiscalDocumentNumber'])
        else:
            print(
                "Найдена смена №",
                data['transactions'][i]['shiftNumber'],
                "номер фискального документа открытия смены ",
                data['transactions'][i]['fiscalDocumentNumber'])


def search_shift(cass, num_shift, session):
    all_transactions = {"transactions": []}  # Список для хранения всех чеков
    for page in range(1, 100):
        search_shift = f'https://org.1-ofd.ru/api/cp-ofd/kkms/{cass}/transactions?shiftNumber={num_shift}&transactionTypes=BSO,TICKET&page={page}&pageSize=120'
        logging.debug(f"Request {search_shift}")
        response = session.get(search_shift)
        data = response.json()
        logging.debug(f"Response {search_shift}")
        transactions = data.get('transactions', [])
        all_transactions["transactions"].extend(transactions)
        if len(transactions) < 120:  # Если получено меньше 120 чеков, прекращаем запросы
            pagination_data = data["pagination"]
            break
    all_transactions["pagination"] = pagination_data
    logging.debug(f"Refund and search_shift() {all_transactions}")
    return all_transactions


def search_shift_all(log, pas, factorynum, num_shift):
        session = authorize(log, pas)
        if session == None:
            return 'error'
        cass = search_cass(factorynum, session)
        check_num = search_shift(cass, num_shift, session)
        logging.debug(f"Refund and search_shift_all() check_num: ={check_num}")
        return check_num


def select_ofd_check(check):
    zapros = f"https://org.1-ofd.ru/api/cp-ofd/ticket/{check}"
    logging.debug(f"Request {zapros}")
    response = global_session.get(zapros)
    data = response.json()
    logging.debug(f"Response and Refund: {data}")
    return data
