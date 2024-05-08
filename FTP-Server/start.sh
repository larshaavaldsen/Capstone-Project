#!/bin/bash
# Redirect all outputs to a log file and stdout

# Setup log file
LOG_FILE="/var/log/startup.log"
touch $LOG_FILE
exec &> >(tee -a "$LOG_FILE")

echo "Starting the script..."

# Start Docker daemon in the background and log output
echo "Starting Docker daemon..."
dockerd > /var/log/dockerd.log 2>&1 &
status=$?
if [ $status -eq 0 ]; then
    echo "Docker daemon started successfully."
else
    echo "Failed to start Docker daemon. Status: $status"
fi

# Sleep a bit to ensure Docker daemon starts properly
echo "Waiting for Docker daemon to initialize..."
sleep 5

# Start vsftpd in the foreground and log output
echo "Starting vsftpd..."
vsftpd
status=$?
if [ $status -eq 0 ]; then
    echo "vsftpd started successfully."
else
    echo "Failed to start vsftpd. Status: $status"
fi
