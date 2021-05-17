from socket import *
from tkinter import *
from tkinter import messagebox
import json
import os
host = ''
port = ''
def delete(value):
    if value == 'con':
        con_host_e.delete(0, 'end')
        con_port_e.delete(0, 'end')
    elif value == 'send':
        msg_e.delete('1.0', 'end')
def connect():
    host_data = con_host_e.get()
    port_data = con_port_e.get()
    if len(host_data) and len(port_data) != 0:
        global host
        global port
        host = str(host_data)
        port = int(port_data)
        delete('con')
        messagebox.showinfo('Connection', 'Connected to ' + host + ':' + str(port))
    else:
        messagebox.showerror('ERROR', "You didn't fill anything")
def send():
    name = name_e.get()
    msg = msg_e.get('1.0', 'end')
    if len(name) and len(msg) != 0:
        word = ''
        try:
            num = int(msg)
            word = num+1
        except:
            for i in msg:
                if i.isdigit():
                    word += str(int(i) + 1)
                elif i.isalpha():
                    if i == 'я':
                        word += 'а'
                    elif i == 'Я':
                        word += 'А'
                    elif i == 'z':
                        word += 'a'
                    elif i == 'Z':
                        word += 'A'
                    else:
                        word_n = ord(i)
                        word += chr(word_n + 1)
                else:
                    word += i
        quest = messagebox.askquestion('Sending', 'Message: \n' + msg +  '\nAre you sure to send it?')
        delete('send')
        if quest == 'yes':
            obj = {'name': name, 'msg': word}
            obj_json = json.dumps(obj).encode('utf-8')
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((host, port))
            s.send(obj_json)
            s.close()
            messagebox.showinfo('Sending', 'Message was sent')
        else:
            word = ''
            messagebox.showinfo('Sending', 'Message was deleted')
    else:
        messagebox.showerror('ERROR', "You didn't fill anything")
def decode(msg):
    word = ''
    for i in msg:
        if i.isdigit():
            word += str(int(i) - 1)
        elif i.isalpha():
            if i == 'а':
                word += 'я'
            elif i == 'А':
                word += 'Я'
            elif i == 'a':
                word += 'z'
            elif i == 'A':
                word += 'Z'
            else:
                word_n = ord(i)
                word += chr(word_n - 1)
        else:
            word += i
    return word
def view():
    mes_data = ''
    with open('history.txt', 'r') as history:
        for index, line in enumerate(history):
            hist_data = history.readlines()
        num = 1
        for i in hist_data:
            mes_data += str(num) + ' message: '
            cur_msg = decode(str(i))
            mes_data += cur_msg
            num += 1
        messagebox.showinfo('History', mes_data)
window = Tk()
window.title('Messenger')
title = Label(window, text='Messenger', font=('Verdana', 14), fg='blue')
name_title = Label(window, text='Your name: ')
name_e = Entry(window, width=10, font=('Verdana', 10))
msg_title = Label(window, text='Message: ')
msg_e = Text(window, width=19,height=3, font=('Verdana', 10))
send_but = Button(window, text='Send a message', width=21, command=send)
con_title = Label(window, text='Connection', font=('Verdana', 14), fg='blue')
con_host_title = Label(window, text='IP: ')
con_host_e = Entry(window, width=10, font=('Verdana', 10))
con_port_title = Label(window, text='PORT: ')
con_port_e = Entry(window, width=10, font=('Verdana', 10))
con_but = Button(window, text='Connect', width=21, command=connect)
view_but = Button(window, text='View history of messages', width=21, command=view)
check_var = IntVar()
title.grid(row=0, columnspan=3)
name_title.grid(row=1, column=0)
name_e.grid(row=1, column=1)
msg_title.grid(row=2, columnspan=2)
msg_e.grid(row=3, columnspan=2)
send_but.grid(row=4, columnspan=2)
con_title.grid(row=6, columnspan=3)
con_host_title.grid(row=7, column=0)
con_host_e.grid(row=7, column=1)
con_port_title.grid(row=8, column=0)
con_port_e.grid(row=8, column=1)
con_but.grid(row=9, columnspan=2)
view_but.grid(row=10, columnspan=2)
window.mainloop()
