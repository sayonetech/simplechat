import socket, select
import settings

from services import UserNamesHandler
 

def broadcast_data (client_sock, message):
    """
    Function to broadcast data to clients
    Do not send the message to server and client who sent the message
    """
    for socket in CONNECTIONS:
        if socket != server_socket and socket != client_sock :
            try :
                socket.send(message)
            except Exception as e:
                socket.close()
                CONNECTIONS.remove(socket)


if __name__ == "__main__":

    CONNECTIONS = []
    BUFFER_SIZE = 4096
    PORT = settings.PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((settings.HOST, settings.PORT))
    server_socket.listen(settings.MAX_CONN)


    CONNECTIONS.append(server_socket)

    print "Server started on port" + str(PORT)

    while 1:
        sockets_to_read, write_sockets,error_sockets = select.select(CONNECTIONS,[],[])
 
        for client_socket in sockets_to_read:
            if client_socket == server_socket:
                # Add new connection
                socket_obj, client_address = server_socket.accept()
                CONNECTIONS.append(socket_obj)
                print "Client (%s, %s) connected" % client_address

                broadcast_data(client_socket, "[%s:%s] entered room\n" % client_address)

            #Messages from client
            else:
                try:
                    data = client_socket.recv(BUFFER_SIZE)
                    if data:
                        broadcast_data(client_socket, '(' + str(client_socket.getpeername()) + ') ' + data)

                except Exception as e:
                    broadcast_data(client_socket, "(%s, %s) went offline..." % client_address)
                    print "(%s, %s) went offline..." % client_address
                    client_socket.close()
                    if client_socket in CONNECTIONS:
                        CONNECTIONS.remove(client_socket)

    server_socket.close()


