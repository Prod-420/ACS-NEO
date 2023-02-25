#!/bin/bash

# Stop all running containers
sudo docker stop $(sudo docker ps -a -q)

# Stop all Docker containers
docker-compose down

# Remove all containers
sudo docker rm $(sudo docker ps -a -q)

# Remove all images
sudo docker rmi -f $(sudo docker images -a -q)

# Uninstall Docker and Docker Compose
sudo apt-get purge docker-ce docker-ce-cli containerd.io
sudo apt-get autoremove -y --purge docker-ce docker-ce-cli containerd.io

# Remove Docker and Docker Compose configuration files
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker
sudo rm -rf /etc/containerd
sudo rm -rf /var/run/docker.sock

# Uninstall Docker Compose
sudo rm /usr/local/bin/docker-compose

echo "Docker and Docker Compose have been completely removed from your system."
#How to unistall:
# download unistall-docker.sh
# move file to directories where your *.yml file or Docker file
# open Terminal and run command "unistall-docker.sh"
# run command "unistall-docker.sh"
# reboot
# If you have any questions, feel free to ask ChatGPT.
