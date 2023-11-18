import time
import socket
import socketserver
from dns_message.message import DnsMessage
from dns_server.values import DnsServer
from data.database import Database

ROOT_DNS_SERVERS = [
    DnsServer('aboba', '213.180.193.1', None),
    DnsServer('a.root-servers.net.', '198.41.0.4', None),
    DnsServer('b.root-servers.net.', '199.9.14.201', None),
    DnsServer('c.root-servers.net.', '192.33.4.12', None),
    DnsServer('d.root-servers.net.', '199.7.91.13', None),
    DnsServer('e.root-servers.net.', '192.203.230.10', None),
    DnsServer('f.root-servers.net.', '192.5.5.241', None),
    DnsServer('g.root-servers.net.', '192.112.36.4', None),
    DnsServer('h.root-servers.net.', '198.97.190.53', None),
    DnsServer('i.root-servers.net.', '192.36.148.17', None),
    DnsServer('j.root-servers.net.', '192.58.128.30', None),
    DnsServer('k.root-servers.net.', '193.0.14.129', None),
    DnsServer('l.root-servers.net.', '199.7.83.42', None),
    DnsServer('m.root-servers.net.', '202.12.27.33', None),
]


class DnsRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.database = Database()
        super().__init__(request, client_address, server)

    def handle(self):
        query = self.request[0]
        sock = self.request[1]

        response = self.resolve(query)
        sock.sendto(response, self.client_address)

    def send_query(self, query: bytes, server: DnsServer) -> DnsMessage:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query, (server.ip, 53))
        raw_response = sock.recv(4096)
        return DnsMessage.parse_message(raw_response)

    def resolve(self, query) -> bytes:
        servers_to_ask = ROOT_DNS_SERVERS.copy()
        request = DnsMessage.parse_message(query)

        self.database.check_expiration()
        if self.database.check_server_exists(request.questions[0].qname):
            response = DnsMessage.parse_message(
                self.database.get_response(request.questions[0].qname))
            response.change_id(request)
            return response.raw_message

        response = self.send_query(query, servers_to_ask.pop())
        while servers_to_ask and not response.has_answers():
            server = servers_to_ask.pop()
            response = self.send_query(query, server)
            servers_to_ask.extend(response.get_responsible_dns_servers())

        if response.has_answers():
            self.database.add_entry(response.questions[0].qname,
                                    response.raw_message,
                                    time.time(),
                                    response.answers[0].ttl,
                                    )

        return response.raw_message
