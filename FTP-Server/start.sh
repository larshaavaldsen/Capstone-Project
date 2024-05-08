#!/bin/bash
echo "Script started"

# Start Docker daemon in the background
echo "Starting Docker daemon..."
dockerd > /var/log/dockerd.log 2>&1 &
sleep 10  # Increase sleep if Docker takes longer to initialize
echo "Docker daemon should be up."

# Start vsftpd in the background
echo "Starting vsftpd..."
vsftpd &

# Create a dummy Dockerfile in /ftp/upload
echo "Creating a dummy Dockerfile..."
cat > /ftp/upload/Dockerfile <<EOF
# Use a base image
FROM alpine:latest

# Define volumes
VOLUME /ftp
VOLUME /secure

# Run a simple command
CMD echo 'Hello from dummy Dockerfile!' > /ftp/test.txt
EOF

# Create a note.txt file in /ftp
echo "Creating note in /ftp..."
echo "TODO: remove auto-rebuild script for Dockerfile in upload" > /ftp/note.txt

# Function to build Docker image and run with volumes mounted
build_and_run_image() {
    echo "Building Docker image from Dockerfile..."
    docker build -t dummy-image /ftp/upload
    echo "Running container from built image with volumes..."
    docker run -d --rm \
        -v /ftp:/ftp \
        -v /secure:/secure \
        dummy-image
}

# Run build_and_run_image function every 60 seconds
while true; do
    build_and_run_image
    sleep 60
done

