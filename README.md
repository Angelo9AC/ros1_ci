sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo service docker start

Then, you can use docker without sudo with:

sudo usermod -aG docker $USER
newgrp docker