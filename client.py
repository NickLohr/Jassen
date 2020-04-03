import socket
import select
import errno
import sys 
import tkinter 

window = tkinter.Tk()


textbox = tkinter.Text(window)
textbox.pack()

input_box = tkinter.StringVar()
input_field = tkinter.Entry(window,text=input_box)
input_field.pack(side=tkinter.BOTTOM, fill=tkinter.X)


IP = "127.0.0.1"
PORT = 1234

HEADERSIZE = 10
HEADER_LENGTH = 40

#wqesdfbgujzdtgfbvdcerwfsd
SESSIONID = b""
USERID = b"qedas"


my_username = ""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username1 = my_username.encode("utf-8")

username_header = f"{len(username1):<{HEADERSIZE}}".encode("utf-8")


def Enter_pressed(event):
    global my_username, SESSIONID,username1
    input_get = input_field.get()
    print(1212)
    if not input_get:
        return
    if my_username == "":
        my_username = input_get
        
    elif SESSIONID == b"":
        if len(input_get)==25:
            SESSIONID = input_get.encode("utf-8")
            username1 = my_username.encode("utf-8")
            username_header = f"{len(username1):<{HEADERSIZE}}".encode("utf-8")
            print(username_header +USERID+SESSIONID+ username1, "header1")
            client_socket.send(username_header +USERID+SESSIONID+ username1)
    elif input_get:
        textbox.insert(tkinter.INSERT, '%s > %s\n' % (username1.decode("utf-8"),input_get))
        message = input_get.encode("utf-8")
        message_header = f"{len(message) :< {HEADERSIZE}}".encode("utf-8")
        client_socket.send(message_header+ USERID +SESSIONID+ message)
        input_box.set('')
    input_box.set('')
    return "break"


def revieve_message():
    try:
        while True:
            username_header = client_socket.recv(HEADERSIZE)
            if not len(username_header):
                textbox.insert(tkinter.INSERT,"Connection closed by the server\n")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")
            

            message_header = client_socket.recv(HEADERSIZE)

            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")


            textbox.insert(tkinter.INSERT,f"{username} > {message}\n")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error", str(e))
            sys.exit()
        else:
            pass

    except Exception as e:
        print("General error", str(e))
        sys.exit()
    
    window.after(200,revieve_message)


frame = tkinter.Frame(window) 
input_field.bind("<Return>", Enter_pressed)
frame.pack()

window.after(200,revieve_message)
window.mainloop()
