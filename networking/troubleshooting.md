# Networking Troubleshooting

Scenarios with Linux Commands on how to approach Networking related
troubleshooting

## Table of Content

1. A Server Cannot Reach the Internet
2. Slow Network Performance
3. Cannot SSH into a Remote Server

## **Section 1: A Server Cannot Reach the Internet – Detailed Troubleshooting & Explanation**

Your server is unable to access the internet (e.g., `ping google.com` fails).
This could be due to **network misconfiguration, DNS issues, firewall rules, or
routing problems**. Let’s break it down step by step.

---

### **Step 1: Check Connectivity**

#### 🔹 **Command:**

```bash
ping google.com
```

#### 🔹 **Explanation:**

- `ping` sends **ICMP Echo Requests** to the target and waits for a reply.
- If the server responds, basic network connectivity is working.
- If the request times out, there’s a **network issue** preventing the server
  from reaching the destination.

#### **Possible Outcomes & What They Mean:**

| Output                                        | Interpretation                                                     |
| --------------------------------------------- | ------------------------------------------------------------------ |
| `64 bytes from google.com...`                 | The server can reach Google; no immediate problem.                 |
| `Request timed out`                           | Google did not reply; possible network or firewall issue.          |
| `ping: google.com: Name or service not known` | The hostname could not be resolved; possible **DNS issue**.        |
| `Destination Host Unreachable`                | The network route is broken or the **default gateway is missing**. |

---

### **Step 2: Check for DNS Resolution Issues**

#### 🔹 **Command:**

```bash
nslookup google.com
dig google.com
```

#### 🔹 **What is DNS Resolution?**

DNS (Domain Name System) translates human-friendly domain names (**google.com**)
into machine-readable IP addresses (**142.250.64.78**). If this process fails,
your system cannot connect to websites using domain names.

#### 🔹 **Explanation:**

- `nslookup` and `dig` query the DNS server for the IP address of `google.com`.
- If **both fail**, your system **cannot resolve domain names**.
- If `ping 8.8.8.8` works, but `nslookup google.com` fails, **your DNS is
  misconfigured**.

#### **Possible Outcomes & Solutions:**

| Output                                                 | Interpretation                           | Solution                                                |
| ------------------------------------------------------ | ---------------------------------------- | ------------------------------------------------------- |
| `Non-authoritative answer: 142.250.64.78`              | DNS resolution works fine.               | No action needed.                                       |
| `;; connection timed out; no servers could be reached` | No DNS servers are responding.           | Check `/etc/resolv.conf` for the correct DNS server.    |
| `SERVFAIL` or `REFUSED`                                | The DNS server is misconfigured or down. | Try a different DNS server like `8.8.8.8` (Google DNS). |

#### 🔹 **Solution: Check `/etc/resolv.conf`**

```bash
cat /etc/resolv.conf
```

This file contains the **DNS servers your system uses**. If it’s empty or
incorrect, update it:

🔹 **Fix: Set Google’s Public DNS**

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

This tells your system to use Google’s DNS for resolution.

---

### **Step 3: Check the Default Gateway & Routing**

#### 🔹 **Command:**

```bash
ip route
```

#### 🔹 **What is the Default Gateway?**

- The **default gateway** is the router that directs traffic from your server to
  the internet.
- If it is missing or incorrect, your server **cannot communicate with external
  networks**.

#### 🔹 **Example Output:**

```bash
default via 192.168.1.1 dev eth0 proto static
```

- This means the system sends all non-local traffic through `192.168.1.1`.

#### **Possible Issues & Fixes:**

| Output                         | Interpretation                      | Fix                                                |
| ------------------------------ | ----------------------------------- | -------------------------------------------------- |
| No `default via` line          | No default gateway is set.          | Add one: `ip route add default via <gateway-IP>`   |
| `default via 0.0.0.0 dev eth0` | Invalid gateway.                    | Correct it to a real router IP.                    |
| Destination Host Unreachable   | Routing is broken or misconfigured. | Restart networking: `systemctl restart networking` |

---

### **Step 4: Check Network Interface Status**

#### 🔹 **Command:**

