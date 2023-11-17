from dns_message.utils import read_ipv4, read_ipv6
from dns_message.resource_record import ResourceRecord


class Answer(ResourceRecord):
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

    def _read_data(self, message, pointer):
        match self.rdlength:
            case 4:
                return read_ipv4(message, pointer)
            case 16:
                return read_ipv6(message, pointer)
            case _:
                raise ValueError(f'Unsupported data type: {self.rtype}')

    @staticmethod
    def parse(message: bytes, count: int, pointer: int):
        records = []
        for _ in range(count):
            record = Answer(message, pointer)
            pointer = record.pointer
            records.append(record)
        return records, pointer
