from tkinter import *
import socket
import threading
from tkinter import ttk
from tkinter.filedialog import  askdirectory ,askopenfilename
import os
from tqdm.tk import tqdm
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


PORT = 5555
SIZE = 1024
ready = False
ready_to_send = False
# client always send ie sender become client
# server always receive ie receiver becme server
def gethostip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.0.0.0', 0)) 
    return str(s.getsockname()[0])

def help2():
    global ready_to_send
    ready_to_send = True
def help1():
    global ready
    ready=True

def send_file():
    root.title('PyshareCLIENT')
    global ready
    global ready_to_send
    main_frame.pack_forget()
    sender_frame_1.pack()
    count = 0
    while ready==False:
        count+=1
    IP = sender_frame_1_ip.get()
    sender_frame_1_lbl.config(text='Enter ip of host')
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (IP,PORT)
    client_socket.connect(ADDR)
    sender_frame_1_lbl.config(text='Connected')
    sender_frame_1_connect_btn.pack_forget()
    sender_frame_1_ip.pack_forget()
    # sending of files is handled in this section
    FILE_PATH = askopenfilename()
    FILE_NAME = os.path.basename(FILE_PATH)
    FILE_SIZE = os.path.getsize(FILE_PATH)
    data = f"{FILE_NAME}_{FILE_SIZE}"
    sender_frame_1_send_file_btn.pack(pady=10)
    client_socket.send(data.encode())
    while ready_to_send == False:
        count+=1
    bar = tqdm(range(int(FILE_SIZE)),f"Sending {FILE_NAME}",unit="B",unit_scale=True,unit_divisor=SIZE)
    with open(FILE_PATH,"rb") as f:
        while True:
            data = f.read(SIZE)
            if not data:
                break
            client_socket.send(data)
            bar.update(len(data))
    client_socket.send(b"DONE")
    client_socket.close()
    sender_frame_1.pack_forget()
    main_frame.pack()
    ready_to_send = False
    ready = False
    
def receive_file():
    root.title('PyshareHOST')
    main_frame.pack_forget()
    receive_frame_1.pack()
    IP = gethostip()
    # IP = socket.gethostbyname(socket.gethostname())
    #IP = '192.168.246.200'
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (IP,PORT)
    server_socket.bind(ADDR)
    receive_frame_1_lbl.config(text=f'IP = {IP}\nserver is listening\n')
    server_socket.listen()
    conn , addr = server_socket.accept()
    receive_frame_1_lbl.config(text=f'client connected\n{addr[0]} {addr[1]}')
    # receiving of file handled in this section 
    FILE_PATH = askdirectory(title="select folder location where you want to receive file")
    data = conn.recv(1024).decode()
    item =  data.split("_")
    FILE_NAME , FILE_SIZE = item[0],int(item[1])
    bar = tqdm(range(int(FILE_SIZE)),f"Receiving {FILE_NAME}",unit="B",unit_scale=True,unit_divisor=SIZE)
    with open(f"{FILE_PATH}/revived_{FILE_NAME}","wb") as f:
        while True:
            data = conn.recv(SIZE)
            if data == b"DONE":
                break
            if data[len(data)-4::1] == b"DONE":
                break
            if not data:
                break
            f.write(data)
            bar.update(len(data))
    receive_frame_1.pack_forget()
    main_frame.pack()
    
def on_enter(e,button):
   button.config(background='OrangeRed3', foreground= "white")

def on_leave(e,button):
   button.config(background= 'lightgray', foreground= 'black')

root = Tk()
root.geometry('300x300')
root.resizable(0,0)
root.title('PyShare')

main_frame = Frame(root)
label = Label(main_frame,text = 'Welcome to \n PyShare',font=('Helvetica 13 bold'))
label.grid(column=0,row=0,columnspan=2,pady=40)
send_btn = Button(main_frame,text='SEND',border=0,bg='lightgray',width=10,font=('Helvetica 10'),command=lambda:threading.Thread(target=send_file).start())
send_btn.grid(column=0,row=1,padx=10,)
receive_btn = Button(main_frame,text='RECEIVE',border=0,bg='lightgray',width=10,font=('Helvetica 10'),command=lambda:threading.Thread(target=receive_file).start())
receive_btn.grid(column=1,row=1,padx=10)
send_btn.bind('<Enter>', lambda e:on_enter(e,send_btn))
send_btn.bind('<Leave>', lambda e:on_leave(e,send_btn))
receive_btn.bind('<Enter>', lambda e:on_enter(e,receive_btn))
receive_btn.bind('<Leave>', lambda e:on_leave(e,receive_btn))
main_frame.pack()

receive_frame_1 = Frame(root)
receive_frame_1_lbl = Label(receive_frame_1,font=('Helvetica 13'))
receive_frame_1_lbl.pack(pady=10)

sender_frame_1 = Frame(root)
sender_frame_1_lbl = Label(sender_frame_1,text = "Enter ip of host",font=('Helvetica 13'))
sender_frame_1_lbl.pack(pady=10)
sender_frame_1_ip = Entry(sender_frame_1,border=1)
sender_frame_1_ip.pack(pady=5)
sender_frame_1_connect_btn = Button(sender_frame_1,text='connect',border=0,bg='lightgray',width=10,font=('Helvetica 10'),command=help1)
sender_frame_1_connect_btn.pack(pady=10)
sender_frame_1_send_file_btn = Button(sender_frame_1,text='SEND',border=0,bg='lightgray',width=10,font=('Helvetica 10'),command=help2)
sender_frame_1_connect_btn.bind('<Enter>', lambda e:on_enter(e,sender_frame_1_connect_btn))
sender_frame_1_connect_btn.bind('<Leave>', lambda e:on_leave(e,sender_frame_1_connect_btn))
sender_frame_1_send_file_btn.bind('<Enter>', lambda e:on_enter(e,sender_frame_1_send_file_btn))
sender_frame_1_send_file_btn.bind('<Leave>', lambda e:on_leave(e,sender_frame_1_send_file_btn))


root.mainloop()
