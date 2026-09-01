import socket

import dns.message
import dns.query
import dns.flags
import dns.rdatatype
import dns.rcode


def resolve_domain_ipv4_with_windows(domain: str) -> list[str]:
    """Windows의 일반 이름 조회로 도메인의 IPv4 주소를 반환한다."""
    if not domain:
        raise ValueError("도메인 매개변수가 비어있습니다!")

    normalized_domain = domain.rstrip(".")
    if not normalized_domain:
        raise ValueError("도메인 매개변수가 비어있습니다!")

    results = socket.getaddrinfo(
        normalized_domain,
        None,
        family=socket.AF_INET,
    )

    ip_list = []
    for _, _, _, _, sockaddr in results:
        ip = sockaddr[0]
        if ip not in ip_list:
            ip_list.append(ip)

    return ip_list

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

def trace_domain(domain: str, root_server_ip: str) -> list[dict[str, str]]:

    server_ip = root_server_ip
    traces: list[dict] = [] # DNS 이동 과정 기록

    while True:
        response = query_dns(domain, server_ip)
        current = {
            "server_ip": server_ip, 
            "next_server_ip": "", 
            "final_ips": [],} 

        if response.rcode() != dns.rcode.NOERROR:
            raise ValueError("DNS 서버로부터 오류 반환")

        if response.answer:
            current["final_ips"] = extract_ip(response)
            traces.append(current)
            return traces
        else:
            server_ip = extract_ip(response)[0]
            current["next_server_ip"] = server_ip
            traces.append(current)

def print_trace(domain: str, traces: list[dict]) -> None:
    lines = [f"조회 도메인: {domain}", ""]

    for step in traces:
        lines.append(f"현재 서버: {step['server_ip']}")

        if not step["next_server_ip"]:
            lines.append(f"도메인 IP: {step['final_ips']}")
        else:
            lines.append(f"다음 서버: {step['next_server_ip']}")
            lines.append("")

    print("\n".join(lines))  

if __name__ == "__main__":
    domain = "www.example.com."
    root_server_ip = "198.41.0.4"
    response = query_dns(domain, root_server_ip)
    print(response)
