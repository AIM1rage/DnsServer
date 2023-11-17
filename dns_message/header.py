import struct
from dataclasses import dataclass


@dataclass
class Header:
    """
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """""
    id: int
    flags: int
    qdcount: int
    ancount: int
    nscount: int
    arcount: int

    @staticmethod
    def parse(message: bytes, pointer: int):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack_from(
            '!6H',
            message,
            offset=pointer,
        )
        print(
            f'Reading headers: {id=} {qdcount=} {ancount=} {nscount=} {arcount=}')
        return (Header(id, flags, qdcount, ancount, nscount, arcount),
                pointer + 12,
                )
