import socket
import threading
import os
import time
import tkinter
from tkinter import messagebox
from tkinter import filedialog

# create and initialize a udp socket for message exchange
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind(("127.0.0.1", 12001))

# create and initialize a tcp socket for file transfer receival
# both sockets can be bound to the same port
client_rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_rec.bind(("127.0.0.1", 12001))
client_rec.listen()

# application lobby setup
print("===> Dardesh Lobby <=====")
name = input("Enter your name: ")
print("\nType 'quit' to exit.")
print("File transfer supports almost all file types, e.g. image,pdf,audio,text,excel...")
print("The app might take some time to transfer the file depending on the type and size")
print("please wait until the file is fully sent before interacting with the app to avoid a crash")
print("If error is encountered, please restart the app.")

# initialize useful variables
ms = "999990"
# False being a 0 and True being a 1
current_seq = False
new_msg = True
can_send = True
msg = "initializing...0"

# initialize message buffer
ms_queue = []

# packet-making function: wrap message with ack and encode


def makePkt(msg, acknumber):
    pkt = msg+str(int(acknumber))
    pkt = pkt.encode()
    return pkt

# check if ack is received


def isAck(msg, acknumber):
    if len(msg) == 1 and msg[0] == acknumber:
        return True
    else:
        return False

# grab user input from ui


def grab_input(event=None):
    inp = user_input.get()
    ms_queue.append(inp)
    temp = f"{name} : {inp}"
    msg_list.insert(tkinter.END, temp)
    user_input.set("")

# check if a timout had occured (timout set to 3s)


def timeout(timer_start, now, timer_active):
    if not timer_active:
        return False
    if now-timer_start >= 3:
        return True
    return False


def send_file():
    # get file address
    # file_address = input(
    # "please enter 'file_address/file_name.file_extension'\n!only include letters and numbers in the file_name!\n")

    #file_address = user_input.get()
    # user_input.set("")

    top.filename = filedialog.askopenfilename(title="selector")
    file_address = top.filename

    if len(file_address) == 0:

        messagebox.showinfo("Error",
                            "Please enter a valid address")
    else:
        if '/' not in file_address:
            file_name = file_address
        else:
            index = file_address.rfind('/')
            file_name = file_address[index+1:]

        # create a tcp socket to send the file
        client_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to the other peer
        client_send.connect(("127.0.0.1", 12000))

        try:
            # open the file
            file = open(file_address, "rb")
        except:
            messagebox.showinfo("Error",
                                "unsupported file type or invalid address")
        else:
            client_send.send(file_name.encode())

            # read data
            data = file.read(1024)
            while len(data) != 0:
                client_send.send(data)
                data = file.read(1024)
            file.close()
            client_send.send("[done]".encode())

        # closing the tcp connection
        client_send.close()


def rec_file():
    conn, addr = client_rec.accept()

    filename = conn.recv(1024).decode("utf-8")
    index = filename.rfind('.')
    file_name = filename[:index]
    file_extension = filename[index+1:]
    file = open(file_name+' .'+file_extension, "wb+")

    data = conn.recv(1024)
    while True:
        if data != "[done]".encode():
            file.write(data)
            data = conn.recv(1024)
        else:
            file.close()
            break

    msg_list.insert(tkinter.END, "You've received a file")
    conn.close()


# sender
def send():
    # initialize variables
    global can_send
    global current_seq
    timer_active = False
    timer_start = 0

    # start loop
    while True:

        # state 0&2 (send message when there is one)
        if can_send and len(ms_queue) != 0:
            can_send = False
            timer_active = True
            timer_start = time.perf_counter()
            ms = ms_queue.pop(0)
            if ms == "quit":
                top.quit()
                os._exit(1)
            sm = f"{name} : {ms}"
            sm = makePkt(sm, current_seq)
            client_socket.sendto(sm, ("127.0.0.1", 12000))

        # state 1&3 (wait for ack)
        if isAck(msg, str(int(current_seq))):
            current_seq = not current_seq
            can_send = True
            timer_start = time.perf_counter()
            timer_active = False

        if timeout(timer_start, time.perf_counter(), timer_active):
            client_socket.sendto(sm, ("127.0.0.1", 12000))
            timer_active = True
            timer_start = time.perf_counter()


def rec():
    # initialize variables
    global msg
    ex_pkt = False

    # start loop
    while True:
        # check for received messages
        msg = client_socket.recvfrom(1024)[0].decode()
        # if msg is not an ack, check if it is expected then push
        if len(msg) != 1:
            client_socket.sendto(msg[-1].encode(), ("127.0.0.1", 12000))
            if msg[-1] == str(int(ex_pkt)):
                msg_list.insert(tkinter.END, msg[:-1])
                ex_pkt = not ex_pkt


# initialize threads
x1 = threading.Thread(target=send)
x2 = threading.Thread(target=rec)
x3 = threading.Thread(target=rec_file)

# start threads
x1.start()
x2.start()
x3.start()

# initialize gui frame
top = tkinter.Tk()
top.title("Dardesh Lobby")
messages_frame = tkinter.Frame(top)

# initialize and connect widgets
user_input = tkinter.StringVar()
user_input.set("What's on your mind?")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15,
                           width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=user_input)
entry_field.bind("<Return>", grab_input)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=grab_input)
send_button.pack()

file_button = tkinter.Button(top, text="File", command=send_file)
file_button.pack()

tkinter.mainloop()
