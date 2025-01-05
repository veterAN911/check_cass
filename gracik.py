import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
import cash_postgresql
import json
import zapros_OFD
import parser_check
import base64
import os
import logging
from logging_config import setup_logging
from image_base64 import encoded_image

setup_logging()

decoded_image = base64.b64decode(encoded_image)
with open("icon.ico", "wb") as icon_file:
    icon_file.write(decoded_image)
    logging.info("new icon")
def extract_last_value(string):
    parts = string.split('_')
    last_value = parts[-1]
    logging.info("return of the split")
    return last_value


def compare_receipts_in_shift(
        login,
        password,
        cash,
        catalog,
        result_num_fiscal,
        id):
    set_text_to_entry_logi("\nПолучены данные из ОФД")
    logging.info("Data received from the OFD")
    entry0_1_1.yview(tk.END)
    try:
        last_values = zapros_OFD.search_shift_all(
            login, password, result_num_fiscal[0], result_num_fiscal[1])
    except:
        logging.error("An error occurred when connecting to the OFD")
        messagebox.showerror("Error", "Произошла ошибка при подключении к ОФД")        
    list1 = []
    for i in range(last_values['pagination']['totalItems']):
        last_value = extract_last_value(last_values['transactions'][i]['id'])
        list1.append(last_value)
    logging.info("Data was received from the database")
    set_text_to_entry_logi("\nПолучены данные из базы данных")
    entry0_1_1.yview(tk.END)
    check_bd = cash_postgresql.num_check_db(cash, id)
    list2 = [int(item[0]) for item in check_bd]
    list1 = [int(i) for i in list1]
    set1 = set(list1)
    set2 = set(list2)
    logging.info("The data from the OFD and the Yandex.Checkout database are checked.")
    set_text_to_entry_logi("\nСверяются данные из ОФД и БД кассы")
    entry0_1_1.yview(tk.END)
    missing_elements = list(set1 - set2)
    if (missing_elements == []):
        messagebox.showinfo(
            "Результат",
            "Смены сверены с ОФД расхождений нету")
        logging.info("GOOD! Shifts are checked against the OFD, there are no discrepancies")
    else:
        answer = messagebox.askquestion(
            "Результат", f"Смены сверены расхождения с ОФД в {
                len(missing_elements)} чека \n Исправить смену ?")
        logging.info("There are discrepancies!")
        if answer == "yes":
            prefix_cass = last_values['transactions'][0]['id'].rsplit('_', 1)[
                0]
            for i in range(len(missing_elements)):
                num_check = f"{prefix_cass}_{str(missing_elements[i])}"
                set_text_to_entry_logi(f"\nФормируем чек {num_check}")
                logging.debug(f'Receipt formation = {num_check}')
                entry0_1_1.yview(tk.END)
                check = zapros_OFD.select_ofd_check(num_check)
                logging.debug(f'Request to the OFD by receipt = {num_check}')
                receipt_details = parser_check.pars_check(check)
                logging.debug("Сreating a receipt header in the database")
                receipt_pos_details = parser_check.pars_pos(check)
                logging.debug("Creating positions for a cheque")
                cash_postgresql.new_cap_check(
                    cash,
                    catalog,
                    id,
                    receipt_details['data_time'],
                    receipt_details['fiscal'],
                    receipt_details['sum_check'],
                    receipt_details['qr'],
                    receipt_details['paymont'],
                    receipt_pos_details)            
            messagebox.showinfo(
                "Результат", "Отсутствующие чеки сформированны")
            logging.info("Receipt created")
        else:
            set_text_to_entry_logi("\nОставляем смену")
            entry0_1_1.yview(tk.END)


def check_and_create_OFD_file():
    try:
        with open('OFD', "r") as file:
            data = json.load(file)
            logging.info("Open file OFD.json and checking the structure")
        if 'fix' not in data or 'azbuka' not in data:
            messagebox.showerror(
                "Error OFD.json",
                "Неверная структура в файле OFD\nДля исправления просто удалите его и он сформируется по новой")
            logging.error("Incorrect structure in the OFD\file to fix it, simply delete it and it will be formed in a new way")
        if not data['fix']['login'] or not data['fix']['password']:
            messagebox.showerror(
                "Error OFD.json",
                "В файле OFD.json у fix не заполнены login и password")
            
        if not data['azbuka']['login'] or not data['azbuka']['password']:
            messagebox.showerror(
                "Error OFD.json",
                "В файле OFD.json у azbuka не заполнены login и password")
    except FileNotFoundError:
        data = {}
        data['fix'] = {'login': '', 'password': ''}
        data['azbuka'] = {'login': '', 'password': ''}
        with open('OFD', "w") as file:
            json.dump(data, file, indent=2)
        messagebox.showinfo(
            "Внимание",
            "Не закрывая форму заполните сейчас в создавшемся файле OFD.json поля у всех login и password и только после этого нажимай ОК!\nИначе дальнейшая работа     приведёт к ошибкам!")
        logging.critical("Without closing the form, fill it out now in the created MOD file.the json fields are all login and password, and only after that click   OK!\otherwise, further work will lead to errors!")
    return data


