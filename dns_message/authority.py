from dataclasses import dataclass
from dns_message.utils import (read_name,
                               read_ushort_number,
                               read_ulong_number,
                               )


@dataclass
class Authority:
    """
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    rname: str
    rtype: int
    rclass: int
    ttl: int
    rdlength: int
    rdata: str

    @staticmethod
    def parse(message: bytes, nscount: int, pointer: int):
        records = []
        for _ in range(nscount):
            record, pointer = Authority._read_record(message, pointer)
            records.append(record)
        return records, pointer

    @staticmethod
    def _read_record(message: bytes, pointer: int):
        rname, pointer = read_name(message, pointer)
        rtype, pointer = read_ushort_number(message, pointer)
        rclass, pointer = read_ushort_number(message, pointer)
        ttl, pointer = read_ulong_number(message, pointer)
        rdlength, pointer = read_ushort_number(message, pointer)
        rdata, pointer = read_name(message, pointer)
        print(f'Reading authority: {rname=} with {ttl=} and {rdata=}')
        return Authority(rname, rtype, rclass, ttl, rdlength, rdata), pointer
