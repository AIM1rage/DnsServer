import abc
from abc import ABC
from dns_message.utils import (read_domain_name,
                               read_ushort_number,
                               read_ulong_number,
                               )


class ResourceRecord(ABC):
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
    pointer: int

    def __init__(self, message: bytes, pointer: int):
        self.rname, pointer = read_domain_name(message, pointer)
        self.rtype, pointer = read_ushort_number(message, pointer)
        self.rclass, pointer = read_ushort_number(message, pointer)
        self.ttl, pointer = read_ulong_number(message, pointer)
        self.rdlength, pointer = read_ushort_number(message, pointer)
        self.rdata, pointer = self._read_data(message, pointer)
        self.pointer = pointer
        print(
            f'Reading record: {self.rname=} {self.rtype=} {self.rclass=} {self.ttl=} {self.rdlength=} {self.rdata=}')

    @abc.abstractmethod
    def _read_data(self, message: bytes, pointer: int):
        ...

    @staticmethod
    def _parse(message: bytes, count: int, pointer: int, constructor):
        records = []
        for _ in range(count):
            record = constructor(message, pointer)
            pointer = record.pointer
            records.append(record)
        return records, pointer
