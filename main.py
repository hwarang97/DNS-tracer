import dns_trace

root_sever_ip = "198.41.0.4"
domain = "www.example.com."

# 직접 DNS 서버에 query 전송
trace = dns_trace.trace_domain(domain, root_sever_ip)
dns_trace.print_trace(domain, trace)

# 윈도우에서 DSN query 전송
system_ips = dns_trace.resolve_domain_ipv4_with_windows(domain)
print(f"윈도우에서 조회한 도메인 IP: {system_ips}")
