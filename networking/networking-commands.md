# Linux networking commands

list of essential Linux networking commands.

## **1. Interface & IP Configuration**

### 🛠 **Checking Network Interfaces & IP Addresses**

- `ip a` or `ip addr show` – Show all network interfaces and IP addresses
- `ip link show` – List network interfaces
- `ifconfig` (deprecated, but still useful) – Display network interfaces and
  configurations
- `ip -s link show eth0` – Show statistics for a specific interface
- `ip route` or `route -n` – Show current routing table
- `ip rule show` – View IP rules for policy-based routing

### 🛠 **Configuring Network Interfaces**

- `ip link set eth0 up/down` – Bring an interface up or down
- `ip addr add 192.168.1.100/24 dev eth0` – Assign an IP to an interface
- `dhclient eth0` – Request a dynamic IP via DHCP
- `nmcli dev status` – Manage and check network connections (NetworkManager CLI)

---

## **2. Connectivity & Debugging**

### 🛠 **Checking Connectivity & Latency**

- `ping google.com` – Check if a host is reachable
- `ping -c 5 8.8.8.8` – Send 5 ping requests
- `ping -i 0.2 google.com` – Set ping interval to 0.2s

### 🛠 **Checking Route to a Host**

- `traceroute google.com` – Show the network path to a destination
- `mtr google.com` – Continuous traceroute (better for real-time analysis)

### 🛠 **Testing TCP/UDP Connectivity**

- `telnet google.com 80` – Test TCP connection to a port
- `nc -zv google.com 443` – Check if a TCP port is open
- `nc -ul 5000` – Listen for UDP traffic on port 5000

---

## **3. DNS & Name Resolution**

### 🛠 **Checking DNS Resolution**

- `nslookup google.com` – Query DNS for a domain
- `dig google.com` – Get detailed DNS records
- `dig google.com +short` – Get a short answer for an IP
- `dig -x 8.8.8.8` – Reverse DNS lookup

### 🛠 **Checking Local DNS Cache**

- `cat /etc/resolv.conf` – Show configured DNS servers
- `systemd-resolve --status` – Check DNS settings

---

## **4. Analyzing Network Traffic**

### 🛠 **Capturing & Inspecting Packets**

- `tcpdump -i eth0` – Capture packets on eth0
- `tcpdump -i eth0 port 443` – Capture HTTPS traffic
- `tcpdump -nn -X port 80` – Show raw HTTP traffic in real-time
- `tcpdump -w capture.pcap` – Save packets to a file

### 🛠 **Inspecting Traffic in Detail**

- `wireshark` – GUI tool for deep packet analysis
- `tshark -i eth0` – CLI version of Wireshark

---

## **5. Network Statistics & Performance**

### 🛠 **Monitor Network Traffic**

- `netstat -tulnp` – Show open ports & processes using them
- `ss -tulnp` – Faster alternative to `netstat`
- `nmap -sP 192.168.1.0/24` – Scan local network for active hosts
- `ethtool eth0` – Get interface statistics

### 🛠 **Checking Bandwidth Usage**

- `iftop -i eth0` – Live bandwidth usage per connection
- `vnstat` – Monitor historical bandwidth usage
- `iperf -s` & `iperf -c <server>` – Test network speed

---

## **6. Firewall & Security**

### 🛠 **Managing Firewall Rules**

- `iptables -L` – List firewall rules
- `iptables -A INPUT -p tcp --dport 22 -j ACCEPT` – Allow SSH
- `iptables -A INPUT -p icmp -j DROP` – Block ping requests
- `ufw status` – Check firewall status (if UFW is used)

### 🛠 **Checking Open Ports**

- `lsof -i :80` – Check which process is using port 80
- `netstat -plnt` – List open ports with process names

---

## **7. Network Configuration & Logs**

### 🛠 **Checking System Logs**

- `journalctl -u networking` – View networking-related logs
- `cat /var/log/syslog | grep network` – Search network-related logs

### 🛠 **Testing Proxy & HTTP Requests**

- `curl -I google.com` – Get HTTP headers
- `wget -O- google.com` – Fetch a webpage
- `curl -x http://proxy:8080 google.com` – Use a proxy

---

## **8. Advanced Networking (For Meta-Specific Scale)**

### 🛠 **Managing Network Namespaces**

- `ip netns list` – Show network namespaces
- `ip netns exec <namespace> ip a` – Show IPs in a namespace

### 🛠 **Simulating Network Latency**

- `tc qdisc add dev eth0 root netem delay 100ms` – Add 100ms delay
- `tc qdisc del dev eth0 root netem` – Remove delay

---
