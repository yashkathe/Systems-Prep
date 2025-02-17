# Operating System (OS) Troubleshooting Scenarios

## High CPU Usage on a Production Server

1. **How would you check which process is consuming the most CPU?**  
   → Use `top` or `htop` to list processes sorted by CPU usage.

2. **What’s the difference between system CPU usage and user CPU usage?**  
   → **User CPU** is time spent running user processes, while **system CPU** is
   time spent on kernel tasks.

3. **If a single process is using 100% CPU, what are the possible reasons?**  
   → It could be an **infinite loop, high computation task, or process stuck in
   a kernel call**.

4. **How can you limit the CPU usage of a process without killing it?**  
   → Use `cpulimit` or **adjust process priority** with `nice` or `renice`.

5. **What are “nice” and “renice” values in Linux, and how do they affect
   process scheduling?**  
   → Lower values (e.g., -20) make processes **higher priority**, while higher
   values (+19) make them **lower priority**.

```bash
top      # Shows system resource usage (CPU, memory, load average)
htop     # Interactive version of top with better visualization
ps aux --sort=-%cpu  # Lists processes sorted by CPU usage
taskset -c 0,1 <pid>  # Restrict a process to specific CPU cores
renice -n 10 -p <pid>  # Lower priority of a CPU-intensive process
```

## Out of Memory (OOM) Killing Critical Services

1. **How do you check if the system is running out of memory?**  
   → Use `free -m` or `vmstat` to see memory and swap usage.

2. **Where would you check logs to see if the OOM killer is terminating
   processes?**  
   → Use `dmesg | grep -i "oom"` or `journalctl -k`.

3. **What’s the difference between swap memory and physical memory, and how does
   it affect performance?**  
   → **Physical memory (RAM)** is faster, while **swap (disk-based memory)** is
   slower and used when RAM is full.

4. **What strategies can prevent the OOM killer from terminating an essential
   process?**  
   → **Increase swap, set memory limits (`ulimit`), or adjust OOM score
   (`oom_score_adj`).**

5. **How do you find which process is consuming the most memory?**  
   → Use `ps aux --sort=-%mem` or `top`.

```bash
free -m      # Shows memory usage in MB (total, used, free, swap)
vmstat -s    # Shows detailed memory statistics
dmesg | grep -i "oom"   # Check if the OOM killer is terminating processes
cat /proc/meminfo  # Detailed system memory stats
ps aux --sort=-%mem  # List processes sorted by memory usage
```

## A Process is Stuck and Unresponsive

1. **How do you check if the process is in an uninterruptible sleep state (D
   state)?**  
   → Use `ps aux | grep <pid>` and look for **D (disk wait) state**.

2. **How do you differentiate between a hung process and a zombie process?**  
   → **Hung process** is stuck in execution, while a **zombie** is **defunct**
   but still in the process table.

3. **What could cause a process to become unresponsive while still consuming
   CPU?**  
   → **Deadlocks, high I/O wait, or infinite loops.**

4. **How would you forcefully terminate a process if it doesn’t respond to
   SIGTERM?**  
   → Use `kill -9 <pid>` or `pkill -9 <process-name>`.

5. **How do you debug an unresponsive process without restarting the system?**  
   → Use `strace -p <pid>` to trace system calls or `lsof -p <pid>` to check
   open files.

```bash
ps aux | grep <process-name>  # Find process details
strace -p <pid>  # Trace system calls made by the process
lsof -p <pid>  # List open files used by the process
kill -9 <pid>  # Forcefully terminate a process
echo w > /proc/sysrq-trigger  # Dump process state for debugging
```

## Disk I/O is Causing Slow Performance

1. **How do you check if disk I/O is causing performance issues?**  
   → Use `iostat -x 1` or `vmstat 1`.

2. **What’s the difference between iowait and user/system CPU time in `top`?**  
   → **iowait** is time CPU waits for I/O, while **user/system CPU** shows
   computation load.

3. **How can you identify which process is performing the most disk I/O?**  
   → Use `iotop` or `pidstat -d`.

4. **How can you reduce I/O wait time and improve performance?**  
   → Use **faster disks (SSD), caching, or optimize file reads/writes**.

5. **How do you monitor disk read/write activity in real-time?**  
   → Use `iostat`, `iotop`, or `df -h` for space usage.

```bash
iostat -x 1  # Shows disk usage statistics
iotop        # Shows real-time disk I/O usage per process
df -h        # Check available disk space
du -sh /var/log/*  # Check which files are using the most disk space
sync; echo 3 > /proc/sys/vm/drop_caches  # Free up cached memory
```

## System Boot is Taking Too Long

