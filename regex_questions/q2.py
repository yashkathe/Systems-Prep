import re

data = """
Email: test.email@example.com
InvalidEmail: test.email@com
AnotherEmail: hello.world@domain.net
User: user123_name@service.io
Website: www.example-site.com
IPv4: 192.168.1.1
InvalidIPv4: 999.999.999.999
ID: A1B2-C3D4-E5F6
"""

"""
email:
    Must have an "@" symbol.
    Should have a domain name followed by a top-level domain (e.g., .com, .net, .io).
"""

for line in data.splitlines():
    
    pattern = re.compile(r'[\w\d\.]+@[\w]+\.(?:com|net|io)+')

    for match in pattern.findall(line):
        print(match)

"""
Write a regex pattern to match valid IPv4 addresses from the text. A valid IPv4:

    Consists of four groups of numbers (0-255) separated by dots (.).
    Each group should be between 0 and 255.
    The invalid IP (999.999.999.999) should not match.
"""

def is_valid_ip(ip):
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

for line in data.splitlines():
    
    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    for match in pattern.findall(line):
        if is_valid_ip(match):
            print(match)
    




