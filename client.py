import socket
import time


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
                self.sock.connect(('192.168.1.17', 5555))
                print("[+] Connection established")
                self.shell()
                self.sock.close()
                print('Socket is closed.')
                # it breaks the loop if I can connect since no error has been thrown
                break
            except:
                # if it throws an error then
                self.connection()

    def shell(self):
        """
            Listen to the commands made by the Server.
        """
        while True:
            message = self.sock.recv(1024)
            if message == 'ter':
                break
            self.sock.send('Dummy response from the client... :0)'.encode('utf-8'))


if __name__ == '__main__':
    Client().connection()
