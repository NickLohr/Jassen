import socket
import select
import random
import sys

HEADERSIZE = 10
HEADER_LENGTH = 40
SESSIONID_LENGTH = 25
USERID_LENGTH = 5

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)


server_socket.bind((IP, PORT))

server_socket.listen()


sockets_list =[server_socket]

clients = {"Server":{"header":b' 6        ',"data":b"Server","sessionID":"-1"}}
c = {}
cards_set = ['Rosen 6', 'Rosen 7', 'Rosen 8', 'Rosen 9', 'Rosen Banner', 'Rosen Under', 'Rosen Ober', 'Rosen König', 'Rosen As', 'Eichel 6', 'Eichel 7', 'Eichel 8', 'Eichel 9', 'Eichel Banner', 'Eichel Under', 'Eichel Ober', 'Eichel König', 'Eichel As', 'Schilten 6', 'Schilten 7', 'Schilten 8', 'Schilten 9', 'Schilten Banner', 'Schilten Under', 'Schilten Ober', 'Schilten König', 'Schilten As', 'Schellen 6', 'Schellen 7', 'Schellen 8', 'Schellen 9', 'Schellen Banner', 'Schellen Under', 'Schellen Ober', 'Schellen König', 'Schellen As']


cards = {'Rosen 6': 0, 'Rosen 7': 0, 'Rosen 8': 0, 'Rosen 9': 0, 'Rosen Banner': 10, 'Rosen Under': 2, 'Rosen Ober': 3, 'Rosen König': 4, 'Rosen As': 11, 'Eichel 6': 0, 'Eichel 7': 0, 'Eichel 8': 0, 'Eichel 9': 0, 'Eichel Banner': 10, 'Eichel Under': 2, 'Eichel Ober': 3, 'Eichel König': 4, 'Eichel As': 11, 'Schilten 6': 0, 'Schilten 7': 0, 'Schilten 8': 0, 'Schilten 9': 0, 'Schilten Banner': 10, 'Schilten Under': 2, 'Schilten Ober': 3, 'Schilten König': 4, 'Schilten As': 11, 'Schellen 6': 0, 'Schellen 7': 0, 'Schellen 8': 0, 'Schellen 9': 0, 'Schellen Banner': 10, 'Schellen Under': 2, 'Schellen Ober': 3, 'Schellen König': 4, 'Schellen As': 11}
def create_header(msg):
    return f"{len(msg) :< {HEADERSIZE}}".encode("utf-8")

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERSIZE)
      
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        userID = client_socket.recv(USERID_LENGTH)
        sessionID = client_socket.recv(SESSIONID_LENGTH)
     
        return {"header": message_header, "userID": userID,"sessionID": sessionID, "data":client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, expception_sockets = select.select(sockets_list,[],sockets_list)



    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted new connection form {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)
            
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8') }")
            if not message['data'].decode('utf-8')[0]=="/":

                for client_socket in clients:
                   
                    if client_socket != notified_socket:
                        if clients[client_socket]["sessionID"]==user["sessionID"]:
                            print("send")
                            client_socket.send(user["header"]+user["data"]+message["header"]+message["data"])
                        else:
                            print("not in the same chat")

            else:
                print("Special")
                m = message['data'].decode('utf-8')[1:]
                
                print("Message: ", m)
                if user["sessionID"] in c:
                    print("Game erkannt")
                    sessionID = user["sessionID"]
                    game = c[sessionID]
                    t = -1
                    for client_i in range(len(game[9])):
                        if notified_socket == game[9][client_i]:
                            t = client_i
                    if t ==-1:
                        print("Errororororrorororor, player not found")
                        sys.exit()
                    if notified_socket == game[9][game[4]]:                        #checks if the socket at the moment is the one turns it is
                        if m[:5] == "trump":
                            if m[6:] in ["Rosen", "Schilten", "Schellen","Eicheln"]:
                                if c[sessionID][8]!=-1:
                                    msg = b"Trumpf wurde schon gewaehlt"
                                    notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                else:
                                    for client_socket in clients:
                                        
                                        if clients[client_socket]["sessionID"]==user["sessionID"]:
                                            msg = f"Der Trumpf ist {m[6:]}\n"
                                            msg = bytearray(msg,"utf-8")
                                            client_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                            continue
                                c[sessionID][8] = m[6:]
                                continue
                            else:
                                msg = b"Entweder Rosen, Schilten, Schellen oder Eicheln. Z.B /trump Eicheln"
                                notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                continue
                        elif m[:8] == "playcard":
                            print("Playing")
                            if game[8] == -1:
                                msg = b"Waehle zuerst einen Trumpf aus"
                                notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                continue
                            elif m[9:] in game[game[4]]: # check if the cards he wants to play is in his hands
                                c[sessionID][game[4]].remove(m[9:])
                                c[sessionID][5].append(m[9:])
                                for client_socket in clients:
                                    print(clients[client_socket]["data"])
                                    if clients[client_socket]["sessionID"]==user["sessionID"]:
                                        msg = f"Tisch: { ' '.join(c[sessionID][5]) }\n"
                                        msg = bytearray(msg,"utf-8")
                                        client_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                
                                c[sessionID][4]+=1
                                c[sessionID][4]%=4
                                if len(c[sessionID][5]) == 4:
                                    color = c[sessionID][5][0].split(" ")[0]
                                    highest = [c[sessionID][5][0].split(" ")[1], 0,False]
                                    trump = c[sessionID][8]
                                    index = 1
                                    trumped = False
                                    for card in c[sessionID][5][1:]:
                                        if color in card and not trumped:
                                            if highest[0] < card.split(" ")[1]:
                                                highest = [card.split(" ")[1],index,False]
                                        if trump in card:
                                            if not highest[2]:
                                                trumped = True
                                                highest = [card.split(" ")[1],index,True]
                                            else:
                                                if highest[0] < card.split(" ")[1]:
                                                    highest = [card.split(" ")[1],index,True]
                                    p=0
                                    for m in c[sessionID][5]:
                                        p+=cards[m]

                                    if (highest[1]+t)%2==0:

                                        c[sessionID][6]+=p
                                    else:
                                        c[sessionID][7]+=p
                                    c[sessionID][5] = []
                                    c[sessionID][4] = index

                                
                                continue
                                       
                            else:
                                msg = b"Es kann sein, dass du diese Karte nicht besitzt, versuche es nochmals so: /playcard Eicheln 7 oder /playcard Schellen Banner"
                                notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                                continue
                    
                    if m == "mycards":
                        mycards = bytearray(" ".join(game[t]),"utf-8")
                        print("cards?")
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(mycards)+mycards)
                    elif m == "help":
                        msg = b"Hilfe:\n/help fuer die Hilfe\n/trump [Farbe] fuer den Trumpf waehlen\n/playcard [Karte] um eine Karte auf den Tisch zu legen\n/mycards um die eigene Karten anzuschauen"
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                    elif m== "myturn":
                        msg = f"{4-(c[sessionID][4]+t)%4} people are before you"
                        msg = bytearray(msg,"utf-8")
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                    elif m == "points":
                        msg = f"Team 1 has {c[sessionID][6]} points and team 2 has {c[sessionID][7]} points."
                        msg = bytearray(msg,"utf-8")
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                    else:
                        msg = b"Command Not Found!!"
                        
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)

                else:
                    if m == "start":
                        i = 0
                        players = []
                        for client_socket in clients:
                            if clients[client_socket]["sessionID"]==user["sessionID"]:
                                i+=1
                                players.append(client_socket)
                        if i != 4:
                            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(b"Not enough / too many players")+b"Not enough / too many players")
                            print("Not enough / too many players")
                        else:
                            car = list(cards_set)
                            random.shuffle(car)
                            c[user["sessionID"]] = [sorted(car[:9]),sorted(car[9:18]),sorted(car[18:27]),sorted(car[27:]),0, [],0,0,-1,list(players)]
                
            
                    elif m=="help":
                        msg = b"Hilfe:\n/help fuer die Hilfe\n/start um das SPiel zu starten\n/trump [Farbe] fuer den Trumpf waehlen\n/playcard [Karte] um eine Karte auf den Tisch zu legen\n/mycards um die eigene Karten anzuschauen"
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)


    for notified_socket in expception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]


