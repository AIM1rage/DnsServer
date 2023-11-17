from dataclasses import dataclass
from dns_message.header import Header
from dns_message.question import Question
from dns_message.answer import Answer
from dns_message.authority import Authority


@dataclass
class DnsMessage:
    """
    +---------------------+
    |        Header       | Заголовок
    +---------------------+
    |       Question      | Секция запросов
    +---------------------+
    |        Answer       | Секция ответа
    +---------------------+
    |      Authority      | Секция ответа об уполномоченных серверах
    +---------------------+
    |      Additional     | Секция ответа дополнительных записей
    +---------------------+
    """

    header: Header
    questions: list[Question]
    answers: list[Answer]
    authoritative_records: list[Authority]

    # additional

    @staticmethod
    def parse_message(message: bytes):
        pointer = 0
        header, pointer = Header.parse(message, pointer)
        print(f'Header parsed!')
        questions, pointer = Question.parse(message, header.qdcount, pointer)
        print(f'Questions parsed!')
        answer = Answer.parse(message, header.ancount, pointer)
        print(f'Answers parsed!')
        authoritative_records = Authority.parse(message,
                                                header.nscount,
                                                pointer,
                                                )
        print(f'Authority parsed!')
        # additional = parse_additional(message)
        # return DnsMessage(header, question, answer, authority, additional)
        return DnsMessage(header,
                          questions,
                          authoritative_records,
                          )
