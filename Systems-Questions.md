# Questions - Systems

## **1. What is a Filesystem? How does it work?**

A filesystem organizes and stores data on a disk. It manages files, directories,
metadata, and permissions. Common types: **ext4, NTFS, XFS, ZFS**.

**How it works:**

- **Blocks/Inodes:** Data is stored in blocks; metadata (permissions, ownership)
  is in inodes.
- **Mounting:** A filesystem is mounted to make it accessible.

---

### **2. File Permissions & Properties**

Each file has three permission sets:

- **Owner (U), Group (G), Others (O)**
- Permissions: **Read (r), Write (w), Execute (x)**
- Represented as: `-rw-r--r--` (Owner: read/write, Group: read, Others: read)
- Use `ls -l` to check permissions, `chmod` to modify them.

**Properties:**

- **Owner:** User who created the file (`chown` to change).
- **Size, Modified Time, Type:** Shown with `ls -lh`.

---

### **3. File Types**

- **Regular (-):** Normal files.
- **Directory (d):** Contains files (`ls -l`).
- **Symbolic link (l):** Points to another file (`ln -s`).
- **Block device (b):** Represents a storage device.
- **Character device (c):** Represents serial devices like terminals.
- **Socket (s):** Inter-process communication endpoint.

Check type using `ls -l` or `file <filename>`.

---

### **4. Write Operation Failed – Debugging Steps**

1. **Check free space:** `df -h` (disk) / `du -sh <dir>` (folder).
2. **Check inode availability:** `df -i`.
3. **Check file permissions:** `ls -l <file>` / `ls -ld <dir>`.
4. **Check mount status:** `mount` / `df -T`.
5. **Check logs:** `dmesg | tail` (hardware issues), `journalctl -xe`.
6. **Check disk errors:** `fsck` (on unmounted filesystem).
7. **Check if file is in use:** `lsof <file>` / `fuser -v <file>`.

Let me know if you need a more specific explanation!

## **1. What is a Signal?**

A signal is an **asynchronous notification** sent to a process by the kernel or
another process to notify about an event (e.g., termination, interruption).

### **2. Common Signals:**

- `SIGINT (2)` – Interrupt (Ctrl + C)
- `SIGTERM (15)` – Graceful termination
- `SIGKILL (9)` – Force kill (cannot be caught)
- `SIGHUP (1)` – Terminal hang-up
- `SIGSEGV (11)` – Segmentation fault

### **3. How Signals Are Handled by the Kernel:**

1. **Signal Generation:**

   - Kernel generates signals (e.g., due to an error, user input).
   - Another process can send signals using `kill -SIGNAL PID`.

2. **Signal Delivery:**

   - Kernel places the signal in the **pending queue** of the process.
   - If a process has multiple pending signals, only **one instance of each
     type** is stored.

3. **Signal Handling:**

   - **Default action** (e.g., terminate, ignore, stop).
   - **Custom handler** (process can define how to handle the signal).
   - **Ignored signals** (except `SIGKILL` & `SIGSTOP`, which cannot be
     ignored).

4. **Signal Execution:**
   - When a process runs, the kernel **checks pending signals** and handles them
     before resuming execution.

### **4. Checking & Sending Signals:**

- **List signals:** `kill -l`
- **Send a signal:** `kill -SIGTERM <PID>`
- **Handle a signal in code (C example):**

  ```c
  #include <signal.h>
  #include <stdio.h>

  void handler(int sig) {
      printf("Received signal %d\n", sig);
  }

  int main() {
      signal(SIGINT, handler);  // Custom handler for Ctrl+C
      while (1);
      return 0;
  }
  ```

## **Zombie Process (Defunct Process)**

A **zombie process** is a process that has **completed execution** but still has
an entry in the **process table** because its parent has not read its exit
status.

### **How It Happens:**

1. **Child process exits** → Sends exit status to the parent.
2. **Parent doesn't call `wait()`** → The child remains in a **zombie state**
   (defunct).
3. **Entry stays in process table** → Occupies system resources until the parent
   reads the status.

### **Identifying Zombie Processes:**

- Run `ps aux | grep Z` (Look for **Z** in the STAT column).

### **Fixing a Zombie Process:**

- **If parent is active:**
  - Call `wait()` in the parent process to clean up.
- **If parent is unresponsive:**
  - Find parent `PPID` using `ps -o ppid= -p <zombie_PID>`.
  - Kill parent: `kill -9 <PPID>` (init/systemd will clean up the zombie).
- **Reboot as a last resort** if too many zombies exist.

## **Understanding `iostat` Output**

`iostat` shows CPU and disk I/O performance metrics, helping diagnose system
bottlenecks.

#### **1. User vs. System CPU Load (`%user` vs. `%system`)**

- **`%user`** – CPU time spent executing user-space processes (applications).
- **`%system`** – CPU time spent on **kernel-level** tasks (handling syscalls,
  drivers, etc.).

💡 **High `%system`** means the system is handling many kernel operations, which
can slow down applications.

#### **2. `iowait%` – What It Means**

- **`%iowait`** – The percentage of CPU time spent **waiting for disk I/O to
  complete**.
- High `iowait` means the CPU is idle, waiting for **slow disk operations** to
  finish.

💡 **High `iowait` → Disk is a bottleneck** (e.g., slow HDD, heavy disk
reads/writes).

#### **3. Cache vs. Buffers (`free -m` Output)**

- **Cache** – Stores **recently used file data** for quick access.
- **Buffers** – Store **metadata and temporary data** before writing to disk.

💡 **Why Needed?**

