# Use the official Kali Linux rolling image as the base
FROM kalilinux/kali-rolling

# Install nmap and gobuster
RUN apt-get update && apt-get install -y \
    nmap \
    hydra \
    vim \
    ftp \
    iputils-ping \
    ssh \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY ./2020-200_most_used_passwords.txt ./
COPY ./top-usernames-shortlist.txt ./