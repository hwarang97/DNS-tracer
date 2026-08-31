import dns_trace

root_sever_ip = "198.41.0.4"
domain = "www.example.com."
answer = dns_trace.get_domain_ip(domain, root_sever_ip)
print(answer)
