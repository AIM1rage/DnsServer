import socket
import socketserver
import time
from dns_message.message import DnsMessage
from collections import namedtuple

DnsServer = namedtuple('DnsServer', ['name', 'ip'])

ROOT_DNS_SERVERS = [
    DnsServer('aboba', '213.180.193.1'),
    DnsServer('a.root-servers.net.', '198.41.0.4'),
    DnsServer('b.root-servers.net.', '199.9.14.201'),
    DnsServer('c.root-servers.net.', '192.33.4.12'),
    DnsServer('d.root-servers.net.', '199.7.91.13'),
    DnsServer('e.root-servers.net.', '192.203.230.10'),
    DnsServer('f.root-servers.net.', '192.5.5.241'),
    DnsServer('g.root-servers.net.', '192.112.36.4'),
    DnsServer('h.root-servers.net.', '198.97.190.53'),
    DnsServer('i.root-servers.net.', '192.36.148.17'),
    DnsServer('j.root-servers.net.', '192.58.128.30'),
    DnsServer('k.root-servers.net.', '193.0.14.129'),
    DnsServer('l.root-servers.net.', '199.7.83.42'),
    DnsServer('m.root-servers.net.', '202.12.27.33'),
]


class DnsRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        query = self.request[0]
        sock = self.request[1]

        response = self.resolve(query)
        time.sleep(0.1)
        sock.sendto(response, self.client_address)

    def resolve(self, response):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(response, (ROOT_DNS_SERVERS[0].ip, 53))
        raw_response = sock.recv(4096)
        response = DnsMessage.parse_message(raw_response)
        return raw_response
