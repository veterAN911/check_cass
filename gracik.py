import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
import cash_postgresql
import json
#import zapros_OFD


def send_data():
    #connOFD = combo.get()
    id = entry1_1.get().strip()
    result = cash_postgresql.num_smen(id)
    if result:
        messagebox.showinfo("Результат", f"№ смены: {result}")
        #zapros_OFD.search_shift()
    else:
        messagebox.showinfo("Результат", "Данные не найдены")
    with open('OFD', "r") as file:
        data = json.load(file)
    #if connOFD == "Fix Price":
    #    messagebox.showinfo("Данные по OFD", f"Логин: {data['fix']['login']}\nПароль: {data['fix']['password']}")
    #elif connOFD == "Азбука Вкус":
    #    messagebox.showinfo("Данные по OFD", f"Логин: {data['azbuka']['login']}\nПароль: {data['azbuka']['password']}")

root = tk.Tk()
root.title("Восстановление чеков в смене")
root.geometry("350x150") 

frame = tk.Frame(root)
frame.pack(expand=True)

label0 = tk.Label(frame, text="IP Кассы")
label0.grid(row=0, column=0)

entry0 = tk.Entry(frame)
entry0.insert(0, "10.199.166.3")
entry0.grid(row=0, column=1)

label0_1 = tk.Label(frame, text="id смены")
label0_1.grid(row=0, column=2)

entry1_1 = tk.Entry(frame)
entry1_1.insert(0, "2077432")
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