```bash
ip a
ip link show eth0
```

#### 🔹 **Why Check the Interface?**

- If the network interface is **down**, the server cannot communicate.
- If it’s **misconfigured**, it might not receive an IP address.

#### **Possible Issues & Fixes:**

| Output             | Interpretation                           | Fix                                   |
| ------------------ | ---------------------------------------- | ------------------------------------- |
| `eth0: state DOWN` | The interface is disabled.               | Enable it: `ip link set eth0 up`      |
| No `inet` address  | No IP assigned.                          | Restart DHCP: `dhclient eth0`         |
| `inet 169.254.x.x` | The system failed to get a DHCP address. | Manually set IP or check DHCP server. |

---

### **Step 5: Check Firewall Rules**

#### 🔹 **Command:**

```bash
iptables -L
ufw status
```

#### 🔹 **Why Check the Firewall?**

- A misconfigured **firewall** can block outgoing traffic.
- If you cannot **ping external websites but can ping the local network**,
  firewall rules may be **blocking outbound connections**.

#### **Possible Issues & Fixes:**

| Output                          | Interpretation               | Fix                                      |
| ------------------------------- | ---------------------------- | ---------------------------------------- |
| `DROP all -- anywhere anywhere` | Outbound traffic is blocked. | Allow it: `iptables -A OUTPUT -j ACCEPT` |
| `ufw: inactive`                 | Firewall is off.             | No issue here.                           |

---

## Section 2: Slow Network Performance

Users are reporting that a service is running **slowly**. This could be due to
**high latency, packet loss, network congestion, or bandwidth exhaustion**.
Let’s systematically diagnose the issue.

---

### **Step 1: Measure Network Latency**

#### 🔹 **Command:**

```bash
ping -c 5 google.com
```

#### 🔹 **Explanation:**

- This sends **five ICMP Echo Requests** to `google.com` and measures **response
  time**.
- If latency is **high**, it could indicate **network congestion or routing
  issues**.

#### **Possible Outcomes & What They Mean:**

| Output                                                  | Interpretation                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------ |
| `64 bytes from google.com: icmp_seq=1 ttl=57 time=12ms` | Normal latency (~10-50ms is typical for external sites).           |
| `time=500ms` or higher                                  | High latency, likely **network congestion** or **bad routing**.    |
| `Request timed out`                                     | No response, possible **firewall, packet loss, or routing issue**. |

---

## **Step 2: Check Packet Routing**

#### 🔹 **Command:**

```bash
traceroute google.com
```

#### 🔹 **Explanation:**

- `traceroute` **maps the network path** between your server and the
  destination.
- It helps **identify slow hops** or **network bottlenecks**.

#### **Possible Outcomes & What They Mean:**

| Output                                        | Interpretation                                                       |
| --------------------------------------------- | -------------------------------------------------------------------- |
| Multiple hops showing `time=10ms, 15ms, 12ms` | Normal routing, no delays.                                           |
| A hop with `time=200ms, 300ms, *`             | Network congestion at that point.                                    |
| `* * *` for multiple hops                     | Possible **firewall blocking ICMP** or network failure at that node. |

---

### **Step 3: Capture Packets for Analysis**

#### 🔹 **Command:**

```bash
tcpdump -i eth0 port 80
```

#### 🔹 **Explanation:**

- Captures **real-time traffic** to analyze what is happening at the **packet
  level**.
- Helps check if **requests are being retransmitted**, leading to delays.

#### **Possible Outcomes & What They Mean:**

| Output                                | Interpretation                                                     |
| ------------------------------------- | ------------------------------------------------------------------ |
| Normal-looking HTTP packets           | The application is functioning fine.                               |
| Lots of retransmissions (TCP DUP ACK) | Network congestion or **bad connection**.                          |
| No traffic at all                     | The application might not be sending/receiving requests correctly. |

---

### **Step 4: Monitor Bandwidth Usage**

#### 🔹 **Command:**

```bash
iftop -i eth0
```

#### 🔹 **Explanation:**

- Shows a **real-time view** of bandwidth usage per connection.
- Helps **identify which process or IP** is consuming excessive bandwidth.