- Reduces disk reads/writes (improves performance).
- In-memory access is much faster than disk.

#### **4. How Much Cache Is Needed?**

- The kernel dynamically adjusts cache size.
- More RAM → More cache → Faster performance.
- Use `vmstat` and `free -m` to monitor cache usage.

#### **5. Improving Disk Performance**

- **Use SSDs** instead of HDDs.
- **Increase RAM** to allow more caching.
- **Optimize I/O scheduling** (e.g., `noop` for SSDs, `deadline` for DB
  servers).
- **Use RAID or LVM** for better disk performance.
- **Tune `sysctl` parameters** (e.g., `vm.dirty_ratio` for write buffering).

#### **6. Finding the Bottleneck**

Check:

- **High `iowait`** → Disk bottleneck.
- **High `%system`** → Kernel-intensive tasks (check with `top`).
- **High CPU usage but low I/O** → CPU bottleneck.
- **Check `iostat -dx`** for per-disk load.

## **What Happens When a Client Opens a Web Page?**

1. **Domain Name System (DNS) Resolution:**

   - The browser converts the **URL** (e.g., `example.com`) into an **Internet
     Protocol (IP) address** using **DNS lookup**.

2. **Transmission Control Protocol (TCP) Handshake:**

   - The browser establishes a **TCP connection** with the web server using the
     **three-way handshake** (SYN, SYN-ACK, ACK).

3. **Hypertext Transfer Protocol Secure (HTTPS) / Transport Layer Security (TLS)
   Handshake (If Secure Site):**

   - If HTTPS is used, the browser and server perform a **TLS handshake** to
     establish a **secure encrypted connection**.

4. **Hypertext Transfer Protocol (HTTP) Request Sent:**

   - The browser sends an **HTTP request** (`GET /index.html HTTP/1.1`) to fetch
     the page.

5. **Server Processes Request:**

   - The **web server** (e.g., Nginx, Apache) processes the request.
   - It may run backend logic (e.g., PHP, Node.js) or query a **database**.

6. **HTTP Response Sent:**

   - The server returns an **HTTP response** (e.g., `200 OK`) with the requested
     **Hypertext Markup Language (HTML) page**.

7. **Browser Renders the Page:**

   - The browser **parses HTML** and starts fetching **Cascading Style Sheets
     (CSS), JavaScript, and images** (each requires separate requests).
   - JavaScript execution, **CSS styling, and Document Object Model (DOM)
     construction** happen in parallel.

8. **Page Displayed:**

   - Once all content is loaded, the browser **paints the final webpage** on the
     screen.

9. **Additional Requests:**
   - If there are **Asynchronous JavaScript and XML (AJAX) requests, WebSockets,
     or API calls**, they run in the background for dynamic content.

---

### **Debugging & Optimization Tips:**

- **Slow DNS resolution?** → Use `nslookup example.com`.
- **Slow page load?** → Check **network requests** (`DevTools → Network`).
- **Too many requests?** → Enable **caching, compression, Content Delivery
  Network (CDN)**.
- **Blocking scripts?** → Use **asynchronous JavaScript (`async`/`defer`)**.

## **How Does HTTP (Hypertext Transfer Protocol) Work?**

HTTP is a **request-response protocol** used for communication between clients
(browsers) and servers over the internet. It follows a **stateless model**,
meaning each request is independent.

---

### **1. Client Sends an HTTP Request**

The browser (client) sends a request to the web server, specifying:

- **Method:** What action to perform (`GET`, `POST`, `PUT`, `DELETE`).
- **URL:** The resource being requested.
- **Headers:** Metadata (e.g., `User-Agent`, `Accept`, `Authorization`).
- **Body:** (Only in `POST`, `PUT`) Contains data being sent.

📌 **Example HTTP Request:**

```http
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

---

### **2. Server Processes the Request**

- The **web server (e.g., Nginx, Apache)** receives the request.
- It may fetch data from a **database** or run backend logic.

---

### **3. Server Sends an HTTP Response**

- **Status Code** (e.g., `200 OK`, `404 Not Found`,
  `500 Internal Server Error`).
- **Headers** (e.g., `Content-Type`, `Cache-Control`).
- **Body** (e.g., HTML, JSON, file content).

📌 **Example HTTP Response:**

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1024

<html>
  <body>Hello, World!</body>
</html>
```

---

### **4. Browser Renders the Response**

- If it's an **HTML page**, it is **parsed and displayed**.
- If there are additional **CSS, JavaScript, images**, the browser makes
  separate requests for them.

---

### **HTTP vs HTTPS**

- **HTTP (Hypertext Transfer Protocol)** → Plain text, **not secure**.
- **HTTPS (Hypertext Transfer Protocol Secure)** → Uses **TLS (Transport Layer
  Security)** for **encryption, authentication, and integrity**.

---

### **Common HTTP Methods**

- **GET** → Retrieve data.
- **POST** → Send data to the server.
- **PUT** → Update/replace a resource.
- **DELETE** → Remove a resource.

---

### **Key Features of HTTP:**

✅ **Stateless:** Each request is independent (cookies/sessions help maintain
state).  
✅ **Flexible:** Supports various data formats (HTML, JSON, XML).  
✅ **Extensible:** Uses headers for additional features (e.g., caching,
authentication).

### **How Does a Router Work?**

A **router** is a networking device that connects multiple networks (e.g., home
network to the internet) and directs data packets based on **IP addresses**.

#### **1. Packet Forwarding (Routing Process):**

