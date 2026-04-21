#сервер
import socket
import threading

clients = []
clients_lock = threading.Lock()

def broadcast_message(message, sender_socket=None):
    global clients
    with clients_lock:
        for client_socket, username in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    pass

def send_private_message(message, recipient_socket):
    try:
        recipient_socket.send(message.encode('utf-8'))
    except:
        pass

def handle_client(client_socket, client_address):
    global clients
    print(f'Клиент {client_address} подключён')
    
    try:
        client_socket.send("Введите ваше имя: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        if not username:
            username = f"Аноним_{client_address[1]}"
        
        with clients_lock:
            clients.append((client_socket, username))
        
        welcome_msg = f"Добро пожаловать в чат, {username}!"
        send_private_message(welcome_msg, client_socket)
        
        join_msg = f"{username} присоединился к чату"
        broadcast_message(join_msg, client_socket)
        
        print(f'Пользователь {username} ({client_address}) присоединился к чату')
        print(f'Всего подключено клиентов: {len(clients)}')
        
    except:
        with clients_lock:
            clients = [c for c in clients if c[0] != client_socket]
        client_socket.close()
        return
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            
            current_username = None
            with clients_lock:
                for sock, name in clients:
                    if sock == client_socket:
                        current_username = name
                        break
            
            print(f'[{current_username}]: {message}')
            
            broadcast_message(f"{current_username}: {message}", client_socket)
            
        except:
            break
    
    with clients_lock:
        disconnected_user = None
        for sock, name in clients:
            if sock == client_socket:
                disconnected_user = name
                clients.remove((sock, name))
                break
    
    client_socket.close()
    print(f'Пользователь {disconnected_user} ({client_address}) отключился')
    
    if disconnected_user:
        leave_msg = f"{disconnected_user} покинул чат"
        broadcast_message(leave_msg)

def get_online_users():
    global clients
    with clients_lock:
        return [name for _, name in clients]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5001))
server_socket.listen()

print('Сервер ждёт подключения клиентов')

try:
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()
        
except KeyboardInterrupt:
    print("\nСервер завершает работу...")
    with clients_lock:
        for client_socket, _ in clients:
            try:
                client_socket.close()
            except:
                pass
    server_socket.close()
    print("Сервер остановлен")

#клиент
import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("\nСоединение с сервером разорвано")
                break
            
            decoded_msg = message.decode('utf-8')
            
            if decoded_msg == "Введите ваше имя: ":
                continue
            
            print(f"\n{decoded_msg}")
            print("Вы: ", end="", flush=True)
            
        except:
            print("\nОшибка соединения с сервером")
            break
    
    print("Завершение работы клиента...")
    sys.exit(0)

def send_messages(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
        except:
            print("Ошибка отправки сообщения")
            break

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5001))
    
    username = input("Введите ваше имя для чата: ")
    if not username.strip():
        username = "Аноним"
    
    client_socket.send(username.encode('utf-8'))
    
    print(f"\nПодключено к чат-серверу как {username}!")
    
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    sys.exit(1)

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
receive_thread.start()

send_thread = threading.Thread(target=send_messages, args=(client_socket,), daemon=True)
send_thread.start()

try:
    receive_thread.join()
    send_thread.join()
except KeyboardInterrupt:
    print("\nЗавершение работы клиента...")
    client_socket.close()
    sys.exit(0)