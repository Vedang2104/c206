import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None
screen_height = None

mouse = Controller()


def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])

def recvMessege(client_socket):
    global mouse
    while True:
        try:
            messege=client_socket.recv(2048).decode()
            if(messege):
                new_messege=eval(messege)
                if (new_messege["data"]=='left_click'):
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                elif (new_messege["data"]=='right_click'):
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                else:
                    xpos=new_messege["data"][0]*screen_width
                    ypos=screen_height*(1-(new_messege["data"][1]-0.2)/0.6)
                    mouse.position=(int(xpos),int(ypos))
        except Exception as error:
            pass

def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()

        print(f"Connection established with {client_socket} : {addr}")
        thread1=Thread(target=recvMessege,args=(client_socket))
        thread1.start()

def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    getDeviceSize()
    acceptConnections()

setup()
