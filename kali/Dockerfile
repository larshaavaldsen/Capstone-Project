# Use the official Kali Linux rolling image as the base
FROM kalilinux/kali-rolling

# Install nmap and gobuster
RUN apt-get update && apt-get install -y \
    nmap \
    gobuster \
    iputils-ping \
    seclists \
    && rm -rf /var/lib/apt/lists/*
