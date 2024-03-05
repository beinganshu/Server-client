import random
import socket
import threading
global shared_pool
global shared_pool_id
def handle_client(client_server, prisoner_id,L,R,L1,R1):
     global escape_order
     if(prisoner_id in shared_pool_id):
        while prisoner_id in shared_pool and prisoner_id not in escape_order:
            client_server.send(f"{L1} {R1}".encode())
            guess = int(client_server.recv(1024).decode())
            if guess > X:
              client_server.send(f"Too high".encode())
            elif guess < X:
              client_server.send(f"Too low".encode())
            else:
              for prisoner_id in shared_pool_id:
                 escape_order.append(prisoner_id)
                 print(f"Prisoner {prisoner_id} escaped")
                 client_server.send(f"Shared pool members escaped.".encode())
              if len(clients) == len(escape_order) :
                client_server.send(f"All prisoners escaped".encode())
                break
            data = client_server.recv(1024).decode()
            L1,R1=map(int, data.split())
     else:
      while True:
          client_server.send(f"{L} {R}".encode())
          guess = int(client_server.recv(1024).decode())
          if guess > X:
              client_server.send(f"Too high".encode())
          elif guess < X:
              client_server.send(f"Too low".encode())
          else:
              escape_order.append(prisoner_id)
              client_server.send(f"Prisoner {prisoner_id} escaped".encode())
              print(f"Prisoner {prisoner_id} escaped")
              if len(clients) == len(escape_order) :
                  client_server.send(f"All prisoners escaped".encode())
                  break
          data = client_server.recv(1024).decode()
          L,R=map(int, data.split())
     client_server.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' 
port = 12345

server_socket.bind((host, port))
server_socket.listen(2)
clients = []
escape_order = []
shared_pool=[]
shared_pool_id=[]
L = random.randrange(0,10**3)
R = L + random.randint(10**4, 10**5)
L1=L
R1=R
X = random.randint(L, R)
print("Waiting for prisoners to connect...")
def accept_connection():
    while True:
        client_server, addr = server_socket.accept()
        clients.append(client_server)
        prisoner_id = len(clients)
        print(f"Prisoner {prisoner_id} connected: {addr}")
        messg=client_server.recv(1024).decode()
        if(messg=="Yes"):
            print(f"Prisoner {prisoner_id} choosed for shared pool.")
            shared_pool.append(client_server)
            shared_pool_id.append(prisoner_id)
        else:
            print(f"Prisoner {prisoner_id} did not choose shared pool.")
        if len(clients)==4:
            start_game()
        ##thread=threading.Thread(target=handle_client, args=(client_server,prisoner_id))
        ##thread.start()
accept_thread= threading.Thread(target=accept_connection)
accept_thread.start()

def start_game():
    print("Staring the game...")
    for prisoner_id,client_server in enumerate(clients,1):
        thread=threading.Thread(target=handle_client, args=(client_server,prisoner_id,L,R,L1,R1))
        thread.start()