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
    return result

def num_check_db(conn,id):
    cursor = conn.cursor()
    query = f"SELECT fiscal_doc_id FROM public.ch_purchase WHERE id_shift = '{id}' and fiscal_doc_id IS NOT NULL ORDER BY fiscal_doc_id DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def new_cap_check(conn,conn_catalog,id,data,fiscal_num,summ_check,qr,paymont,data_position):
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
    id_purchase = cursor.fetchone()[0]
    conn.commit()

    for pos in data_position:
        response_s_pos = search_pos(conn_catalog,pos)[0]
        name = pos['position_name']
        NDS = pos['nds']
        sum_nds = pos['ndssumm']
        num_position =  pos['num_pos']
        price_1_pos = pos['price']
        price_sum = pos['summ']
        qentity = pos['col']
        excise_code = pos['subjectCode']

        barcode = response_s_pos[0]
        item = response_s_pos[1]
        ST = response_s_pos[2]
        cat_mask = response_s_pos[3]
        mark_type = response_s_pos[4]
        if mark_type == None:
            mark_type = 'null'

        creature_position = f'''INSERT INTO ch_position (
        "id","barcode","calculatediscount","datecommit",
        "departnumber","inserttype","item","measure_code","name","nds","ndsclass","ndssum","numberfield","priceend","pricestart","product_type",
        "qnty","precision","sumfield","sumdiscount","typepricenumber","id_purchase","category_mask","can_change_qnty","minimal_price_alarm","return_restricted","collapsible","no_actions","fixed_price","excise","raw_string","flags_mask","mark_type","calculation_method") 
        (SELECT nextval('hibernate_sequence'),'{barcode}','t','{data}',1,0,'{item}','{ST}','{name}','{NDS}','NDS','{sum_nds}',{num_position},'{price_1_pos}','{price_1_pos}','ProductPieceEntity',{qentity},1,
        '{price_sum}','0','1',{id_purchase},'{cat_mask}','t','NONE','f','t','f','f','{excise_code}','{excise_code}','0',{mark_type},'4');'''
        print(creature_position)
        cursor.execute(creature_position)
        conn.commit()
        if paymont == 'CARD':
            creature_paymont = f'''INSERT INTO "public"."ch_payment" ("id", "id_basecurrency", "id_currency", "datecommit", "datecreate", "numberfield", "paymenttype", "sumpay", "sumpaybasecurrency", "id_purchase", "successprocessed") 
            VALUES (SELECT nextval('hibernate_sequence'), 'RUB', 'RUB', '{data}', '{data}', 1, 'BankCardPaymentEntity', {price_sum}, {price_sum}, {id_purchase}, 't')'''
            cursor.execute(creature_paymont)
            cursor.execute("SELECT lastval()")
            id_paymont = cursor.fetchone()[0]
            conn.commit()

            creature_payment_transaction = f'''INSERT INTO "public"."ch_payment_transaction" ("id", "cash_num", "discriminator", "create_time", "sumpay", "senttoserverstatus", "filename", "id_purchase", "id_payment", "num_shift", "cash_guid", "shop_index", "annulling")
            VALUES (SELECT nextval('hibernate_sequence'), 4, 'BankCardPaymentEntity', '2024-10-12 23:10:12.094', 29100, 2, NULL, {id_purchase}, {id_paymont}, 190, 1728763812094, 362, 'f')'''
            cursor.execute(creature_payment_transaction)
            cursor.execute("SELECT lastval()")
            id_payment_transaction = cursor.fetchone()[0]
            conn.commit()

            creature_bankcardpayment = f'''INSERT INTO "public"."ch_bankcardpayment" ("authcode", "cardnumber", "cardhash", "cardtype", "cashtransid", "cashtransdate", "hosttransid", "merchantid", "message", "operationcode", "refnumber", "responsecode", "resultcode", "status", "terminalid", "bankid", "banktype") 
            VALUES ('{id_paymont}', '416000', '243892', '************6964', '47FF8E2E5D9D7C651693628984CEDC4990787855', 'Visa', 170010, '2023-09-28 14:41:22.379', NULL, NULL, 'ОДОБРЕНО:', '1', 327150134963, '0', NULL, 't', 29118026) RETURNING *'''
            cursor.execute(creature_bankcardpayment)
            conn.commit()

            creature_bankcardpayment_transaction =  f'''INSERT INTO "public"."ch_bankcardpayment_transaction" ("id", "authcode", "cardnumber", "cardhash", "cardtype", "cashtransid", "cashtransdate", "hosttransid", "merchantid", "message", "operationcode", "refnumber", "responsecode", "currency", "resultcode", "status", "terminalid", "bankid", "banktype") 
            VALUES ({id_payment_transaction}, '243892', '************6964', '47FF8E2E5D9D7C651693628984CEDC4990787855', 'Visa', 170010, '2023-09-28 14:41:22.379', NULL, NULL, 'ОДОБРЕНО:', 1, '327150134963', '0', 'RUB', NULL, 't', '29118026', 'Сбербанк', 1) RETURNING *'''
            cursor.execute(creature_bankcardpayment_transaction)
            conn.commit()
        else:
            creature_paymont = f'''INSERT INTO "public"."ch_payment" ("id", "id_basecurrency", "id_currency", "datecommit", "datecreate", "numberfield", "paymenttype", "sumpay", "sumpaybasecurrency", "id_purchase", "successprocessed") 
            VALUES (SELECT nextval('hibernate_sequence'), 'RUB', 'RUB', '{data}', '{data}', 1, 'CashPaymentEntity', {price_sum}, {price_sum}, {id_purchase}, 't')'''
            cursor.execute(creature_paymont)
            cursor.execute("SELECT lastval()")
            id_paymont = cursor.fetchone()[0]
            conn.commit()

    conn.close()

def search_pos(conn,pos):
    cursor = conn.cursor()
    name_pos, nds = pos['position_name'], pos['nds']
    print(name_pos,nds)
    while True:
        zapros_prod = f"SELECT br.barcode,pr.item,pr.measure_code,pr.category_mask,pr.mark_type FROM cg_product pr JOIN cg_barcode br ON br.product_item = pr.item where pr.name like '%{name_pos}%' and pr.nds = '{nds}' and br.defaultcode = 't' limit 1"
        cursor.execute(zapros_prod)
        result = cursor.fetchall()
        if result:
            break
        else:
            if len(name_pos) > 1:
                name_pos = name_pos[:-1]
            else:
                break
            
    return result