1. **How do you check which services are slowing down the boot process?**  
   → Use `systemd-analyze blame`.

2. **What’s the difference between `systemd` and `init` in Linux?**  
   → `systemd` is **faster, parallelized, and modern**, while `init` is
   **sequential and older**.

3. **How can you disable unnecessary services to speed up boot time?**  
   → Use `systemctl disable <service>` to prevent startup.

4. **How do you check system logs for boot-related errors?**  
   → Use `journalctl -b -p err` or `dmesg | grep -i "error"`.

5. **How can you measure and optimize the time taken for different boot
   stages?**  
   → Use `systemd-analyze` to see breakdown of **kernel, initrd, and user-space
   startup**.

```bash
systemd-analyze blame  # Show which services took the most time to start
systemctl list-units --failed  # List failed services
journalctl -b -p err  # Show boot-time errors
dmesg | grep -i "error"  # Look for kernel errors during boot
```

## Kernel Panic on a Production Server

1. **What are common causes of a kernel panic?**  
   → **Corrupt kernel, faulty drivers, hardware failure, or memory errors.**

2. **How can you check logs for the reason behind the last kernel panic?**  
   → Use `journalctl -k -b -1` or `dmesg | tail -50`.

3. **What’s the difference between a kernel panic and a normal system crash?**  
   → **Kernel panic means the OS halts completely** due to a fatal error, unlike
   an **application crash**.

4. **How do you configure the system to automatically reboot after a kernel
   panic?**  
   → Set `sysctl -w kernel.panic=10` to reboot after 10 seconds.

5. **How do you prevent future kernel panics in a production environment?**  
   → **Use stable kernel versions, test new drivers, monitor logs, and keep
   hardware updated.**

```bash
journalctl -k -b -1  # View logs from the last boot (before the crash)
dmesg | tail -50  # Check kernel messages leading up to the crash
cat /proc/sys/kernel/panic  # Check if auto-reboot is enabled
sysctl -w kernel.panic=10  # Set the system to reboot 10 seconds after a kernel panic
```

## Process Scheduling Issues on a Server

1. **How do you check which processes are consuming the most CPU and their
   scheduling priority?**  
   → Use `top` or `ps -eo pid,ppid,cmd,%cpu,%mem,pri,ni --sort=-%cpu`.

2. **What is the difference between preemptive and non-preemptive
   scheduling?**  
   → **Preemptive scheduling** allows the OS to interrupt a process, while
   **non-preemptive** scheduling lets the process run until it voluntarily
   yields CPU.

3. **How do you manually change the priority of a running process?**  
   → Use `nice -n <priority> <command>` to start a process with a priority or
   `renice -n <new-priority> -p <pid>` for a running process.

4. **What is a real-time scheduling policy, and when would you use it?**  
   → **Real-time scheduling (SCHED_FIFO, SCHED_RR)** is used for **low-latency
   tasks like audio/video processing** or critical system tasks.

5. **What command allows you to bind a process to specific CPU cores?**  
   → Use `taskset -c <core-list> <pid>` to restrict execution to selected CPU
   cores.

```bash
top  # View process scheduling priorities in real-time
ps -eo pid,ppid,cmd,%cpu,%mem,pri,ni --sort=-%cpu  # View process priority
nice -n 10 ./script.sh  # Start a process with lower priority
renice -n -5 -p 1234  # Increase priority of an existing process
taskset -c 0,1 1234  # Bind process 1234 to CPU cores 0 and 1
chrt -r -p 99 1234  # Set real-time priority for a process
```

## Memory Leak in a Long-Running Application

1. **How do you check if a system is running low on available memory?**  
   → Use `free -m`, `vmstat -s`, or `cat /proc/meminfo` to check memory stats.

2. **What is a memory leak, and how can you identify it?**  
   → **A memory leak happens when a process allocates memory but never releases
   it**, causing RAM usage to grow continuously. Identify it using `pmap <pid>`
   or `valgrind`.

3. **How do you determine which process is consuming the most memory?**  
   → Use `ps aux --sort=-%mem` or `smem -t` to see per-process memory usage.

4. **How does the Linux kernel reclaim memory from idle processes?**  
   → **Through swapping, page caching, and OOM killer** if memory is exhausted.

5. **How can you clear cached memory without rebooting the system?**  
   → Run `sync; echo 3 > /proc/sys/vm/drop_caches` to free page cache, dentries,
   and inodes.

```bash
free -m  # Check available and used memory in MB
vmstat -s  # Detailed memory statistics
ps aux --sort=-%mem  # List processes consuming the most memory
pmap <pid>  # View memory map of a process
echo 3 > /proc/sys/vm/drop_caches  # Clear system cache
valgrind --leak-check=full ./program  # Debug memory leaks in an application
```

