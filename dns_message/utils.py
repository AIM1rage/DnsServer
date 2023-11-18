import struct
import binascii


def read_domain_name(message: bytes, pointer: int) -> tuple[str, int]:
    name, pointer, _ = read_chunks(message, pointer)
    try:
        return b'.'.join(name).decode(), pointer
    except UnicodeDecodeError:
        return '', pointer


def read_ipv4(message: bytes, pointer: int) -> tuple[str, int]:
    return ".".join(str(message[pointer + i]) for i in range(4)), pointer + 4


def read_ipv6(message: bytes, pointer):
    return ":".join(
        binascii.hexlify(
            message[pointer + 2 * i:
                    pointer + 2 * (i + 1)])
        .decode() for i in
        range(8)), pointer + 16


def read_fixed_length_data(message: bytes,
                           pointer: int,
                           length: int
                           ) -> tuple[bytes, int]:
    return message[pointer: pointer + length], pointer + length


def read_chunks(message: bytes,
                pointer: int,
                ) -> tuple[list[str], int, bool]:
    data = []
    while True:
        first_two_bits = message[pointer] >> 6
        match first_two_bits:
            case 0:  # 00 prefix bits
                length = message[pointer]
                pointer += 1
                if length == 0:
                    break
                chunk = message[pointer: pointer + length]
                data.append(chunk)
                pointer += length
            case 3:  # 11 prefix bits
                chunk_offset = (((message[pointer] & 0b00111111) << 8) +
                                message[pointer + 1])
                chunks, _, is_end = read_chunks(message, chunk_offset)
                data.extend(chunks)
                pointer += 2
                if is_end:
                    break
            case _:  # not supported bits 01 and 10
                raise ValueError(
                    f'Not supported data type: {first_two_bits=} of {message[pointer]}')
    return data, pointer, True


def read_number(message: bytes,
                format: str,
                length,
                pointer: int,
                ) -> tuple[int, int]:
    number = struct.unpack_from(format, message[pointer: pointer + length])[0]
    pointer += length
    return number, pointer


def read_ushort_number(message: bytes, pointer: int) -> tuple[int, int]:
    number, pointer = read_number(message, '!H', 2, pointer)
    return number, pointer


def read_ulong_number(message: bytes, pointer: int) -> tuple[int, int]:
    number, pointer = read_number(message, '!L', 4, pointer)
    return number, pointer
