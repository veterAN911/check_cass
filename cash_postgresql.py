import psycopg2

def con_cash(ip,login,pas):
    conn = psycopg2.connect(
        dbname="cash", 
        user=login,
        password=pas,
        host=ip,
        port="5432",
        options="-c client_encoding=UTF8"
    )
    print('Есть подключение к БД')
    return conn

def con_catalog(ip,login,pas):
    conn = psycopg2.connect(
        dbname="catalog", 
        user=login,
        password=pas,
        host=ip,
        port="5432",
        options="-c client_encoding=UTF8"
    )
    return conn

def num_smen_and_fiscalnum(conn,id):
    cursor = conn.cursor()
    query = f"SELECT fiscalnum,numshift FROM public.ch_shift WHERE id = '{id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def num_check_db(conn,id):
    cursor = conn.cursor()
    query = f"SELECT fiscal_doc_id FROM public.ch_purchase WHERE id_shift = '{id}' and fiscal_doc_id IS NOT NULL ORDER BY fiscal_doc_id DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def new_cap_check(id):
    qwery = '''INSERT INTO ch_purchase ("id","datecommit","datecreate","fiscaldocnum","senttoserverstatus","id_session","id_shift","checkstatus","checksumend","checksumstart","currentchecknum","discountvaluetotal",
"id_loyaltransaction","operationtype","id_purchaseref","filename","kpk","spnd","set5checknumber","denyprinttodocuments","client_guid","clienttype","id_main_purchase","inn","vet_inspection","receipt_wide_discount",
"on_day","guid_cashier_work_period","qr_code","fiscal_doc_id","cashoperation","reg_status","reg_data")
(SELECT nextval('hibernate_sequence'),'2021-04-06','2021-04-06','1524;185',2,NULL,\'''' + id + '''\',    -- смена
0,123123,123123,0,0,6076001,'t',NULL,NULL,1273666,34341,NULL,'f',NULL,0,NULL,5047085094,'f',0,NULL,NULL,NULL,NULL,0,NULL,NULL);
'''

def new_check(id):
    new_cap_check(id)

