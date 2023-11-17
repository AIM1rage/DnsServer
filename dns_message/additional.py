from dns_message.utils import read_ipv4, read_ipv6
from dns_message.resource_record import ResourceRecord


class Additional(ResourceRecord):
    @staticmethod
    def parse(message: bytes, count: int, pointer: int):
        records = []
        for _ in range(count):
            record = Additional(message, pointer)
            pointer = record.pointer
            records.append(record)
        return records, pointer

    def _read_data(self, message, pointer):
        match self.rdlength:
            case 4:
                return read_ipv4(message, pointer)
            case 16:
                return read_ipv6(message, pointer)
            case _:
                raise ValueError(f'Unsupported data type: {self.rtype}')



