import argparse
import socketserver
from dns_server.server import DnsRequestHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='DnsServer',
                                     description='This server is required to obtain an IP address from a domain name. The implementation is recursive (cache supported!).')
    parser.add_argument('ip', type=str,
                        help='IP - address you want to specify (localhost, 127.0.0.1)',
                        )
    parser.add_argument('port', type=int, default=53,
                        help='port (default and recommended: 53)',
                        )
    args = parser.parse_args()
    with socketserver.UDPServer((args.ip, args.port),
                                DnsRequestHandler,
                                ) as server:
        print(f'Serving for {args.ip}:{args.port} ...')
        server.serve_forever()
