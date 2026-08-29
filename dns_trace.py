import dns.message
import dns.query
import dns.flags

def query_dns(domain:str, dns_server_ip: str) -> dns.message.Message:

    if not domain:
        raise ValueError("도메인 매개변수가 비어있습니다!")

    ############## dns query 메세지 작성 #############
    # qname: 묻고 싶은것. 도메인
    # qtype: 찾는 레코드. A
    # flags: 동작 비트. RD(1), Not RD(0)
    query_message = dns.message.make_query(qname=domain, rdtype="A", flags=0)

    ############### dns query 전송 #################
    # q: 쿼리문
    # where: 쿼리를 보낼 서버 ip 
    # timeout: 응답까지 기다리는 최대 시간
    # udp 전송
    response = dns.query.udp(query_message, dns_server_ip, timeout=3.0)

    # TC 발생시, TCP 방식으로 재요청
    if response.flags & dns.flags.TC:
        response = dns.query.tcp(query_message, dns_server_ip, timeout=3.0)

    return response

if __name__ == "__main__":
    domain = "www.example.com."
    root_server_ip = "198.41.0.4"
    response = query_dns(domain, root_server_ip)
    print(response)
