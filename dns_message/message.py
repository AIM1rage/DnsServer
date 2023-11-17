from dataclasses import dataclass
from dns_message.header import Header
from dns_message.question import Question
from dns_message.answer import Answer
from dns_message.authority import Authority
from dns_message.additional import Additional


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
    additional_records: list[Additional]

    # additional

    @staticmethod
    def parse_message(message: bytes):
        pointer = 0
        header, pointer = Header.parse(message, pointer)
        print(f'Header parsed! {pointer=}')

        questions, pointer = Question.parse(message, header.qdcount, pointer)
        print(f'Questions parsed! {pointer=}')

        answer, pointer = Answer.parse(message, header.ancount, pointer)
        print(f'Answers parsed! {pointer=}')

        authoritative_records, pointer = Authority.parse(message,
                                                         header.nscount,
                                                         pointer,
                                                         )
        print(f'Authority parsed! {pointer=}')

        additional, pointer = Additional.parse(message,
                                               header.arcount,
                                               pointer,
                                               )
        print(f'Additional parsed! {pointer=}')

        print(f'Message parsed! {pointer=} and {len(message)=}')
        return DnsMessage(header,
                          questions,
                          authoritative_records,
                          answer,
                          additional,
                          )