def send_data():
    connOFD = combo.get()
    id = entry1_1.get().strip()
    try:
        ofd_data = check_and_create_OFD_file()
        try:
            cash = cash_postgresql.con_cash(
                entry0.get().strip(),
                entry1.get().strip(),
                entry2.get().strip())
            catalog = cash_postgresql.con_catalog(
                entry0.get().strip(), entry1.get().strip(), entry2.get().strip())
            try:
                result_num_fiscal = cash_postgresql.num_smen_and_fiscalnum(cash, id)
                if not all(result_num_fiscal):
                    logging.exception()
                    raise ValueError("Получены пустые значения из базы данных")
                if connOFD == "Fix Price":
                    login = ofd_data['fix']['login']
                    password = ofd_data['fix']['password']
                    try:
                        compare_receipts_in_shift(
                            login, password, cash, catalog, result_num_fiscal, id)
                    except FileNotFoundError as e:
                        logging.exception(f"{e}")
                        messagebox.showerror("Error", f'Возникла ошибка при создание чека: {e}')
                elif connOFD == "Азбука Вкус":
                    login = ofd_data['azbuka']['login']
                    password = ofd_data['azbuka']['password']
                    compare_receipts_in_shift(
                        login, password, cash, catalog, result_num_fiscal, id)
            except Exception as e:
                logging.exception(f"{e}")
                messagebox.showerror("Error", "Вероятно не заполнены все данные в ch_shift или введён некорректный id")    
        except Exception as e:
            logging.exception(f"{e}")
            messagebox.showerror("Error", "Произошла критическая ошибка посмотри логи в parser_log.log")
    except Exception as e:
        logging.exception(f"{e}")
        set_text_to_entry_logi(f"\n Не обрабатываются данные для ОФД{e}")


def set_text_to_entry_logi(text):
    entry0_1_1.insert(tk.END, text)


root = tk.Tk()

root.title("Восстановление чеков в смене")
root.geometry("400x210")
root.iconbitmap("icon.ico")

frame = tk.Frame(root)
frame.pack(expand=True)

label0 = tk.Label(frame, text="IP Кассы")
label0.grid(row=0, column=0)

entry0 = tk.Entry(frame)
entry0.insert(0, "localhost")
entry0.grid(row=0, column=1)

label0_1 = tk.Label(frame, text="id смены")
label0_1.grid(row=0, column=2)

entry1_1 = tk.Entry(frame)
entry1_1.insert(0, "12962541")
entry1_1.grid(row=0, column=3)

label1 = tk.Label(frame, text="Логин")
label1.grid(row=1, column=0)

entry1 = tk.Entry(frame)
entry1.insert(0, "postgres")
entry1.grid(row=1, column=1)

label2 = tk.Label(frame, text="Пароль")
label2.grid(row=2, column=0)

entry2 = tk.Entry(frame)
entry2.insert(0, "postgres")
entry2.grid(row=2, column=1)

button1 = tk.Button(frame, text="Проверить", command=send_data)
button1.grid(row=3, column=0, columnspan=4, sticky='ew')
button1.configure(width=10, height=1)

container = tk.Frame(root)
container.pack(side='bottom', fill='both', expand=True)

entry0_1_1 = tk.Text(frame, height=8, width=40)
entry0_1_1.insert(tk.END, "Вывод лог файлов:")

entry0_1_1.grid(row=4, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
entry0_1_1.configure(font=("Arial", 6))

combo = Combobox(container)
combo['values'] = ("Fix Price", "Азбука Вкус")
combo.current(0)
combo.pack(side='right', padx=5)
label_version = tk.Label(container, text="version 1.2 / 2025 г")
label_version.pack(side='left', padx=5)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

os.remove("icon.ico")
root.mainloop()
