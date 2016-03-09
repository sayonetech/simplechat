import socket, select, string, sys
import json

import settings
from services import UserNamesHandler

from utils import prompt, UserData, ChatService


if __name__ == "__main__":

    service = UserNamesHandler()
    your_ip = service.get_ip_address('eth0')

    if len(sys.argv) < 2 :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
    name = raw_input("Your name: ")
    user_obj = UserData(name=name)
    host = sys.argv[1]
    port = settings.PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    # Connect Server
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print 'Unable to connect..',e
        sys.exit()
     
    print 'Connection Established..successfully..'
    prompt(user_obj)

    obj = ChatService()
    while 1:
        obj.chat(client_socket, user_obj)