#### **Possible Outcomes & What They Mean:**

| Output                              | Interpretation                                         |
| ----------------------------------- | ------------------------------------------------------ |
| Normal-looking traffic (~50 Mbps)   | No bandwidth issue.                                    |
| A single IP consuming 90% bandwidth | That service is **hogging resources**.                 |
| Extremely low bandwidth (1-2 Mbps)  | **Network throttling** or a misconfigured QoS setting. |

---

### **Step 5: Check Network Interface Errors**

#### 🔹 **Command:**

```bash
ethtool eth0
```

#### 🔹 **Explanation:**

- Displays statistics about **interface performance** (e.g., **dropped packets,
  speed mismatches, link errors**).
- Helps diagnose **hardware-related issues**.

#### **Possible Outcomes & What They Mean:**

| Output                              | Interpretation                                                             |
| ----------------------------------- | -------------------------------------------------------------------------- |
| `Link detected: yes`                | The interface is up and working.                                           |
| `Speed: 100Mb/s` but expected 1Gb/s | The interface is **negotiating a lower speed**, slowing performance.       |
| `Rx errors: 1000`                   | Packets are being dropped due to **hardware issues or misconfigurations**. |

### **Final Summary: Troubleshooting Slow Network Performance**

| **Step**                      | **Command**               | **Purpose**                                    | **Fix**                                                             |
| ----------------------------- | ------------------------- | ---------------------------------------------- | ------------------------------------------------------------------- |
| **1. Measure Latency**        | `ping -c 5 google.com`    | See if response times are normal.              | If latency is high, move to next step.                              |
| **2. Check Routing**          | `traceroute google.com`   | Identify slow or failing network hops.         | If delay occurs at a specific hop, suspect network congestion.      |
| **3. Capture Packets**        | `tcpdump -i eth0 port 80` | Analyze packet flow for retransmissions.       | If excessive retransmissions, suspect packet loss.                  |
| **4. Monitor Bandwidth**      | `iftop -i eth0`           | Check if a process is overloading the network. | If a single IP is consuming all bandwidth, investigate further.     |
| **5. Check Interface Errors** | `ethtool eth0`            | Look for hardware issues affecting speed.      | If speed is lower than expected, check cables and network settings. |

---

## \*\*Section 3: Cannot SSH into a Remote Server

You're trying to **SSH into a remote server**, but the connection fails. This
could be due to **a misconfigured SSH service, firewall rules, network issues,
or incorrect permissions**. Let’s systematically diagnose the problem.

---

### **Step 1: Check If SSH Service Is Running**

#### 🔹 **Command:**

```bash
systemctl status ssh
```

#### 🔹 **Explanation:**

- This checks if the **SSH daemon (sshd)** is running on the remote machine.
- If SSH is not running, it will **reject all connection attempts**.

#### **Possible Outcomes & What They Mean:**

| Output                         | Interpretation                                     |
| ------------------------------ | -------------------------------------------------- |
| `Active: active (running)`     | SSH service is running properly.                   |
| `Active: failed` or `inactive` | The SSH service is down and needs to be restarted. |
| `Unit ssh.service not found`   | SSH is **not installed** on the system.            |

🔹 **Solution:** If the SSH service is down, restart it:

```bash
sudo systemctl restart ssh
```

If SSH is not installed, install it:

```bash
sudo apt install openssh-server  # Debian/Ubuntu
sudo yum install openssh-server  # RHEL/CentOS
```

---

### **Step 2: Verify the SSH Port Is Open**

#### 🔹 **Command:**

```bash
netstat -tulnp | grep 22
ss -tulnp | grep 22
```

#### 🔹 **Explanation:**

- These commands **check if SSH is listening on port 22** (or another configured
  port).
- If the port is **not open**, SSH connections will **fail**.

#### **Possible Outcomes & What They Mean:**

| Output                                  | Interpretation                                               |
| --------------------------------------- | ------------------------------------------------------------ |
| `tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN`   | SSH is listening on all interfaces (Good).                   |
| `tcp 0 0 127.0.0.1:22 0.0.0.0:* LISTEN` | SSH is only accessible locally (bad for remote connections). |
| No output                               | SSH is **not running** or is using a **different port**.     |

