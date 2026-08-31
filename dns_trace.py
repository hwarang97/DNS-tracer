import dns.message
import dns.query
import dns.flags
import dns.rdatatype
import dns.rcode

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

def extract_ip(response: dns.message.Message) -> list[str]:
    # response로부터 ip를 하나 추출해 반환하는 함수
    
    ip_list = []

    # answer에 ip가 들어있을 경우
    if response.answer:
        for rrset in response.answer:
            if rrset.rdtype == dns.rdatatype.A: # CNAME아 아닌 A 레코드일 경우만
                for rdata in rrset:
                    ip_list.append(str(rdata))

    # answer가 비어있을 경우 (아직 DNS 서버 IP 반환)
    else:
        for rrset in response.additional:
            if rrset.rdtype == dns.rdatatype.A:
                ip_list.append(str(rrset[0])) # 후보 중 하나만 선택
                break

    return ip_list

def get_domain_ip(domain: str, root_server_ip: str) -> list[str]:
    server_ip = root_server_ip
    while True:
        response = query_dns(domain, server_ip)

        if response.rcode() != dns.rcode.NOERROR:
            raise ValueError("DNS 서버로부터 오류 반환")

        if response.answer:
            return extract_ip(response)
        else:
            server_ip = extract_ip(response)[0]

if __name__ == "__main__":
    domain = "www.example.com."
    root_server_ip = "198.41.0.4"
    response = query_dns(domain, root_server_ip)
    print(response)