- The router receives an **incoming packet**.
- It examines the **destination IP address**.
- It checks its **routing table** to find the best path.
- It forwards the packet to the appropriate **next hop (another router or
  device)**.

#### **2. Key Router Functions:**

✅ **Network Address Translation (NAT):** Maps private IPs to a public IP (used
in home networks).  
✅ **Dynamic Routing:** Uses protocols like **OSPF (Open Shortest Path First),
BGP (Border Gateway Protocol)**.  
✅ **Firewall & Security:** Filters packets based on rules (prevents
unauthorized access).  
✅ **DHCP (Dynamic Host Configuration Protocol) Server:** Assigns IP addresses
dynamically to devices.

---

### **Difference Between Router and Switch**

| Feature               | **Router**                                  | **Switch**                                              |
| --------------------- | ------------------------------------------- | ------------------------------------------------------- |
| **Purpose**           | Connects different networks (LAN to WAN).   | Connects devices within the same network (LAN).         |
| **Works at**          | Layer 3 (Network Layer, uses IP addresses). | Layer 2 (Data Link Layer, uses MAC addresses).          |
| **Packet Forwarding** | Uses **IP addresses** and routing tables.   | Uses **MAC addresses** and switching tables.            |
| **Traffic Handling**  | Routes data between **different networks**. | Transfers data between **devices in the same network**. |
| **Network Isolation** | Creates separate subnets.                   | Works within one subnet (unless VLANs are used).        |
| **Speed**             | Slower due to complex processing.           | Faster, designed for local traffic.                     |

## **Load vs CPU Utilization**

### **1. CPU Utilization (%)**

- Measures **how busy the CPU is** processing tasks.
- Represented as a **percentage** (`0%` = idle, `100%` = fully used).
- Can be broken down into:
  - **User (`%user`)** → CPU time spent on user-space processes.
  - **System (`%system`)** → CPU time spent on kernel tasks.
  - **Idle (`%idle`)** → CPU waiting with no work.
  - **I/O Wait (`%iowait`)** → CPU waiting for disk operations.

📌 **Check with:** `top`, `htop`, `mpstat -P ALL 1`

---

### **2. Load Average**

- Measures the **average number of processes** waiting for CPU **or I/O**.
- Displayed as three values:
  - **1 min avg**, **5 min avg**, **15 min avg** (e.g., `1.5 2.0 2.5`).
- **Ideal Value:** Should be **≤ CPU cores count**
  (`load > cores → overloaded`).

📌 **Check with:** `uptime`, `cat /proc/loadavg`, `top`

---

### **Key Differences**

| Feature                | **CPU Utilization**               | **Load Average**                         |
| ---------------------- | --------------------------------- | ---------------------------------------- |
| **Definition**         | Percentage of CPU used.           | Number of processes waiting for CPU/I/O. |
| **Focuses On**         | **How much CPU is working**.      | **How many processes are waiting**.      |
| **Includes I/O Wait?** | No (unless specifically checked). | Yes (if processes are waiting).          |
| **Ideal Value**        | ~80% (depends on workload).       | Should be ≤ number of CPU cores.         |
| **Indicates?**         | CPU stress or high process usage. | Overall system load (CPU + I/O wait).    |

## Suppose there is a server with high CPU load but there is no process with high CPU time. What could be the reason for that? How do you debug this problem? Does your solution always work, and if not, what’s the reason for that?

### **Possible Reasons for High CPU Load Without High CPU Usage per Process:**

1. **High I/O Wait (`%iowait`)**

   - CPU is waiting for **slow disk or network I/O**.
   - **Check with:** `iostat -x 1`, `vmstat 1` (look for high `%iowait`).
   - **Fix:** Use **SSDs**, optimize queries, increase RAM for caching.

2. **High Interrupts (`%irq` / `%softirq`)**

   - Caused by **excessive hardware interrupts** (e.g., network, disk, USB).
   - **Check with:** `cat /proc/interrupts`, `vmstat 1` (high `%irq`,
     `%softirq`).
   - **Fix:** Tune **network/disk drivers**, reduce packet bursts, update
     firmware.

3. **Kernel Tasks or Context Switching Overhead**

   - **Frequent process switching** (e.g., too many short-lived threads).
   - **Check with:** `mpstat -P ALL 1` (high `%system`), `pidstat -w 1`.
   - **Fix:** Reduce **context switching**, optimize **thread management**.

4. **Run Queue Overload**

   - Too many **blocked processes** waiting for CPU/I/O.
   - **Check with:** `top`, `uptime` (high **load average**, but low CPU usage).
   - **Fix:** Identify blocked tasks (`ps -eo state,pid,cmd | grep 'D'` for I/O
     wait).

5. **Throttling (CPU Frequency Scaling)**
   - **Power-saving mode** or **thermal throttling** can reduce CPU speed.
   - **Check with:** `cpufreq-info`, `sensors` (look for overheating).
   - **Fix:** Disable power scaling (`cpupower frequency-set -g performance`),
     improve cooling.

---

### **Debugging Steps:**

1. **Check CPU Utilization & Load:**

   - `top`, `htop`, `uptime` → High load but no heavy CPU process?

2. **Check I/O Wait & Disk Usage:**

   - `iostat -x 1`, `vmstat 1` → High `%iowait`?

3. **Check Kernel & Interrupts:**

   - `cat /proc/interrupts`, `mpstat -P ALL 1` → High `%irq`?

4. **Check Power & CPU Scaling:**
   - `cpufreq-info`, `sensors` → Throttling issue?

---

### **Does This Always Work?**

❌ **No, because:**

