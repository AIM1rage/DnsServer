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
    def parse(message: bytes, qdcount: int, offset: int):
        questions = []
        for _ in range(qdcount):
            question, offset = Question._read_question(message, offset)
            questions.append(question)
        return questions, offset

    @staticmethod
    def _read_question(message: bytes, offset: int):
        qname, offset = read_name(message, offset)
        qtype, offset = read_ushort_number(message, offset)
        qclass, offset = read_ushort_number(message, offset)
        print(f'Reading question: {qname}')
        return Question(qname, qtype, qclass), offset
