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
    def parse(message: bytes, nscount: int, offset: int):
        records = []
        for _ in range(nscount):
            record, offset = Authority._read_record(message, offset)
            records.append(record)
        return records, offset

    @staticmethod
    def _read_record(message: bytes, offset: int):
        rname, offset = read_name(message, offset)
        rtype, offset = read_ushort_number(message, offset)
        rclass, offset = read_ushort_number(message, offset)
        ttl, offset = read_ulong_number(message, offset)
        rdlength, offset = read_ushort_number(message, offset)
        rdata, offset = read_name(message, offset)
        print(f'Reading authority: {rname=} with {ttl=} and {rdata=}')
        return Authority(rname, rtype, rclass, ttl, rdlength, rdata), offset