## High Swap Usage Slowing Down the System

1. **How do you check if a system is using swap excessively?**  
   → Use `swapon -s` or `free -m` to check swap usage.

2. **Why is excessive swapping bad for performance?**  
   → **Swap is much slower than RAM**, so high swap usage leads to **disk
   thrashing and slow performance**.

3. **How can you identify which process is using the most swap space?**  
   → Use `grep VmSwap /proc/*/status | sort -nk2 | tail -10`.

4. **What is swappiness, and how can you adjust it to reduce swap usage?**  
   → **Swappiness (0-100) controls how aggressively Linux uses swap; lower
   values prioritize RAM.** Modify it with `sysctl -w vm.swappiness=10`.

5. **How can you increase available swap space on a running system?**  
   → Create a swap file using `dd`, format it with `mkswap`, and activate it
   with `swapon`.

```bash
free -m  # Check swap usage
swapon -s  # List active swap partitions/files
grep VmSwap /proc/*/status | sort -nk2 | tail -10  # Find processes using the most swap
sysctl -w vm.swappiness=10  # Reduce swappiness to prioritize RAM usage
dd if=/dev/zero of=/swapfile bs=1G count=4  # Create a 4GB swap file
mkswap /swapfile  # Format the swap file
swapon /swapfile  # Enable new swap space
```

## File System Running Out of Space

1. **How do you check available disk space on a Linux system?**  
   → Use `df -h` to see disk usage in a human-readable format.

2. **How can you find which folders are consuming the most disk space?**  
   → Use `du -sh /*` or `du -sh /var/log/*`.

3. **How do you check for large, hidden files that are still taking up space
   after deletion?**  
   → Use `lsof | grep deleted` to find files held open by running processes.

4. **How can you clear up space on a log-heavy system?**  
   → Use `logrotate` to compress and manage logs or manually clean `/var/log`.

5. **What is an inode, and how can running out of inodes cause disk-related
   issues?**  
   → **Inodes store file metadata; if all inodes are used, new files can’t be
   created even if space is available.** Check with `df -i`.

```bash
df -h  # Check disk space usage
du -sh /*  # Find which directories use the most space
lsof | grep deleted  # Find deleted files still consuming space
rm -rf /var/log/*.log  # Clear old log files
df -i  # Check inode usage
logrotate -f /etc/logrotate.conf  # Force log rotation
```

## File System Corruption Detected

1. **How do you check if a file system is corrupted?**  
   → Use `dmesg | grep EXT4-fs` or `fsck -n /dev/sdX`.

2. **What are common causes of file system corruption?**  
   → **Unclean shutdowns, disk failures, or software bugs** in the file system.

3. **How can you repair a corrupted file system?**  
   → Run `fsck -y /dev/sdX` (needs unmounted disk or recovery mode).

4. **How do you prevent future file system corruption?**  
   → Use `ext4` journaling, ensure `sync` before shutdown, and check SMART data.

5. **How do you monitor disk health to detect possible failures?**  
   → Use `smartctl -a /dev/sdX` to check disk SMART attributes.

```bash
dmesg | grep EXT4-fs  # Check for file system errors
fsck -n /dev/sdX  # Run a dry-check on the file system
fsck -y /dev/sdX  # Fix file system errors automatically
smartctl -a /dev/sdX  # Check SMART disk health status
```

## Sudden System Hang or Slowdown Due to High Load

1. **How do you check the current system load and active processes?**  
   → Use `uptime`, `top`, or `vmstat 1`.

2. **What is the difference between load average and CPU usage?**  
   → **Load average includes both running and waiting processes**, while CPU
   usage is only active execution.

3. **How can you identify which process is causing high load?**  
   → Use `top -o %CPU` or `ps aux --sort=-%cpu`.

4. **How can you reduce system load without rebooting?**  
   → **Kill or renice high CPU processes, limit I/O with ionice, or restart
   heavy services.**

5. **How do you check if a process is causing a kernel lockup?**  
   → Use `dmesg | tail` and `cat /proc/locks`.

```bash
uptime  # Check system load average
top -o %CPU  # Show processes sorted by CPU usage
ps aux --sort=-%cpu  # Find highest CPU consumers
dmesg | tail  # Check kernel messages for system hangs
```

## Web Server is Not Responding

1. **How do you check if the web server process (e.g., Nginx, Apache) is
   running?**  
   → Use `systemctl status nginx` or `ps aux | grep nginx`.

