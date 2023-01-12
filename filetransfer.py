import socket
from click_shell import shell
from tqdm import tqdm
import os
# from tkinter import Tk
from tkinter.filedialog import  askdirectory ,askopenfilename
os.system('cls')
colors = {
  'reset': '\x1b[0m',
  'bold': '\x1b[1m',
  'italic': '\x1b[3m',
  'underline': '\x1b[4m',
  'inverse': '\x1b[7m',

  'black': '\x1b[30m',
  'red': '\x1b[31m',
  'green': '\x1b[32m',
  'yellow': '\x1b[33m',
  'blue': '\x1b[34m',
  'magenta': '\x1b[35m',
  'cyan': '\x1b[36m',
  'white': '\x1b[37m',
  'gray': '\x1b[90m',
  'bright_red': '\x1b[91m',
  'bright_green': '\x1b[92m',
  'bright_yellow': '\x1b[93m',
  'bright_blue': '\x1b[94m',
  'bright_magenta': '\x1b[95m',
  'bright_cyan': '\x1b[96m',
  'bright_white': '\x1b[97m',

  'bg_black': '\x1b[40m',
  'bg_red': '\x1b[41m',
  'bg_green': '\x1b[42m',
  'bg_yellow': '\x1b[43m',
  'bg_blue': '\x1b[44m',
  'bg_magenta': '\x1b[45m',
  'bg_cyan': '\x1b[46m',
  'bg_white': '\x1b[47m',
  'bg_gray': '\x1b[100m',
  'bg_bright_red': '\x1b[101m',
  'bg_bright_green': '\x1b[102m',
  'bg_bright_yellow': '\x1b[103m',
  'bg_bright_blue': '\x1b[104m',
  'bg_bright_magenta': '\x1b[105m',
  'bg_bright_cyan': '\x1b[106m',
  'bg_bright_white': '\x1b[107m'
}


PORT = 5555
SIZE = 1024

@shell(prompt=">>",intro=f"""
{colors["cyan"]}Greetings 
Welcome to Python file transfer 
hit 'help' to know about all commands or 'instruction' for learn more about the tool
{colors["reset"]}
""")
def main():
    pass

@main.command()
def help():
    print(f'''{colors["yellow"]}
    behost : makes device host 
    beclient : makes device client 
    help : call for help
    instruction : for complete instructions
    about:about me 
    exit : for exit application
    {colors["reset"]}''')

@main.command()
def instruction():
    print(f"""instructions
    {colors["yellow"]}runs on port 5555 make sure the port is free for use to change port use "changeport"(prefer not to change)
    1.make a computer host by using command "behost"
    2.host shows its ip address
    3.make a computer client by using command "beclient"
    4.client ask for host IP address
    5.connection is successfull when both client and host ask for receive send and end command
    6.NOTE first initialize receicing end by typing receive on computer where you want to receive data 
    7.it's default location is downloads folder but you can change it where you want by pressing y 
    8.if  "waiting for data" message appears then configure sending process on other computer by "send" command
    9.it opens a dialog box to select file 
    10.select file and it will automatically send file
    11.progressbar shows the progress of file transfer
    {colors["reset"]}""")

@main.command()
def changeport():
    PORT = int(input("Please enter port(should be same on sender or reciever side)"))

@main.command()
def about():
    print(f"""
    Hey!
    hope you find this program useful
    Download exe file from
        🧾 https://github.com/Lakshit-Karsoliya/python-file-transfer

    Download 👇 source code from 
        🧾 https://github.com/Lakshit-Karsoliya/python-file-transfer

    Connect With Me
        🐈‍⬛ https://github.com/Lakshit-Karsoliya
        📧 lakshitkumar220@outlook.com

    """)

