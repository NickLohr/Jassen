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


cards = {'Rosen 6': [0,6], 'Rosen 7': [0,7], 'Rosen 8': [0,8], 'Rosen 9': [0,9], 'Rosen Banner': [10,10], 'Rosen Under': [2,11], 'Rosen Ober': [3,12], 'Rosen König': [4,13], 'Rosen As': [11,14], 'Eichel 6': [0,6], 'Eichel 7': [0,7], 'Eichel 8': [0,8], 'Eichel 9': [0,9], 'Eichel Banner': [10,10], 'Eichel Under': [2,11], 'Eichel Ober': [3,12], 'Eichel König': [4,13], 'Eichel As': [11,14], 'Schilten 6': [0,6], 'Schilten 7': [0,7], 'Schilten 8': [0,8], 'Schilten 9': [0,9], 'Schilten Banner': [10,10], 'Schilten Under': [2,11], 'Schilten Ober': [3,12], 'Schilten König': [4,13], 'Schilten As': [11,14], 'Schellen 6': [0,6], 'Schellen 7': [0,7], 'Schellen 8': [0,8], 'Schellen 9': [0,9], 'Schellen Banner': [10,10], 'Schellen Under': [2,11], 'Schellen Ober': [3,12], 'Schellen König': [4,13], 'Schellen As': [11,14]}
class JassApp():
    def __init__(self,players,sessionID):
        self.cards = {'Rosen 6': 0, 'Rosen 7': 0, 'Rosen 8': 0, 'Rosen 9': 0, 'Rosen Banner': 10, 'Rosen Under': 2, 'Rosen Ober': 3, 'Rosen König': 4, 'Rosen As': 11, 'Eichel 6': 0, 'Eichel 7': 0, 'Eichel 8': 0, 'Eichel 9': 0, 'Eichel Banner': 10, 'Eichel Under': 2, 'Eichel Ober': 3, 'Eichel König': 4, 'Eichel As': 11, 'Schilten 6': 0, 'Schilten 7': 0, 'Schilten 8': 0, 'Schilten 9': 0, 'Schilten Banner': 10, 'Schilten Under': 2, 'Schilten Ober': 3, 'Schilten König': 4, 'Schilten As': 11, 'Schellen 6': 0, 'Schellen 7': 0, 'Schellen 8': 0, 'Schellen 9': 0, 'Schellen Banner': 10, 'Schellen Under': 2, 'Schellen Ober': 3, 'Schellen König': 4, 'Schellen As': 11}
        self.cards_set = list(cards.keys())
        self.players = players
        self.turn = random.randint(0,3)
        self.table = []
        self.trumpf = -1
        self.sessionID = sessionID
        self.points = [0,0]
        random.shuffle(self.cards_set)
        self.playingcards = [sorted(self.cards_set[:9]),sorted(self.cards_set[9:18]),sorted(self.cards_set[18:27]),sorted(self.cards_set[27:])]

    def trump(self,farbe):
        if farbe in ["Rosen", "Schilten", "Schellen","Eicheln"]:
            if self.trumpf!=-1:
                msg = b"Trumpf wurde schon gewaehlt"
                notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
            else:
                for client_socket in clients:
                    if clients[client_socket]["sessionID"]==self.sessionID:
                        msg = f"Der Trumpf ist {m[6:]}\n"
                        msg = bytearray(msg,"utf-8")
                        client_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                
            self.cards[farbe+"Under"]= [20,20]
            self.cards[farbe+" 9"] = [14,15]
            self.trumpf = farbe
            return
        else:
            msg = b"Entweder Rosen, Schilten, Schellen oder Eicheln. Z.B /trump Eicheln"
            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
            return

    def playcard(self, card):
        if self.trumpf == -1:
            msg = b"Waehle zuerst einen Trumpf aus"
            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
            return
        elif card in self.playingcards[self.turn]: # check if the cards he wants to play is in his hands
            self.playingcards[self.turn].remove(card)
            self.table.append(card)
            for client_socket in clients:
                print(clients[client_socket]["data"])
                if clients[client_socket]["sessionID"]==self.sessionID:
                    msg = f"Tisch: { ' '.join(self.table) }\n"
                    msg = bytearray(msg,"utf-8")
                    client_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
            
            self.turn+=1
            self.turn%=4
            if len(self.table) == 4:
                color = self.table[0].split(" ")[0]
                highest = [self.cards[self.table[0]][1], 0,False]
                index = 1
                trumped = False
                for car in self.table[1:]:
                    if color in car and not trumped:
                        if highest[0] < self.cards[car][1]:
                            highest = [self.cards[car][1],index,False]
                    if self.trumpf in car:
                        if not highest[2]:
                            trumped = True
                            highest = [self.cards[car][1],index,True]
                        else:
                            if highest[0] < self.cards[car][1]:
                                highest = [self.cards[car][1],index,True]
                p=0
                index = highest[1]
                for m in self.table:
                    p+=self.cards[m][0]

                if (self.turn-3+index)%2==0:

                    self.points[0]+=p
                else:
                    self.points[1]+=p
                self.table = []
                self.turn = (self.turn-3+index)%4
            return
                    
        else:
            msg = b"Es kann sein, dass du diese Karte nicht besitzt, versuche es nochmals so: /playcard Eicheln 7 oder /playcard Schellen Banner"
            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
            return

    def mycards(self,player):
        mycards = bytearray(" ".join(self.playingcards[player]),"utf-8")
        print("cards?")
        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(mycards)+mycards)

    def myturn(self, player):
        for m in range(4):
            if (self.turn+m)%4==player:
                msg = f"{m} people are before you"
                msg = bytearray(msg,"utf-8")
                notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
                return
        print("Not working myturn")

    def point(self, player):
        msg = f"Team 1 has {self.points[0]} points and team 2 has {self.points[1]} points."
        msg = bytearray(msg,"utf-8")
        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
        
    def working(self,m):
        t = -1
        for client_i in range(len(self.players)):
            if notified_socket == self.players[client_i]:
                t = client_i
        if t ==-1:
            print("Errororororrorororor, player not found")
            sys.exit()
        print(t)
        if notified_socket == self.players[self.turn]:                        #checks if the socket at the moment is the one turns it is
            if m[:5] == "trump":
                self.trump(m[6:])
                return
            elif m[:8] == "playcard":
                self.playcard(m[9:])
                return
        if m == "mycards":
            self.mycards(t)
        elif m== "myturn":
            self.myturn(t)
        elif m == "points":
            self.point(t)
        elif m == "help":
            msg = b"Hilfe:\n/help fuer die Hilfe\n/trump [Farbe] fuer den Trumpf waehlen\n/playcard [Karte] um eine Karte auf den Tisch zu legen\n/mycards um die eigene Karten anzuschauen"
            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)
        else:
            msg = b"Command Not Found!!"
            notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)


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
                if user["sessionID"] in c:
                    sessionID = user["sessionID"]
                    jassapp = c[sessionID]
                    jassapp.working(m)
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
                            c[user["sessionID"]] = JassApp(players,user["sessionID"])
                
            
                    elif m=="help":
                        msg = b"Hilfe:\n/help fuer die Hilfe\n/start um das SPiel zu starten\n/trump [Farbe] fuer den Trumpf waehlen\n/playcard [Karte] um eine Karte auf den Tisch zu legen\n/mycards um die eigene Karten anzuschauen"
                        notified_socket.send(clients["Server"]["header"]+clients["Server"]["data"]+create_header(msg)+msg)


    for notified_socket in expception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]


