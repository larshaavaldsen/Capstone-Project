## Machines on network:

172\.28.1.7 - **PHP Web Server**

172\.28.1.8 - **MySQL Database**

172\.28.1.9 - **PHPMyAdmin Server**

172\.28.1.5 - **Kali Linux container**

## Overview of Challenge:
This challenge guides the user through executing a simple SQL payload via web page input in order to gain access to an administrator account for a PHP web server.

**PHP** is a general purpose scripting language primarily suited to web development. It will serve as the frontend for the login page available after running the challenge.

**MySQL** is an open-source relational database management system (RDBMS) based on the Structured Query Language which is used to manage data. The service is used to store the logins for the web server.

Walkthrough:

## 1) Scanning the web server

After selecting the SQL Smash challenge from the GUI, we will be presented with a Kali Linux terminal. We can scan the web server to make sure it is up and running with the following command:

```nmap 172.28.1.7```

This command will output the following:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-10 00:00 UTC
Nmap scan report for challengecomposefiles-www-1.webnet (172.28.1.7)
Host is up (0.0000050s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 02:42:AC:1C:01:07 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.15 seconds
```

The output indicates that there is a http service running on port 80 and is functioning appropriately.

## 2) Accessing the web server

Now that we know that the web server is up and running, we can navigate to the site using your preferred web browser.

```http://172.28.1.7:80```

## 3) Injecting the payload

Once the site is loaded on our web browser, all that's left to do is inject the SQL payload into the username text field. All we need to know is a valid username to successfully bypass the password field.

```admin``` is a very common username for many applications and a valid username we can use for this dummy website.

Let's try a quick test to make sure this website is vulnerable to SQL injection. In the username field, type in ```admin'``` (make sure the single quote is included) and type in any password.

If done correctly, we should notice a fatal error resulting from invalid SQL syntax. This is good (for the hacker) and means that the website is vulnerable to SQL injection and we can proceed with the following payload for the username:

```admin' OR '1'='1```

The reason why this works and we can use a random password to grant a successful login is because SQL processes operators such that the AND operator takes precendence over the OR operator. When we include '1'='1' in the username, it is to always have a condition that will always evaluate to true.

Upon receiving the "Login Successful" page, we have completed the challenge. Good job!