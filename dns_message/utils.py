import struct
from typing import Optional


def read_name(message: bytes, offset: int) -> tuple[str, int]:
    name, offset, _ = read_data(message, offset)
    return b'.'.join(name).decode(), offset


def read_data(message: bytes,
              offset: int,
              ) -> tuple[list[str], int, bool]:
    data = []
    while True:
        first_two_bits = message[offset] >> 6
        match first_two_bits:
            case 0:
                length = message[offset]
                offset += 1
                if length == 0:
                    break
                chunk = message[offset: offset + length]
                data.append(chunk)
                offset += length
            case 3:
                chunk_offset = (((message[offset] & 0b00111111) << 8) +
                                message[offset + 1])
                chunks, _, is_end = read_data(message, chunk_offset)
                data.extend(chunks)
                offset += 2
                if is_end:
                    break
            case _:
                raise ValueError(
                    f'Not supported data type: {first_two_bits=} of {message[offset]}')
    return data, offset, True


def read_number(message: bytes,
                format: str,
                length,
                offset: int,
                ) -> tuple[int, int]:
    number = struct.unpack_from(format, message[offset: offset + length])[0]
    offset += length
    return number, offset


def read_ushort_number(message: bytes, offset: int) -> tuple[int, int]:
    number, offset = read_number(message, '!H', 2, offset)
    return number, offset


def read_ulong_number(message: bytes, offset: int) -> tuple[int, int]:
    number, offset = read_number(message, '!L', 4, offset)
    return number, offset
