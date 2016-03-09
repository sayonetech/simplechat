import sys

import socket, select, string, sys


class UserData(object):
    def __init__(self, *args, **kwargs):
        if kwargs.get('name', None):
            self.name = kwargs['name']
    name = None


class ChatService(object):

    def chat(self, client_socket, user_obj):
        socket_list = [sys.stdin, client_socket]

        sockets_to_read, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in sockets_to_read:
            #incoming message from remote server
            if sock == client_socket:
                data = sock.recv(4096)
                if data :
                    sys.stdout.write(data)
                    prompt(user_obj)

                else:
                    print '\nConnection refused'
                    sys.exit()

            #Incoming message
            else :
                message = sys.stdin.readline()
                client_socket.send(message)
                prompt(user_obj)


def prompt(user_obj) :
    sys.stdout.write('('+user_obj.name+')')
    sys.stdout.flush()
