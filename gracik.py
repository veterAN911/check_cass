import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
import cash_postgresql
import json
import zapros_OFD
import parser_check

def extract_last_value(string):
    parts = string.split('_')
    last_value = parts[-1]
    return last_value

def send_data():
    connOFD = combo.get()
    id = entry1_1.get().strip()
    cash = cash_postgresql.con_cash(entry0.get().strip(), entry1.get().strip(), entry2.get().strip())
    result_num_fiscal = cash_postgresql.num_smen_and_fiscalnum(cash, id)

    with open('OFD', "r") as file:
        data = json.load(file)
    if connOFD == "Fix Price":

        list1 = []
        login = data['fix']['login']
        password = data['fix']['password']
        set_text_to_entry_logi("\nПолучены данные из ОФД")
        last_values = zapros_OFD.search_shift_all(login,password, result_num_fiscal[0],result_num_fiscal[1])
        for i in range(last_values['pagination']['totalItems']):
            last_value = extract_last_value(last_values['transactions'][i]['id'])
            list1.append(last_value)

        set_text_to_entry_logi("\nПолучены данные из базы данных")
        cash = cash_postgresql.con_cash(entry0.get().strip(), entry1.get().strip(), entry2.get().strip())
        check_bd = cash_postgresql.num_check_db(cash, id)
        list2 = [int(item[0]) for item in check_bd]
        list1 = [int(i) for i in list1]
        set1 = set(list1)
        set2 = set(list2)
        set_text_to_entry_logi("\nСверяются данные из ОФД и БД кассы")
        missing_elements = list(set1 - set2)
        if(missing_elements == []):
            messagebox.showinfo("Результат", "Смены сверены с ОФД расхождений нету")
        else:
            answer = messagebox.askquestion("Результат", f"Смены сверены расхождения с ОФД в {len(missing_elements)} чека \n Исправить смену ?")
            if answer == "yes":
                prefix_cass = last_values['transactions'][0]['id'].rsplit('_', 1)[0]
                for i in range(len(missing_elements)):
                    num_check = f"{prefix_cass}_{str(missing_elements[i])}"
                    set_text_to_entry_logi(f"\nФормируем чек {num_check}")
                    check = zapros_OFD.select_ofd_check(num_check)
                    receipt_details =parser_check.pars_check(check)
                    cash = cash_postgresql.con_cash(entry0.get().strip(), entry1.get().strip(), entry2.get().strip())
                    cash_postgresql.new_cap_check(cash,id,receipt_details['data_time'],receipt_details['fiscal'],receipt_details['sum_check'],receipt_details['qr'])
                messagebox.showinfo("Результат", "Отсутствующие чеки сформированны")
            else:
                set_text_to_entry_logi("\nОставляем смену")
    elif connOFD == "Азбука Вкус":
        messagebox.showinfo("Данные по OFD", f"Логин: {data['azbuka']['login']}\nПароль: {data['azbuka']['password']}")

def set_text_to_entry_logi(text):
    entry0_1_1.insert(tk.END, text)

root = tk.Tk()
root.title("Восстановление чеков в смене")
root.geometry("350x150") 

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
entry1_1.insert(0, "15577571")
entry1_1.grid(row=0, column=3)

label1 = tk.Label(frame, text="Логин")
label1.grid(row=1, column=0)

entry0_1_1 = tk.Text(frame, height=8, width=40)
entry0_1_1.insert(tk.END, "Вывод лог файлов:")
entry0_1_1.grid(row=1, column=2, rowspan=2, columnspan=2)
entry0_1_1.configure(font=("Arial", 6))

entry1 = tk.Entry(frame)
entry1.insert(0, "postgres")
entry1.grid(row=1, column=1)

label2 = tk.Label(frame, text="Пароль")
label2.grid(row=2, column=0)

entry2 = tk.Entry(frame)
entry2.insert(0, "postgres")
entry2.grid(row=2, column=1)

button1 = tk.Button(frame, text="Проверить", command=send_data)
button1.grid(row=3, column=1)


label1 = tk.Label(frame, text="Логин")
label1.grid(row=1, column=0)

container = tk.Frame(root)
container.pack(side='bottom', fill='both', expand=True)

combo = Combobox(container)
combo['values'] = ("Fix Price", "Азбука Вкус")
combo.current(0)   
combo.pack(side='right', padx=5)

label_version = tk.Label(container, text="version 1 / 2024 г")
label_version.pack(side='left', padx=5) 

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.mainloop()