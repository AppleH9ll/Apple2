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