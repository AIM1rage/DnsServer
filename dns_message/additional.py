from dns_message.utils import read_ipv4, read_ipv6, read_fixed_length_data
from dns_message.resource_record import ResourceRecord


class Additional(ResourceRecord):

    def _read_data(self, message: bytes, pointer: int):
        match self.rtype:
            case 1:  # A record
                return read_ipv4(message, pointer)
            case 28:  # AAAA record
                return read_ipv6(message, pointer)
            case _:  # other records
                return read_fixed_length_data(message, pointer, self.rdlength)

    @staticmethod
    def parse(message: bytes, count: int, pointer: int):
        return ResourceRecord._parse(message, count, pointer,
                                     lambda m, p: Additional(m, p))
