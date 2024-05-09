# Use the official Kali Linux rolling image as the base
FROM kalilinux/kali-rolling

# Install nmap and gobuster
RUN apt-get update && apt-get install -y \
    nmap \
    gobuster \
    vim \
    ftp \
    iputils-ping \
    ssh \
    && rm -rf /var/lib/apt/lists/*

COPY ./2020-200_most_used_passwords.txt ./
COPY ./top-usernames-shortlist.txt ./