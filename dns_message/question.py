from dataclasses import dataclass
from dns_message.utils import read_name, read_ushort_number


@dataclass
class Question:
    """
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """

    qname: str
    qtype: int
    qclass: int

    @staticmethod
    def parse(message: bytes, qdcount: int, pointer: int):
        questions = []
        for _ in range(qdcount):
            question, pointer = Question._read_question(message, pointer)
            questions.append(question)
        return questions, pointer

    @staticmethod
    def _read_question(message: bytes, pointer: int):
        qname, pointer = read_name(message, pointer)
        qtype, pointer = read_ushort_number(message, pointer)
        qclass, pointer = read_ushort_number(message, pointer)
        print(f'Reading question: {qname}')
        return Question(qname, qtype, qclass), pointer
