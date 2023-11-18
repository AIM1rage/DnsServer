# DNS Server

This server is required to obtain an IP address from a domain name. The
implementation is recursive (cache supported!).

## Requirements

- Python 3.10+

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/AIM1rage/DnsServer
   ```

2. Install the required Python version 3.10+ on the official website:

   ```
   https://www.python.org/downloads/
   ```

## Usage

To run the DNS Server go to root directory and enter the following command directly from your console line:

```
python dns.py <ip> <port>
```

- `<ip>`: IP - address you want to specify (localhost, 127.0.0.1)
- `<port>`: port (default and recommended: 53)

You can also use some programs like dig, nslookup and something else:

### dig

```
dig @<dns_server_ip> <domain_name>
```

### nslookup
```
nslookup <domain_name> <dns_server_ip>
```

## Example usage:
You can start the server by entering the following command:

```
python dns.py 127.0.0.1 53
```
And get the IP-address of google.com:
```
dig @127.0.0.1 google.com
```
