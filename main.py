import dns_trace

ROOT_SERVERS = {"name": "a.root-servers.net", "ipv4": "198.41.0.4"}

domain = "www.example.com."
response = dns_trace.query_dns(domain, ROOT_SERVERS["ipv4"])
print(response)
