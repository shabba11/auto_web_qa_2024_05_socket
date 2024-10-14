import socket
import http

# Create a TCP server socket

http_response = (
    f"HTTP/1.0 200 OK\r\n"
    f"Server: otusdemo\r\n"
    f"Date: Sat, 01 Oct 2022 09:39:37 GMT\r\n"
    f"Content-Type: text/html; charset=UTF-8\r\n"
    f"\r\n"
)

end_of_stream = '\r\n\r\n'


def handle_client(connection):
    request_data = connection.recv(1024).decode()
    print(f"Received request:\n{request_data}\n")

    # Разделяем запрос на строку и заголовки
    request_lines = request_data.splitlines()
    request_line = request_lines[0]

    # Получаем метод и URL
    method, url, _ = request_line.split()

    # Получаем статус из параметров
    status_code = url[-3:]

    # Устанавливаем стандартный 200 статус
    if status_code is None or not status_code.isdigit():
        status_code = 200
    else:
        status_code = int(status_code)
        # Если статус не валиден, также выставляем 200
        if status_code < 100 or status_code > 511:
            status_code = 200

    response_status = http.HTTPStatus(status_code).phrase

    # Подготавливаем ответ
    response_headers = [
        f"Request Method: {method}",
        f"Request Source: {connection.getpeername()}",
        f"Response Status: {status_code} {response_status}",
    ]

    # Добавляем заголовки запроса в ответ
    for header in request_lines[1:]:
        if header.strip():  # Игнорируем пустые строки
            response_headers.append(header)

    # Формируем полное содержимое ответа
    response_body = "\r\n".join(response_headers)
    response = f"HTTP/1.1 {status_code} {response_status}\r\n" \
               f"Content-Length: {len(response_body)}\r\n" \
               f"Content-Type: text/plain; charset=utf-8\r\n"\
               f"\r\n"\
               f"{response_body}"

    connection.send(response.encode())


def main():
    with socket.socket() as serverSocket:
        # Bind the tcp socket to an IP and port
        serverSocket.bind(("127.0.0.1", 40404))
        # Keep listening
        serverSocket.listen()

        while True:  # Keep accepting connections from clients
            (clientConnection, clientAddress) = serverSocket.accept()
            handle_client(clientConnection)
            print(f"Sent data to {clientAddress}")


if __name__ == "__main__":
    main()
