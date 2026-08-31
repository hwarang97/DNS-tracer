import dns_trace

root_sever_ip = "198.41.0.4"
domain = "www.example.com."
trace = dns_trace.trace_domain(domain, root_sever_ip)
dns_trace.print_trace(domain, trace)
