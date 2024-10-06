import psycopg2
import gracik

def con_cash(ip,login,pas):
    conn = psycopg2.connect(
        dbname="cash", 
        user=login,
        password=pas,
        host=ip,
        port="5432",
        options="-c client_encoding=UTF8"
    )
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

cash = con_cash(gracik.entry0.get().strip(),gracik.entry1.get().strip(),gracik.entry2.get().strip())
catalog = con_catalog(gracik.entry0.get().strip(),gracik.entry1.get().strip(),gracik.entry2.get().strip())

def num_smen(id):
    conn = cash
    cursor = conn.cursor()
    query = f"SELECT numshift FROM public.ch_shift WHERE id = '{id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    text_result = str(result[0])
    return text_result

def fiscalnum(ip,login,pas,id):
    conn = psycopg2.connect(
        dbname="cash", 
        user=login,
        password=pas,
        host=ip,
        port="5432",
        options="-c client_encoding=UTF8"
    )
    cursor = conn.cursor()
    query = f"SELECT numshift FROM public.ch_shift WHERE id = '{id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    text_result = str(result[0])
    return text_result
