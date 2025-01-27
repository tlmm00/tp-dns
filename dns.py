from dataclasses import dataclass
from dns_student.dns_tools import *
import dataclasses, struct, random, socket, argparse
random.seed(1)

TYPE_A = 1
TYPE_AAAA = 28
CLASS_IN = 1

@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_addidionals: int = 0

@dataclass
class DNSQuestion:
    name: bytes
    type_: int 
    class_: int 

def header_to_bytes(header):
    fields = dataclasses.astuple(header)

    # 6 H para 6 campos diferentes
    return struct.pack("!HHHHHH", *fields)

def question_to_bytes(question):

    # 2 H para 2 campos diferentes
    return question.name + struct.pack("!HH", question.type_, question.class_)

def encode_dns_name(domain_name):
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += bytes([len(part)]) + part
    
    return encoded + b"\x00"

def build_query(domain_nane, record_type):
    name = encode_dns_name(domain_nane)
    id = random.randint(0, 65535)
    RECURSION_DESIRED = 1 << 8
    header = DNSHeader(id=id, num_questions=1, flags=RECURSION_DESIRED)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)

    return header_to_bytes(header) + question_to_bytes(question)

def find_paragraph_with_string(text, search_string):
    paragraphs = text.split("\n\n")
    matching_paragraphs = [
        paragraph for paragraph in paragraphs
        if search_string.lower() in paragraph.lower()
    ]
    
    return matching_paragraphs

def main():
    dns_tool = DNS()

    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="A", type=str, choices=["A", "AAAA"])
    parser.add_argument("--name", default="www.google.com", type=str)
    parser.add_argument("--server", default="8.8.8.8", type=str)
    
    args = parser.parse_args()

    record_type = TYPE_A if args.type == "A" else TYPE_AAAA
    query = build_query(args.name, record_type)
    # print("Raw DNS query:", query)

    if ":" in args.server:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(query, (args.server, 53))
        response, _ = sock.recvfrom(1024)
        dns_tool.decode_dns(response)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()