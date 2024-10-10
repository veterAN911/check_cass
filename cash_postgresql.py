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
    if general_info == []:
        zapros_fool_check = cursor.execute("SELECT numberfield, inn, kpp, id_session FROM ch_purchase ORDER BY id DESC LIMIT 1")
        general_info = cursor.fetchall()
        general_info = [(0, general_info[0][1], general_info[0][2], general_info[0][3])]
    creature_check = f'''INSERT INTO ch_purchase ("id","datecommit","datecreate","fiscaldocnum","numberfield","senttoserverstatus","id_session","id_shift","checkstatus","checksumend","checksumstart","currentchecknum","discountvaluetotal",
                        "id_loyaltransaction","operationtype","id_purchaseref","filename","kpk","spnd","set5checknumber","denyprinttodocuments","client_guid","clienttype","id_main_purchase","inn","vet_inspection","receipt_wide_discount",
                        "on_day","guid_cashier_work_period","qr_code","fiscal_doc_id","cashoperation","reg_status","reg_data","kpp")
                        (SELECT nextval('hibernate_sequence'),'{data}','{data}','{fiscal_num};{general_info[0][0] + 1}',{general_info[0][0] + 1},2,{general_info[0][3]},'{id}',
                        0,{summ_check},{summ_check},0,0,-1,'t',NULL,NULL,{fiscal_num},NULL,NULL,'f',NULL,0,NULL,{general_info[0][1]},'f',0,NULL,NULL,'{(qr)}',{fiscal_num},0,NULL,NULL,{general_info[0][2]});'''
    cursor.execute(creature_check)
    cursor.execute("SELECT lastval()")
    created_id = cursor.fetchone()[0]
    conn.commit()

    #создание позиции 
    #---------------------------------------------------------------


    creature_position = f'''INSERT INTO ch_position (
    "id","barcode","calculatediscount","datecommit",
    "departnumber","inserttype","item","measure_code","name","nds","ndsclass","ndssum","numberfield","priceend","pricestart","product_type",
    "qnty","precision","sumfield","sumdiscount","typepricenumber","id_purchase","category_mask","can_change_qnty","minimal_price_alarm","return_restricted","collapsible","no_actions","fixed_price","raw_string","flags_mask") 
    (SELECT nextval('hibernate_sequence'),'4620004391223','t','2021-01-29 18:16:31',1,0,'1702015' --(SELECT product_item FROM "public"."cg_barcode" WHERE "barcode" = '4620004391223'),
    'ST','хуита_именная' --(SELECT name FROM "public"."cg_product" WHERE "item" = '1702015'),'-1','NDS','0',номер позиции,'123123'--(SELECT price FROM "public"."cg_price" WHERE "product_item" = '1702015'),
    '123123'--(SELECT price FROM "public"."cg_price" WHERE "product_item" = '1702015'),'ProductPieceEntity',1000,1,
    '123123'--(SELECT price FROM "public"."cg_price" WHERE "product_item" = '1702015'),'0','1',198071, -- id_purchase
    '0','t','NONE','f','t','f','f','4620004391223','0');'''


    conn.close()

pos = [{'position_name': 'Молоко СлавКружеваГОСТ 3,2% 973млБЗМЖ 1 2 5 6', 'nds': 10}, {'position_name': 'Молоко СлавКружеваГОСТ 3,2% 973млБЗМЖ', 'nds': 10}, {'position_name': 'Пакет  "Майка" большая', 'nds': 20}, {'position_name': 'Шапка женская ИМП', 'nds': 20}, {'position_name': 'Носки женские ИМП', 'nds': 20}, {'position_name': 'Носки мужские ТТ', 'nds': 20}, {'position_name': 'Органайзер, 27*21*8 см_ИМП', 'nds': 20}, {'position_name': 'Пряники Кольцо 900г Асс', 'nds': 20}]

def search_pos(pos):
    conn = psycopg2.connect(
        dbname="catalog", 
        user='postgres',
        password='postgres',
        host='localhost',
        port="5432",
        options="-c client_encoding=UTF8"
    )
    cursor = conn.cursor()
    for i in pos:
        name_pos, nds = i['position_name'], i['nds']
        while True:
            zapros_prod = f"SELECT * FROM cg_product WHERE name LIKE '%{name_pos}%' AND nds = '{nds}'  LIMIT 1"
            cursor.execute(zapros_prod)
            result = cursor.fetchall()
            if result:
                break
            else:
                if len(name_pos) > 1:
                    name_pos = name_pos[:-1]
                else:
                    break
            

        print(result)
    conn.close()
    return result
    

search_pos(pos)