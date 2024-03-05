import socket
import random
import threading
def pri():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    try:
         client_socket.connect((host, port))
         sp=int(input("Do you want shared pool?(Input 1 for yes, 0 for no)"))
         if sp==1:
           client_socket.send(f"Yes".encode())
         else:
           client_socket.send(f"No".encode())
         
         
         while True:
            data = client_socket.recv(1024).decode()
            L,R=map(int, data.split())
            Y = random.randint(L, R)
            client_socket.send(str(Y).encode())
            message = client_socket.recv(1024).decode()
            print(message)
            if "Too high" in message:
                R = Y
            elif "Too low" in message:
                L = Y+1
            else:
                msg=client_socket.recv(1024).decode()
                print(msg)
                break
            client_socket.send(f"{L} {R}".encode())             
    finally:
         client_socket.close()
if __name__=="__main__":
      ##m= int(input("Number of prisoners:"))
      ##for i in range(0,m):
        t= threading.Thread(target=pri,args=())
        t.start()