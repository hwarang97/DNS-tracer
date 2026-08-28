import dns.message

ROOT_SERVERS = [
    {"name": "a.root-servers.net", "ipv4": "198.41.0.4"}
]

# 임의 도메인 설정
# TODO: 사용자 입력에서 도메인을 추출하도록 확장
domain = "www.example.com."

# dns query 메세지 작성
###################################
# qname: 묻고 싶은것. 도메인
# qtype: 찾는 레코드. A
# flags: 동작 비트. RD(1), Not RD(0)
###################################
query_message = dns.message.make_query(qname=domain, rdtype="A", flags=0)

print(query_message)
