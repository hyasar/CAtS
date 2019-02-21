sudo apt update

# install docker
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# build container (under the directory of docker-compose.yml)
# sudo docker-compose up

# get Jenkins password
# sudo docker ps
# sudo docker exec -it <container name> /bin/bash