- Some CPU load is **invisible** to normal tools (e.g., **kernel threads, hidden
  daemons**).
- Some workloads (e.g., **packet storms, lock contention**) don’t show high
  per-process usage.
- If it’s a **hypervisor (VM),** the issue could be in the host system, not the
  guest.

## **Problems with Inter-Process Communication (IPC)**

1. **Race Conditions**

   - Multiple processes accessing shared resources **simultaneously** can lead
     to data corruption.
   - **Fix:** Use **locks, semaphores, or message queues**.

2. **Deadlocks**

   - Two processes waiting on each other to release resources.
   - **Fix:** Implement **timeouts, resource ordering**.

3. **Synchronization Issues**

   - Processes may read/write shared memory at the wrong time.
   - **Fix:** Use **mutexes, condition variables**.

4. **Data Loss in Pipes**

   - If the pipe buffer is full, the writer **blocks or loses data**.
   - If the reader is too slow, **data may be lost** in unnamed pipes.

5. **Limited Buffer Size**

   - Pipes and message queues have **fixed buffer sizes**.
   - **Fix:** Use shared memory for large data or increase buffer size.

6. **Security Concerns**
   - Unauthorized processes can **access shared memory or named pipes**.
   - **Fix:** Use proper **permissions and access control**.

---

### **How the OS Transfers Data in a Pipe**

1. **Process A (Writer) writes to the pipe.**
   - Data is stored in a **kernel buffer**.
2. **Kernel manages the buffer (FIFO).**
   - If the buffer is **full**, the writer **blocks** until space is available.
   - If the buffer is **empty**, the reader **blocks** until data arrives.
3. **Process B (Reader) reads from the pipe.**
   - The OS copies data from the **kernel buffer** to user-space memory.

📌 **Example Pipe Usage in C:**

```c
int pipefd[2];
pipe(pipefd);
write(pipefd[1], "Hello", 5);
read(pipefd[0], buffer, 5);
```

---

### **Limits & Bottlenecks in IPC**

| **IPC Method**     | **Limits & Bottlenecks**                                         |
| ------------------ | ---------------------------------------------------------------- |
| **Pipes**          | Limited buffer size, one-way communication, slow for large data. |
| **Message Queues** | Limited message size, kernel overhead, requires synchronization. |
| **Shared Memory**  | Needs explicit synchronization, race conditions possible.        |
| **Sockets**        | High latency for local processes, needs serialization.           |

---

### **How to Debug IPC Issues**

1. **Check buffer size:** `ulimit -a` (pipe buffer).
2. **Use `strace`:** `strace -p <pid>` to trace system calls.
3. **Monitor synchronization:** Look for **deadlocks, race conditions**.

## **How Does Packet Routing Work?**

### **1. How Does the Source Computer Know Where to Route Packets?**

- The source computer checks the **destination IP address** in the packet
  header.
- It refers to its **routing table (`ip route show`)** to decide where to send
  the packet:
  - If the **destination is in the same subnet**, it sends the packet
    **directly**.
  - If not, it forwards the packet to the **default gateway (router)**.

📌 **Check Routing Table:**

```sh
ip route show
```

---

### **2. How Do Packets Move Across a Network?**

1. **Source Computer Sends Packet**

   - Adds **destination IP address** (Layer 3 – Network).
   - Wraps in an **Ethernet frame with the MAC address** of the next hop (Layer
     2 – Data Link).

2. **Router Receives the Packet**

   - Strips the Ethernet frame.
   - Checks the **destination IP** against its **routing table**.
   - If destination is known, forwards to the **next hop**.
   - If unknown, drops the packet or sends an **ICMP "Destination
     Unreachable"**.

3. **Packet Hops Across Multiple Routers**

   - Each router updates the **TTL (Time-To-Live) field** (prevents infinite
     loops).
   - Uses **OSPF (Open Shortest Path First) or BGP (Border Gateway Protocol)**
     for path selection.

4. **Destination Computer Receives Packet**
   - Strips headers, reconstructs data.
   - Passes it to the application.

---

### **Key Concepts in Packet Routing**

| **Concept**                                  | **Explanation**                                    |
| -------------------------------------------- | -------------------------------------------------- |
| **Routing Table**                            | Stores paths for known networks (`ip route show`). |
| **Default Gateway**                          | The router used when no specific route exists.     |
| **TTL (Time-To-Live)**                       | Limits hops to prevent loops (decreases per hop).  |
| **ICMP (Internet Control Message Protocol)** | Used for errors (`ping`, `traceroute`).            |
| **OSPF & BGP**                               | Dynamic routing protocols for path selection.      |

---

### **Debugging Routing Issues**

1. **Check routing table:** `ip route show`
2. **Check connectivity:** `ping <destination IP>`
3. **Trace packet path:** `traceroute <destination>`
4. **Check ARP table (for MAC resolution):** `arp -a`

## **OSPF (Open Shortest Path First) – Explained**

OSPF is a **dynamic routing protocol** used in **IP networks** to find the
shortest path between routers. It operates within **Autonomous Systems (AS)**
and uses **link-state routing**.

---

### **How OSPF Works**

1. **Neighbor Discovery & Adjacency Formation**

   - Routers exchange **Hello packets** to discover OSPF neighbors.
   - They establish an **adjacency** if parameters match (area ID,
     authentication, etc.).

2. **Link-State Database (LSDB) Synchronization**

   - Routers exchange **Link-State Advertisements (LSAs)** to share their
     network topology.
   - Each router builds a complete **map of the network**.

