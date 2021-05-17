from socket import *
from tkinter import *
from tkinter import messagebox
import json
import os
directory = os.listdir()
if 'history.txt' in directory:
    print('History loaded')
else:
    print('History created')
    with open('history.txt', 'w') as file:
        file.write('Message history\n')
def decode(msg, name):
    word = ''
    try:
        num = int(msg)
        word = num-1
    except:
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
    messagebox.showinfo('Message', str(word) + '\nBy: ' + name)
host = input('IP >>> ')
port = input('PORT >>> ')
print('Created server ' + host + ':' + port)
s = socket(AF_INET, SOCK_STREAM)
s.bind((host, int(port)))
s.listen(1)
while True:
    conn, addr = s.accept()
    encoding_data = conn.recv(1024)
    decoding_data = encoding_data.decode('utf-8')
    data = json.loads(decoding_data)
    name = data['name']
    msg = data['msg']
    with open('history.txt', 'a') as file:
        file.write(str(msg) + '\n')
    window = Tk()
    window.wm_withdraw()
    quest = messagebox.askquestion('New message', 'You got a new message!\n\n\n' + str(msg) + '\nBy: ' + str(name)+'\n\n\nNeed to decode it?')
    if quest == 'yes':
        decode(msg, name)
    else:
        messagebox.showinfo('Message', msg + '\nBy: ' + name)
    conn.close()
