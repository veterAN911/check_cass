import requests
import time
import json

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
        return session
    else:
        print("Авторизация не удалась")
        return None


def search_cass(factorynum, session):
    # URL для POST запроса авторизации
    searck_cass_url = 'https://org.1-ofd.ru/api/cp-ofd/kkm-groups/filter?extraInfo=lastShift'
    searck_cass_payload = {"criteria": factorynum, "monitoringFilter": ""}
    response = session.post(searck_cass_url, json=searck_cass_payload)

    data = response.json()
    return data['subgroups'][0]['retailPlaces'][0]['kkms'][0]['id']


def search_shift_cass_30(cass, session):
    search_shift = f'https://org.1-ofd.ru/api/cp-ofd/kkms/{cass}/transactions?shiftNumber=&transactionTypes=OPEN_SHIFT,CLOSE_SHIFT&page=1&pageSize=30'
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
        response = session.get(search_shift)
        data = response.json()
        transactions = data.get('transactions', [])
        all_transactions["transactions"].extend(transactions)
        if len(transactions) < 120:  # Если получено меньше 120 чеков, прекращаем запросы
            pagination_data = data["pagination"]
            break
    all_transactions["pagination"] = pagination_data
    return all_transactions


def search_shift_all(log, pas, factorynum, num_shift):
        session = authorize(log, pas)
        if session == None:
            return 'error'
        cass = search_cass(factorynum, session)
        check_num = search_shift(cass, num_shift, session)
        return check_num


def select_ofd_check(check):
    zapros = f"https://org.1-ofd.ru/api/cp-ofd/ticket/{check}"
    response = global_session.get(zapros)
    data = response.json()
    return data
