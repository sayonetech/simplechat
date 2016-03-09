import json
import fcntl
import struct
import socket

import settings


user_data = {}


class UserNamesHandler(object):

    def write_to_file(self, data):
        data_file = open(settings.MAPPING_FILE_PATH, 'r+')
        data_file.seek(0)
        json.dumps((data, data_file))
        data_file.close()

    def read_data(self):
        data_file = open(settings.MAPPING_FILE_PATH, 'r+')
        data = data_file.read()
        return data

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def add(self, data):
        user_data.update(data)
        return data

    def read(self):
        return user_data

    def manage_chat_port(self, address):
        ip = address[0]
        port = address[1]
        key = ip+':'+str(port)
        user_data[key] = user_data[ip]
        # data[ip].pop()