3. **Shortest Path Calculation (SPF Algorithm)**

   - Routers use **Dijkstra's Algorithm** to compute the shortest path to all
     destinations.
   - The best routes are stored in the **Routing Table**.

4. **Packet Forwarding**
   - OSPF selects the **best route** based on **cost (metric)** (lower cost =
     better path).
   - If multiple equal-cost paths exist, it does **Equal-Cost Multi-Path (ECMP)
     routing**.

---

### **Key Features of OSPF**

| **Feature**                     | **Explanation**                                          |
| ------------------------------- | -------------------------------------------------------- |
| **Link-State Protocol**         | Each router knows the full network topology.             |
| **Dijkstra’s Algorithm**        | Computes the shortest path to each destination.          |
| **Areas & Hierarchical Design** | OSPF divides networks into **areas** (reduces overhead). |
| **Fast Convergence**            | Updates network changes quickly with LSAs.               |
| **Supports Load Balancing**     | Uses ECMP if multiple best routes exist.                 |

### **RIP (Routing Information Protocol) – Explained**

RIP is a **distance-vector routing protocol** that determines the best route
based on **hop count**. It is simple but inefficient for large networks.

---

### **How RIP Works**

1. **Routers Exchange Routing Tables**

   - Every **30 seconds**, routers broadcast their routing tables to neighbors.
   - Each route has a **hop count** (number of routers to the destination).

2. **Routing Table Updates**

   - If a router receives a **shorter path**, it updates its table.
   - If a route is unreachable, it is **marked as "infinity" (16 hops,
     considered unreachable)**.

3. **Loop Prevention**
   - Uses **Split Horizon, Route Poisoning, Hold-Down Timers** to prevent
     routing loops.

---

### **Key Features of RIP**

| **Feature**                  | **Explanation**                                    |
| ---------------------------- | -------------------------------------------------- |
| **Distance-Vector Protocol** | Uses hop count as the metric.                      |
| **Max Hop Count = 15**       | Any route with 16+ hops is considered unreachable. |
| **Slow Convergence**         | Updates every **30 seconds**, leading to delays.   |
| **Uses UDP (Port 520)**      | Does not use TCP, making it lightweight.           |

---

### **RIP Versions**

| **Version** | **Key Differences**                                                             |
| ----------- | ------------------------------------------------------------------------------- |
| **RIPv1**   | Classful, no support for subnet masks.                                          |
| **RIPv2**   | Classless, supports **CIDR (Classless Inter-Domain Routing)** & authentication. |

---

### **RIP vs. OSPF**

| **Protocol** | **Type**        | **Metric Used**           | **Best Use Case**         |
| ------------ | --------------- | ------------------------- | ------------------------- |
| **RIP**      | Distance-Vector | Hop Count (≤ 15)          | Small/simple networks     |
| **OSPF**     | Link-State      | Cost (based on bandwidth) | Large enterprise networks |

### **Understanding the Question: Configuring & Using a Client/Server Network Service**

This question tests your knowledge of setting up and managing a **network
service**. You need to:

1. **Pick a common network service** (e.g., SSH, HTTP, DNS, FTP, NFS).
2. **Explain how it works internally** (client-server interaction, protocol
   details).
3. **Discuss its features and configuration** (setup steps, security,
   troubleshooting).

---

## **Example: SSH (Secure Shell) – A Client/Server Network Service**

### **1. How SSH Works Internally**

- SSH is a **secure protocol** used for remote login to servers over an
  **encrypted connection**.
- Uses **TCP (Port 22)** for communication.
- Establishes a **client-server connection** with:
  1. **Key Exchange (Diffie-Hellman, RSA, etc.)** – Securely shares encryption
     keys.
  2. **Authentication** – User logs in via **password or SSH key**.
  3. **Encrypted Data Transmission** – Commands and responses are securely
     exchanged.

---

### **2. Features of SSH**

✅ **Encrypted Communication** – Prevents eavesdropping.  
✅ **Public/Private Key Authentication** – More secure than passwords.  
✅ **Port Forwarding (Tunneling)** – Allows secure access to internal
services.  
✅ **Multiplexing** – Can run multiple sessions over one connection.

---

### **3. Configuring SSH Server (Linux Example)**

**Install SSH Server:**

```sh
sudo apt update && sudo apt install openssh-server
```

**Start & Enable SSH:**

```sh
sudo systemctl enable ssh
sudo systemctl start ssh
```

**Modify Config (`/etc/ssh/sshd_config`):**

- Change default port (`Port 2222`).
- Disable root login (`PermitRootLogin no`).
- Enable key-based auth (`PasswordAuthentication no`).

**Restart SSH Service:**

```sh
sudo systemctl restart ssh
```

---

### **4. Debugging SSH Issues**

**Check if SSH is running:**

```sh
systemctl status ssh
```

**Check listening ports:**

```sh
netstat -tulnp | grep ssh
```

**Check logs:**

```sh
journalctl -u ssh --no-pager | tail -n 20
```

## **Setting Up SSH Without a Password (Key-Based Authentication)**

You can configure **SSH key-based authentication** to log in **without a
password**, using **public-private key pairs**.

---

### **1. Generate SSH Key Pair on the Client**

Run this on your **local machine** (client):

```sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

✅ **`-t rsa`** → Use RSA key.  
✅ **`-b 4096`** → 4096-bit encryption.  
✅ **`-f ~/.ssh/id_rsa`** → Saves the key file.  
✅ **`-N ""`** → No passphrase.

---

### **2. Copy the Public Key to the SSH Server**

Use `ssh-copy-id` to transfer the key automatically:

```sh
ssh-copy-id -i ~/.ssh/id_rsa.pub user@server_ip
```

**OR** manually append it to the server's `authorized_keys`:

```sh
cat ~/.ssh/id_rsa.pub | ssh user@server_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