🔹 **Solution:**  
If SSH is running **only on localhost**, edit the SSH configuration file:

```bash
sudo nano /etc/ssh/sshd_config
```

Find this line:

```plaintext
ListenAddress 127.0.0.1
```

Change it to:

```plaintext
ListenAddress 0.0.0.0
```

Then restart SSH:

```bash
sudo systemctl restart ssh
```

---

### **Step 3: Check Firewall Rules**

#### 🔹 **Command:**

```bash
iptables -L | grep 22
ufw status
```

#### 🔹 **Explanation:**

- If the **firewall blocks port 22**, SSH connections will be **rejected**.

#### **Possible Outcomes & What They Mean:**

| Output                                       | Interpretation                               |
| -------------------------------------------- | -------------------------------------------- |
| `ACCEPT tcp -- anywhere anywhere tcp dpt:22` | SSH traffic is allowed.                      |
| `DROP all -- anywhere anywhere`              | The firewall is blocking SSH traffic.        |
| `Status: inactive` (from `ufw status`)       | No firewall issue (SSH should be reachable). |

🔹 **Solution:** If SSH is blocked, allow it:

```bash
sudo ufw allow 22/tcp
sudo systemctl restart ssh
```

Or, if using `iptables`:

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

---

### **Step 4: Test Network Connectivity**

#### 🔹 **Command:**

```bash
ping <server-ip>
```

#### 🔹 **Explanation:**

- If the server is **unreachable**, the issue is **not SSH-related but a network
  problem**.

#### **Possible Outcomes & What They Mean:**

| Output                                                   | Interpretation                         |
| -------------------------------------------------------- | -------------------------------------- |
| `64 bytes from <server-ip>: icmp_seq=1 ttl=57 time=12ms` | The server is reachable.               |
| `Request timed out`                                      | Network issue; check routes/firewalls. |
| `Destination Host Unreachable`                           | No route to the server exists.         |

🔹 **Solution:**  
If the server is **unreachable**, check the network configuration and routes:

```bash
ip route
```

If the default gateway is missing:

```bash
ip route add default via <gateway-ip>
```

---

### **Step 5: Verify User Permissions and SSH Key Issues**

#### 🔹 **Command:**

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

#### 🔹 **Explanation:**

- SSH will **reject connections** if file permissions are **too open** (for
  security reasons).

#### **Possible Outcomes & What They Mean:**

| Output                                                     | Interpretation                                   |
| ---------------------------------------------------------- | ------------------------------------------------ |
| `drwx------ 2 user user 4096 Feb 15 ~/.ssh`                | SSH directory permissions are correct.           |
| `-rw------- 1 user user 600 Feb 15 ~/.ssh/authorized_keys` | Authorized keys file is correctly secured.       |
| `-rw-r--r--` (public access)                               | SSH may **reject the key** for security reasons. |

🔹 **Solution:**  
Fix permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

### **Final Summary: Troubleshooting SSH Connectivity Issues**

| **Step**                         | **Command**            | **Purpose**                                  | **Fix**                                 |
| -------------------------------- | ---------------------- | -------------------------------------------- | --------------------------------------- | -------------------------------------- |
| **1. Check SSH Service**         | `systemctl status ssh` | Ensure SSH is running.                       | Restart or install SSH if needed.       |
| **2. Verify SSH Port**           | `netstat -tulnp        | grep 22`                                     | Check if SSH is listening.              | If not, change `sshd_config` settings. |
| **3. Check Firewall Rules**      | `iptables -L           | grep 22`                                     | Ensure SSH is not blocked.              | Allow port 22 in firewall rules.       |
| **4. Test Network Connectivity** | `ping <server-ip>`     | Check if the server is reachable.            | Fix routing if the host is unreachable. |
| **5. Verify User Permissions**   | `ls -l ~/.ssh`         | Ensure SSH keys and permissions are correct. | Adjust permissions using `chmod`.       |

---
