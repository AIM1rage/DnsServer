import socketserver
from server import DnsRequestHandler


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 53
    with socketserver.UDPServer((HOST, PORT), DnsRequestHandler) as server:
        server.serve_forever()