@main.command()
def behost():
    IP = socket.gethostbyname(socket.gethostname())
    print(f"{colors['bright_green']}[HOST]{colors['reset']}host ip: {IP}")
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (IP,PORT)
    server_socket.bind(ADDR)
    server_socket.listen()
    print(f"{colors['bright_green']}[HOST]{colors['reset']}waiting for client to connect")
    conn , addr = server_socket.accept()
    print(f"client connected {addr[0]} {addr[1]}")
    while True:
        command = input(f"{colors['bright_green']}[HOST]{colors['reset']}Enter a command : receive , send , end : ")
        if command == 'end':
            break
        elif command == 'receive':
            print(f"{colors['bright_green']}[HOST]{colors['reset']}Do you want to enter location where to save file Default location is Downloads folder (y/n) : ")
            prompt = input()
            if prompt=='y':
                FILE_PATH = askdirectory(title="select folder location")
                print(FILE_PATH)                
            else:
                FILE_PATH = r'C:/Users/laksh/Downloads'
            print(f'{colors["bright_green"]}[HOST]{colors["reset"]}{colors["yellow"]} waiting for data {colors["reset"]}')
            data = conn.recv(1024).decode()
            item =  data.split("_")
            FILE_NAME , FILE_SIZE = item[0],int(item[1])
            print(f"{colors['bright_green']}[HOST]{colors['reset']}{FILE_NAME} :{FILE_SIZE}")
            conn.send(f'File name and File size are recieved you are clear to send data'.encode())
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
            print(f'{colors["green"]} file received successfully {colors["reset"]}')
        elif command=='send':
            FILE_PATH = askopenfilename()
            FILE_NAME = os.path.basename(FILE_PATH)
            FOLDER_PATH = os.path.dirname(FILE_PATH)
            print(f"{colors['bright_green']}[HOST]{colors['reset']}{FILE_PATH}-{FILE_NAME}")
            FILE_SIZE = os.path.getsize(FILE_PATH)
            data = f"{FILE_NAME}_{FILE_SIZE}"
            conn.send(data.encode())
            bar = tqdm(range(int(FILE_SIZE)),f"Sending {FILE_NAME}",unit="B",unit_scale=True,unit_divisor=SIZE)
            
            with open(FILE_PATH,"rb") as f:
                while True:
                    data = f.read(SIZE)
                    if not data:
                        break
                    conn.send(data)
                    bar.update(len(data))
            conn.send(b"DONE")
            print(f"{colors['bright_green']}[HOST]{colors['reset']}file send successfully")
    conn.close()
    server_socket.close()
@main.command()
def beclient():
    IP = input(f"{colors['bright_green']}[CLIENT]{colors['reset']}Enter ip of HOST ")
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ADDR = (IP,PORT)
    client_socket.connect(ADDR)
    while True:
        command = input(f"{colors['bright_green']}[CLIENT]{colors['reset']}Enter a command : receive , send , end : ")
        if command == 'end':
            break
        elif command == 'receive':
            print(f"{colors['bright_green']}[CLIENT]{colors['reset']}Do you want to enter location where to save file Default location is Downloads folder (y/n) : ")
            prompt = input()
            if prompt=='y':
                FILE_PATH = askdirectory(title="select folder location")
                print(FILE_PATH)                
            else:
                FILE_PATH = r'C:/Users/laksh/Downloads'
            print(f'{colors["yellow"]} waiting for data {colors["reset"]}')
            data = client_socket.recv(1024).decode()
            item =  data.split("_")
            FILE_NAME , FILE_SIZE = item[0],int(item[1])
            print(FILE_NAME , ":",FILE_SIZE)
            bar = tqdm(range(int(FILE_SIZE)),f"Receiving {FILE_NAME}",unit="B",unit_scale=True,unit_divisor=SIZE)
            with open(f"{FILE_PATH}/revived_{FILE_NAME}","wb") as f:
                while True:
                    data = client_socket.recv(SIZE)
                    if data == b"DONE":
                        break
                    if data[len(data)-4::1] == b"DONE":
                        break
                    if not data :
                        break
                    f.write(data)
                    bar.update(len(data))
            print(f'{colors["green"]} file received successfully {colors["reset"]}')

        elif command=='send':
            FILE_PATH = askopenfilename()
            FILE_NAME = os.path.basename(FILE_PATH)
            FOLDER_PATH = os.path.dirname(FILE_PATH)
            print(FILE_PATH,FILE_NAME)
            FILE_SIZE = os.path.getsize(FILE_PATH)
            data = f"{FILE_NAME}_{FILE_SIZE}"
            client_socket.send(data.encode())
            msg = client_socket.recv(SIZE).decode()
            print(f"{msg}")
            bar = tqdm(range(int(FILE_SIZE)),f"Sending {FILE_NAME}",unit="B",unit_scale=True,unit_divisor=SIZE)
            with open(FILE_PATH,"rb") as f:
                while True:
                    data = f.read(SIZE)
                    if not data:
                        break
                    client_socket.send(data)
                    bar.update(len(data))
            client_socket.send(b"DONE")
    client_socket.send("Holle".encode())
    client_socket.close()

if __name__ == '__main__':
    main()