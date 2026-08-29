import dns.message
import dns.query
import dns.flags

ROOT_SERVERS = [
    {"name": "a.root-servers.net", "ipv4": "198.41.0.4"}
]

# 임의 도메인 설정
# TODO: 사용자 입력에서 도메인을 추출하도록 확장
domain = "www.example.com."

############## dns query 메세지 작성 #############
# 
# qname: 묻고 싶은것. 도메인
# qtype: 찾는 레코드. A
# flags: 동작 비트. RD(1), Not RD(0)
query_message = dns.message.make_query(qname=domain, rdtype="A", flags=0)


############### dns query 전송 #################
# dns query 전송
# q: 쿼리문
# where: 쿼리를 보낼 서버 ip 
# timeout: 응답까지 기다리는 최대 시간
# udp 전송
response = dns.query.udp(query_message, ROOT_SERVERS[0]["ipv4"], timeout=3.0)

# TC 발생시, TCP 방식으로 재요청
if response.flags & dns.flags.TC:
    response = dns.query.tcp(query_message, ROOT_SERVERS[0]["ipv4"], timeout=3.0)

print(response)
