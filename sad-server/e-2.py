from collections import defaultdict

freq = defaultdict(int)

with open('./log-file.txt', 'r') as r:

    lines = r.readlines()

    for line in lines:
        ip = line.split()[0]
        freq[ip] += 1

    freq = sorted(freq.items(), key = lambda x: x[1], reverse=True)[0]

    print(f'IP with highest frequency is {freq[0]}')

"""
IP with highest frequency is 192.168.1.1
"""