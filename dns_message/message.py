from dataclasses import dataclass
from dns_message.header import Header
from dns_message.question import Question
from dns_message.answer import Answer
from dns_message.authority import Authority
from dns_message.additional import Additional
from dns_server.values import DnsServer


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
    raw_message: bytes

    def has_answers(self):
        return any(answer.rtype == 1 for answer in self.answers)

    def has_responsible_dns_servers(self):
        return any(record.rtype == 1 for record in self.additional_records)

    def get_responsible_dns_servers(self):
        for record in self.additional_records:
            if record.rtype == 1:
                yield DnsServer(record.rdata, record.rdata, record.rname)

    @staticmethod
    def parse_message(message: bytes):
        pointer = 0
        header, pointer = Header.parse(message, pointer)
        print(f'Header parsed! {pointer=}')

        questions, pointer = Question.parse(message, header.qdcount, pointer)
        print(f'Questions parsed! {pointer=}')

        answers, pointer = Answer.parse(message, header.ancount, pointer)
        print(f'Answers parsed! {pointer=}')

        authoritative_records, pointer = Authority.parse(message,
                                                         header.nscount,
                                                         pointer,
                                                         )
        print(f'Authority parsed! {pointer=}')

        additional_records, pointer = Additional.parse(message,
                                                       header.arcount,
                                                       pointer,
                                                       )
        print(f'Additional parsed! {pointer=}')

        print(f'Message parsed! {pointer=} and {len(message)=}')
        return DnsMessage(header,
                          questions,
                          answers,
                          authoritative_records,
                          additional_records,
                          message,
                          )
