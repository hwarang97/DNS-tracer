import dns_trace
import dns.rdatatype

ROOT_SERVERS = {"name": "a.root-servers.net", "ipv4": "198.41.0.4"}

domain = "www.example.com."
TLD_response = dns_trace.query_dns(domain, ROOT_SERVERS["ipv4"])
next_server_ip = ""
answer = []

# 응답으로부터 ipv4를 추출
for rrset in TLD_response.additional:
    if rrset.rdtype == dns.rdatatype.A:
        next_server_ip = str(rrset[0])
        break

# 다음 TLD 서버로 DNS query 전송
SLD_response = dns_trace.query_dns(domain, next_server_ip)

# 응답으로부터 ipv4를 추출
for rrset in SLD_response.additional:
    if rrset.rdtype == dns.rdatatype.A:
        next_server_ip = str(rrset[0])
        break

# SLD 서버로 DNS query 전송
final_response = dns_trace.query_dns(domain, next_server_ip)

# 최종 A 레코드값 반환
print(final_response.answer)
for rrset in final_response.answer:
    for rdata in rrset:
        answer.append(str(rdata))

print(answer)