✅ Creates `~/.ssh/authorized_keys` if it doesn’t exist.

---

### **3. Secure Permissions on the SSH Server**

Run this **on the server**:

```sh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

✅ Prevents unauthorized access to SSH files.

---

### **4. Disable Password Authentication (Optional for Security)**

Edit SSH config on the server:

```sh
sudo nano /etc/ssh/sshd_config
```

Change:

```ini
PasswordAuthentication no
PermitRootLogin no
```

Restart SSH service:

```sh
sudo systemctl restart ssh
```

---

### **5. Test SSH Login**

Now, SSH without a password:

```sh
ssh user@server_ip
```

## How many addresses are in a /27 network

A **/27 network** has a **subnet mask of 255.255.255.224**, meaning **5 bits are
used for host addresses**.

### **Formula to Calculate Addresses:**

Total addresses = **2^(32 - subnet mask)**  
= **2^(32 - 27) = 2^5 = 32 addresses**

### **Breakdown of Addresses in /27:**

- **Total IPs:** **32**
- **Usable IPs:** **30** (excluding **1 network address** and **1 broadcast
  address**)
- **Network Address:** First IP (all host bits = 0)
- **Broadcast Address:** Last IP (all host bits = 1)

### **Example: /27 Subnet (192.168.1.0/27)**

| Type                  | Address      |
| --------------------- | ------------ |
| **Network Address**   | 192.168.1.0  |
| **First Usable IP**   | 192.168.1.1  |
| **Last Usable IP**    | 192.168.1.30 |
| **Broadcast Address** | 192.168.1.31 |

**/27 has 32 total addresses, 30 usable IPs.**

## **What is a File Descriptor?**

A **file descriptor (FD)** is a **unique integer identifier** assigned by the
operating system to **open files, sockets, pipes, or other I/O resources** in a
process.

---

### **File Descriptor Basics:**

- When a process opens a file, the OS assigns it a **file descriptor (FD)**.
- The process uses this FD to read/write data instead of the file name.
- FDs are managed in a **per-process file descriptor table**.

---

### **Standard File Descriptors (Always Open by Default):**

| **FD** | **Description**            | **Device**                |
| ------ | -------------------------- | ------------------------- |
| **0**  | Standard Input (`stdin`)   | Keyboard (default input)  |
| **1**  | Standard Output (`stdout`) | Terminal (default output) |
| **2**  | Standard Error (`stderr`)  | Terminal (for errors)     |

📌 **Example:** Redirecting output using file descriptors:

```sh
ls > output.txt  # Redirect stdout (FD 1) to a file
ls 2> error.txt  # Redirect stderr (FD 2) to a file
```

## **How to Load a Module into the Linux Kernel**

A **kernel module** is a piece of code that can be dynamically loaded into the
**Linux kernel** to add functionality (e.g., device drivers).

---

### **1. Check Existing Modules**

Before loading a module, check if it is already loaded:

```sh
lsmod | grep <module_name>
```

---

### **2. Load a Module**

✅ **Using `insmod` (Direct Insertion)**

```sh
sudo insmod <module_name>.ko
```

- **Requires the full path** to the `.ko` (kernel object) file.
- No dependency handling.

✅ **Using `modprobe` (Recommended)**

```sh
sudo modprobe <module_name>
```

- Loads the module **with dependencies** automatically.
- Searches for modules in `/lib/modules/$(uname -r)/`.

---

### **3. Verify Module is Loaded**

```sh
lsmod | grep <module_name>
```

---

### **4. Unload a Module**

✅ **Using `rmmod` (Remove Module)**

```sh
sudo rmmod <module_name>
```

- Works only if no process is using the module.

✅ **Using `modprobe -r` (Recommended)**

```sh
sudo modprobe -r <module_name>
```

- Removes the module and **resolves dependencies**.

---

### **5. Load Module on Boot (Persistent Loading)**

Add module name to:

```sh
echo "<module_name>" | sudo tee -a /etc/modules-load.d/custom.conf
```

---

### **Debugging Issues**

1. **Check dmesg logs for errors:**

   ```sh
   dmesg | tail -20
   ```

2. **Check if module exists:**

   ```sh
   find /lib/modules/$(uname -r) -name "<module_name>.ko"
   ```

### **How to Trace All Function Calls in a Running Process**

To trace function calls in a running process, use **`strace`** (for system
calls) or **`ltrace`** (for library calls).

---

### **1. Trace System Calls (`strace`)**

✅ **Attach to a running process (`-p <PID>`)**

```sh
sudo strace -p <PID>
```

✅ **Trace a command from the start**

```sh
strace -f -o trace.log <command>
```

✅ **Filter by specific system calls**

```sh
strace -e open,read,write -p <PID>
```

✅ **Show timestamps (`-t`)**

```sh
strace -t -p <PID>
```

📌 **Use Case:** Debugging file/network access, permissions, process execution.

---

### **2. Trace Library Calls (`ltrace`)**

✅ **Attach to a running process**

```sh
sudo ltrace -p <PID>
```

✅ **Run a command with function tracing**

```sh
ltrace -f -o ltrace.log <command>
```

📌 **Use Case:** Debugging shared library calls (e.g., `printf()`, `malloc()`).

---

### **3. Trace Kernel-Level Calls (`perf` & `ftrace`)**

✅ **Using `perf` for function profiling**

```sh
sudo perf record -p <PID>
sudo perf report
```

✅ **Using `ftrace` for detailed kernel tracing**

```sh
echo function > /sys/kernel/debug/tracing/current_tracer
cat /sys/kernel/debug/tracing/trace
```

📌 **Use Case:** Analyzing CPU bottlenecks, kernel debugging.

## **Where is DNS Information Stored on a Linux System?**

DNS information is stored in various locations depending on the configuration
and DNS resolution method used.

---

### **1. Primary DNS Configuration Files**

✅ **`/etc/resolv.conf`** – Stores the system's DNS servers.

```sh
cat /etc/resolv.conf
```

📌 Example:

```ini
nameserver 8.8.8.8
nameserver 1.1.1.1
```

- Used by the **glibc resolver** for DNS lookups.
- May be dynamically updated by **NetworkManager, DHCP, or systemd-resolved**.

✅ **`/etc/nsswitch.conf`** – Defines the order of name resolution methods.

```sh
cat /etc/nsswitch.conf | grep hosts
```

📌 Example:

```ini
hosts: files dns myhostname
```

- Controls whether the system checks `/etc/hosts` before querying DNS.

✅ **`/etc/hosts`** – Static hostname-IP mappings (bypasses DNS).

```sh
cat /etc/hosts
```

📌 Example:

```ini
127.0.0.1 localhost
192.168.1.10 myserver.local
```

## **Bash Script to Find the Top 3 Most Repeated Words in a Paragraph**

You can use the following one-liner in **Bash** to process a paragraph and
output the top 3 most repeated words:

```bash
echo "Your paragraph here" | tr -d '[:punct:]' | tr ' ' '\n' | awk '{count[$1]++} END {for (word in count) print count[word], word}' | sort -nr | head -3
```

---

### **Explanation:**

1. **`tr -d '[:punct:]'`** → Removes punctuation.
2. **`tr ' ' '\n'`** → Converts spaces to new lines (one word per line).
3. **`awk '{count[$1]++} END {for (word in count) print count[word], word}'`** →
   Counts occurrences of each word.
4. **`sort -nr`** → Sorts by frequency (descending).
5. **`head -3`** → Outputs the top 3 most repeated words.

---

### **Example Usage**

```bash
echo "This is a test. This test is just a simple test." | tr -d '[:punct:]' | tr ' ' '\n' | awk '{count[$1]++} END {for (word in count) print count[word], word}' | sort -nr | head -3
```

**Output:**

```
3 test
2 is
2 This
```

## **What Happens When You Type `telnet www.facebook.com 80`?**

Typing `telnet www.facebook.com 80` initiates a connection to Facebook's web
server over **port 80 (HTTP)**. Let’s break it down across all **7 OSI layers**
and related **packet layouts**.

---

### **📌 OSI Layer Breakdown**

### **1. Application Layer (Layer 7)**

- `telnet` is a **client application** used for raw communication with a server.
- It initiates an **HTTP request** when you manually type HTTP commands
  (`GET / HTTP/1.1`).

---

### **2. Presentation Layer (Layer 6)**

- Ensures **data formatting** (e.g., text encoding, SSL/TLS encryption if HTTPS
  was used).
- Since you use `telnet` on **port 80**, **no encryption** is involved.

---

### **3. Session Layer (Layer 5)**

- Establishes and maintains the session between **your client and Facebook's
  server**.
- Uses a **TCP handshake** to maintain a persistent connection.

---

### **4. Transport Layer (Layer 4)**

- **Protocol Used:** **TCP (Transmission Control Protocol)**.
- TCP ensures **reliable, ordered delivery** of the HTTP request.
- **3-Way Handshake occurs**:
  1. **SYN** → Client sends **SYN packet** to request a connection.
  2. **SYN-ACK** → Server responds, acknowledging.
  3. **ACK** → Client confirms, and the connection is established.

📌 **Packet Layout at Transport Layer (TCP Header):** | Source Port |
Destination Port | Sequence Number | ACK Number | Flags (SYN, ACK, FIN, etc.) |
|------------|----------------|----------------|------------|-----------------------------|
| Random Port (e.g., 54321) | 80 | 12345678 | 0 | SYN |

---

### **5. Network Layer (Layer 3)**

- **IP (Internet Protocol) is responsible for routing**.
- The client first **resolves `www.facebook.com` to an IP address** using
  **DNS**:

  ```sh
  nslookup www.facebook.com
  ```

- A packet with **source IP (your device) → destination IP (Facebook server)**
  is created.

📌 **Packet Layout at Network Layer (IP Header):** | Source IP | Destination IP
| Protocol (TCP/UDP) | |-----------|---------------|------------------| |
192.168.1.10 | 31.13.70.36 (Facebook) | TCP |

---

### **6. Data Link Layer (Layer 2)**

- **Ethernet Frame (MAC Address Handling)**.
- The client checks its **ARP cache** (`arp -a`) for the **MAC address** of the
  **next-hop router**.
- If not found, it sends an **ARP request** to get the MAC address.
- The Ethernet frame is then sent to the **router/gateway**.

📌 **Packet Layout at Data Link Layer (Ethernet Frame):** | Source MAC |
Destination MAC | Type (IPv4/IPv6) |
|------------|----------------|----------------| | 00:1A:2B:3C:4D:5E |
00:1F:2E:3D:4C:5B | IPv4 |

---

### **7. Physical Layer (Layer 1)**

- The Ethernet frame is **converted into electrical, radio, or optical
  signals**.
- It is transmitted through:
  - **Ethernet (Wired Network)**
  - **Wi-Fi (Wireless Network)**
  - **Fiber Optic (ISP Backbone)**

---

### **📌 What Happens Next?**

1. Facebook's **server receives** the **TCP SYN packet** and completes the
   handshake.
2. The client **sends an HTTP request**:

   ```http
   GET / HTTP/1.1
   Host: www.facebook.com
   ```

3. Facebook's **web server responds** with an HTTP **200 OK** and serves the
   webpage.

## **Why Shouldn't a Root DNS Server Directly Answer Queries?**

Root DNS servers **delegate** queries to authoritative DNS servers instead of
answering them directly. Here's why:

---

### **1. Scalability & Performance**

- Root DNS servers handle **billions of queries** daily.
- If they answered every query, **they would be overwhelmed**.
- Delegation distributes the load to **lower-level authoritative DNS servers**.

---

### **2. Hierarchical Design (Faster Resolution)**

- DNS is designed in a **hierarchical structure**:
  1. **Root DNS servers** → `.com` TLD servers
  2. **TLD (Top-Level Domain) servers** → **Facebook’s authoritative name
     server**
  3. **Authoritative name servers** → Return the actual IP address.
- This allows caching and **faster lookups**.

---

### **3. Cache Efficiency**

- Recursive resolvers **cache responses** from authoritative servers.
- If root servers provided answers directly, caching wouldn't be as effective.
- More cache usage = **less global traffic to root servers**.

---

### **4. Security & Stability**

- **Root servers** should **only provide critical DNS functions**.
- If they were responsible for all domain lookups, a **DDoS attack** on them
  could bring down large portions of the internet.

---

### **5. Delegation for Decentralization**

- DNS is **designed to be decentralized**.
- If root servers answered all queries, they would become **single points of
  failure**.

---

### **How It Works Instead:**

1. Client asks a **recursive resolver** (ISP's DNS server).
2. Resolver queries a **root DNS server** → Root **delegates** to `.com` TLD
   server.
3. TLD server delegates to **authoritative DNS** (e.g., Facebook’s nameserver).
4. The authoritative server **returns the IP address**.
5. Resolver **caches the response** for future use.

---

### **Example of Root Delegation (Using `dig`)**

```sh
dig www.facebook.com +trace
```

✅ Shows root servers **delegating** the request to `.com` TLD, then to
Facebook’s authoritative DNS.

## Question: Large-Scale Network Health Check

You are given a **massive log file (`hosts_ports.txt`)** containing **hostnames
(or IPs) and ports** that need to be checked for availability. Your task is to:

1. **Read from STDIN or a file (assume a 1TB+ file for real-world scenario).**
2. **Efficiently process large inputs** using **streaming (reading line by
   line)**.
3. **Attempt to connect** to each `<HOST>:<PORT>` and determine if it's
   **reachable**.
4. **Print the status** in the format:
   ```txt
   <HOST>:<PORT> - REACHABLE
   <HOST>:<PORT> - UNREACHABLE
   ```
5. **Optimize memory usage** so that even a huge file **doesn’t crash the
   system**.

---

### **Example Content of `hosts_ports.txt`**

```txt
192.168.1.1,22
example.com,443
10.0.0.1,80
google.com,8080
localhost,3306
```

---

### **Expected Output (Example)**

```txt
192.168.1.1:22 - REACHABLE
example.com:443 - REACHABLE
10.0.0.1:80 - UNREACHABLE
google.com:8080 - UNREACHABLE
localhost:3306 - REACHABLE
```

```python
import socket

