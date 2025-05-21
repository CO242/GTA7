import socket
import threading

HOST = '192.168.3.116'
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for Player 2 to connect...")
conn, addr = server.accept()
print(f"Player 2 connected from {addr}")

def relay():
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            server.sendall(data)
        except:
            break

threading.Thread(target=relay, daemon=True).start()

while True:
    msg = input()
    conn.send(msg.encode())

