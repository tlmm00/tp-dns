import socket, glob, json
from dns_student.dns_tools import *

PORT = 53
IP = '127.0.0.1'

def buildresponse(data):
    TransctionId = data[:2]

def main():
    is_ipv6 = False
    dns_tool = DNS()

    if(not is_ipv6):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    sock.bind((IP, PORT))


    while 1:
        data, addr = sock.recvfrom(512)
        # print(data)
        print(dns_tool.decode_dns(data))
        r = buildresponse(data)
        sock.sendto(r, addr)
    
    return

if __name__ == "__main__":
    main()