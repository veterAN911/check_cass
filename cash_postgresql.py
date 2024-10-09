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

def new_cap_check(conn,id,data,fiscal_num,summ_check,qr):
    cursor = conn.cursor()
    zapros_fool_check = f"SELECT numberfield,inn,kpp,id_session FROM ch_purchase WHERE id_shift = '{id}' AND fiscal_doc_id = '{fiscal_num - 1}'"
    cursor.execute(zapros_fool_check)
    general_info = cursor.fetchall()
    creature_check = f'''INSERT INTO ch_purchase ("id","datecommit","datecreate","fiscaldocnum","numberfield","senttoserverstatus","id_session","id_shift","checkstatus","checksumend","checksumstart","currentchecknum","discountvaluetotal",
                        "id_loyaltransaction","operationtype","id_purchaseref","filename","kpk","spnd","set5checknumber","denyprinttodocuments","client_guid","clienttype","id_main_purchase","inn","vet_inspection","receipt_wide_discount",
                        "on_day","guid_cashier_work_period","qr_code","fiscal_doc_id","cashoperation","reg_status","reg_data","kpp")
                        (SELECT nextval('hibernate_sequence'),'{data}','{data}','{fiscal_num};{general_info[0][0] + 1}',{general_info[0][0] + 1},2,{general_info[0][3]},'{id}',
                        0,{summ_check},{summ_check},0,0,-1,'t',NULL,NULL,{fiscal_num},NULL,NULL,'f',NULL,0,NULL,{general_info[0][1]},'f',0,NULL,NULL,'{(qr)}',{fiscal_num},0,NULL,NULL,{general_info[0][2]});'''
    cursor.execute(creature_check)
    conn.commit()
    conn.close()

def new_check(id):
    new_cap_check(id)

