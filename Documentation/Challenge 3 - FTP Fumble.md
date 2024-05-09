Machines on network:

172\.28.1.6 - FTP server

172\.28.1.5 - Kali Linux container

Overview of Challenge:

This challenge will involve using an improperly secured FTP server to access and modify a Dockerfile that is set up to be built automatically.

**FTP (File Transfer Protocol)** is used for the transfer of files across a network. You’ll be connecting to an FTP server configured to allow anonymous access, which means you can log in as the user 'anonymous' and typically no password is required.  
  
**Docker:** A platform used to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package. Dockerfiles are used to define these containers and how they should be built. You will be editing a Dockerfile to gain unintended access to a system.

Walkthrough:

1) Accessing FTP

Once you have access to the environment you can confirm that the FTP server is running using the following command. 

nmap 172.28.1.6

nmap is a tool commonly used by cybersecurity professionals in many roles to scan devices on a network. The output should indicate that port 21 is open, which indicates that ftp is running on this server. to connect using ftp on port 21 use the following command.

ftp 172.28.1.6 21

When you are prompted for a username, type "anonymous" (without quotation marks) and for the password do not enter anything and press enter. This allows you access to the FTP server. In the real world anonymous login is incredibly insecure, but someone setting up an FTP server without adequate care can accidentally enable it.

2) Exploring the FTP server

To discover what we have access to on the ftp server, use the ls or 'list' command

ls

This should provide the following output:

\-rw-r--r--             1 0              0              60 May 08 21:40 note.txt  
\-rw-r--r--             1 0              0               29 May 08 21:41 test.txt  
drwxrwxrwx    1 101      103          4096 May 08 21:41 upload  
  
To pull the two txt files to examine them on our local machine use the following two commands:

get note.txt

get test.txt

We can then exit the FTP interface using the following command:

exit

To examine the contents of the test.txt file we can use the cat command:

cat test.txt

The output should be the following:

Hello from dummy Dockerfile!

Using the cat command again with the note.txt file:

cat note.txt

We get the following hint:

TODO: remove auto-build script for any Dockerfile in upload  
  
This hint indicates that if we place any file named "Dockerfile" in the upload folder on the FTP server it will automatically be built. Connect to the ftp server again using the same command:  
  
ftp 172.28.1.6 21

After logging in anonymously again use the cd command to enter the upload directory:

cd upload

If we use the 'ls' command again we can see the following output:

\-rw-r--r--    1 0        0             163 May 08 21:40 Dockerfile_copy  
  
Let's pull the Dockerfile_copy using the get command:

get Dockerfile_copy

And exit to examine it locally:

exit

Create a copy of the file to edit using the cp or copy command:

cp Dockerfile_copy Dockerfile

We will now use the vim editor to examine and edit this file. Vim is a very powerful text editor with many shortcuts and features. New users often have difficulty using vim but for now the following simple commands will be sufficient for this challenge:

- Press the "i" button to enter insert mode
  - This mode is the most similar to traditional text editors and will allow you to type and delete characters.
- Use arrow keys to move the cursor (mouse buttons will not work)
- Use : to enter command mode
  - :wq! will cause the current file to be saved and quit

Open the file in vim to edit using the following command:

vim Dockerfile

Using the vim commands previously given, we will edit the Docker file. The Dockerfile should initially read:

# Use a base image

FROM alpine:latest

# Define volumes

VOLUME /ftp
VOLUME /secure

# Run a simple command

CMD echo 'Hello from dummy Dockerfile!' > /ftp/test.txt
  
We will explain this Dockerfile line by line. Dockerfiles are essentially instructions on how to set up an environment.

All lines beginning with # are comments intended to clarify the purpose of the lines below them.

FROM alpine:latest

This line indicates the image that the docker container will be based on. There are many pre-built container images that are often used as starting points for other containers. There is not much reason to start from scratch when you can use another container image as a starting point.

VOLUME /ftp

VOLUME /secure 

These lines give mount points for volumes when the container is run. These volumes names give us hints that the container likely will be run with access to these two directories.

CMD echo 'Hello from dummy Dockerfile!' > /ftp/test.txt

This line tells the container to create a textfile in /ftp when the container is run. This is the source of the test note we saw earlier.

3) Accessing /secure

There are many ways that the Dockerfile can be manipulated to give us the contents of the /secure directory. Without this walkthrough, you would have to run commands like the following in the Dockerfile to explore the directory and identify any items inside:

CMD ls /secure > /ftp/ls.txt

This command would run the ls command inside of the /secure directory and put the output in a text file in /ftp where we could log in and access it. Since we already know the contents of the directory though, we simply change the CMD line to the following:

CMD cat /secure/flag.sh > /ftp/flag.sh

This will output the contents of flag.sh into a new file in ftp. Save and exit the file in vim and log in to the FTP server. Navigate to the upload folder and use the following command to upload the Dockerfile:

put Dockerfile

This will upload the Dockerfile. It may take some time for the Dockerfile to be run as the directory is checked every 60 seconds. Use the ls command to check the upload directory until the Dockerfile dissappears. Then navigate out of the upload directory using the following command:

cd ..

Now you should see the flag.sh file. Use the get command to download it and exit FTP. You can now complete the challenge by running the following command:

bash flag.sh

You should see the challenge marked as completed in the WebUI. You can now exit the challenge using the following command on the Kali container:

exit