2. **How do you verify if the server is listening on port 80 or 443?**  
   → Use `netstat -tulnp | grep :80` or `ss -tulnp | grep :443`.

3. **How do you test if the web server is responding locally?**  
   → Use `curl -I localhost` to check the HTTP response headers.

4. **How can you check web server logs for errors?**  
   → Use `tail -f /var/log/nginx/error.log` or
   `journalctl -u nginx --since "10 min ago"`.

5. **How do you restart a web server if it's unresponsive?**  
   → Use `systemctl restart nginx` or `service apache2 restart`.

```bash
systemctl status nginx  # Check if the web server is running
netstat -tulnp | grep :80  # Verify if the server is listening on port 80
curl -I localhost  # Test if the server responds locally
tail -f /var/log/nginx/error.log  # Check web server logs
systemctl restart nginx  # Restart the web server
```

---

## Website is Loading Slowly

1. **How do you check if the server is running low on CPU or memory?**  
   → Use `top` or `htop` to monitor resource usage.

2. **How can you check if the network connection to the server is slow?**  
   → Use `ping <server-ip>` and `mtr <server-ip>` to trace network latency.

3. **How do you find slow database queries that might be affecting the
   website?**  
   → Use `mysql -e "SHOW PROCESSLIST;"` or `pg_stat_activity` for PostgreSQL.

4. **How can you check if there is high disk I/O affecting performance?**  
   → Use `iostat -x 1` or `iotop` to monitor disk activity.

5. **How do you check for overloaded PHP, Python, or application workers?**  
   → Use `ps aux | grep php-fpm` or `systemctl status gunicorn`.

```bash
top  # Monitor CPU and memory usage
ping <server-ip>  # Check network latency
mysql -e "SHOW PROCESSLIST;"  # Identify slow database queries
iostat -x 1  # Monitor disk I/O performance
ps aux | grep php-fpm  # Check if PHP workers are overloaded
```

---

## SSH Connection to the Server is Failing

1. **How do you check if the SSH service is running?**  
   → Use `systemctl status ssh` or `ps aux | grep sshd`.

2. **How do you verify if the SSH port (default 22) is open?**  
   → Use `netstat -tulnp | grep :22` or `ss -tulnp | grep :22`.

3. **How can you test SSH connectivity from another machine?**  
   → Use `ssh -v user@server-ip` for verbose SSH output.

4. **How do you check if a firewall is blocking SSH access?**  
   → Use `iptables -L | grep 22` or `ufw status`.

5. **How can you restart SSH without rebooting the server?**  
   → Use `systemctl restart ssh`.

```bash
systemctl status ssh  # Check if SSH service is running
netstat -tulnp | grep :22  # Verify SSH is listening on port 22
ssh -v user@server-ip  # Test SSH connection with verbose mode
iptables -L | grep 22  # Check firewall rules for SSH
systemctl restart ssh  # Restart SSH service
```

---

## Server Disk is Full

1. **How do you check available disk space?**  
   → Use `df -h` to see disk usage in human-readable format.

2. **How do you find which directories are consuming the most space?**  
   → Use `du -sh /*` or `du -sh /var/*`.

3. **How can you locate and delete large log files?**  
   → Use `find /var/log -type f -size +100M -exec ls -lh {} \;`.

4. **How do you check for deleted files still using disk space?**  
   → Use `lsof | grep deleted`.

5. **How can you clean up old logs automatically?**  
   → Use `logrotate` to manage log retention.

```bash
df -h  # Check available disk space
du -sh /*  # Find large directories consuming space
find /var/log -type f -size +100M -exec ls -lh {} \;  # Find large log files
lsof | grep deleted  # Find deleted files still using space
logrotate -f /etc/logrotate.conf  # Rotate and manage log files
```

## Server Load is High and Unresponsive

1. **How do you check current system load and running processes?**  
   → Use `uptime` and `top` or `htop`.

2. **How do you identify the process consuming the most CPU?**  
   → Use `ps aux --sort=-%cpu | head -5`.

3. **How do you check if high I/O is causing the issue?**  
   → Use `iotop` or `iostat -x 1`.

4. **How do you kill a process that is overloading the system?**  
   → Use `kill -9 <pid>` or `pkill <process-name>`.

5. **How can you reduce load without rebooting?**  
   → Use `renice -n 10 -p <pid>` to lower priority or `systemctl stop <service>`
   for unneeded services.

```bash
uptime  # Check system load
ps aux --sort=-%cpu | head -5  # Find top CPU-consuming processes
iotop  # Monitor real-time disk I/O
kill -9 <pid>  # Kill a misbehaving process
renice -n 10 -p <pid>  # Lower priority of a high-CPU process
```