def check_host_port(host, port, timeout=2):
    """Attempts to connect to the given host and port, returns reachability status."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return "REACHABLE"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "UNREACHABLE"

# Process the file line by line (handles large files efficiently)
with open("hosts_ports.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        try:
            host, port = line.split(",")
            status = check_host_port(host, port)
            print(f"{host}:{port} - {status}")
        except ValueError:
            print(f"Invalid entry: {line}")  # Handles malformed lines

```

## Write a script that connects to 100 hosts, looks for a particular process and sends an email with a report.

```python
import paramiko
import smtplib
from email.mime.text import MIMEText

# --------------------- #
# Configuration Section #
# --------------------- #

HOSTS = ["192.168.1.1", "192.168.1.2", "server1.example.com"]  # Add 100 hosts
USERNAME = "your_user"
PASSWORD = "your_password"  # Use SSH key authentication for security
PROCESS_NAME = "nginx"
EMAIL_TO = "admin@example.com"
EMAIL_FROM = "monitor@example.com"
SMTP_SERVER = "smtp.example.com"

# --------------------- #
# Check Process on Hosts #
# --------------------- #

def check_process(host):
    """SSH into host and check if the process is running."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USERNAME, password=PASSWORD, timeout=5)

        # Run command to check if process is running
        stdin, stdout, stderr = client.exec_command(f"pgrep -x {PROCESS_NAME}")
        output = stdout.read().decode().strip()

        client.close()
        return "RUNNING" if output else "NOT RUNNING"

    except Exception as e:
        return f"ERROR: {str(e)}"

# --------------------- #
# Generate Report       #
# --------------------- #

report = []
for host in HOSTS:
    status = check_process(host)
    report.append(f"{host}: {status}")

# --------------------- #
# Send Email            #
# --------------------- #

def send_email(report):
    """Send an email with the process check report."""
    msg = MIMEText("\n".join(report))
    msg["Subject"] = f"Process Check Report: {PROCESS_NAME}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER) as server:
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

send_email(report)

print("Process check completed. Report sent via email.")

```
