# Installs required dependencies
apt-get update
apt-get install -y git tmux python3-pip

git clone git://github.com/mininet/mininet
mininet/util/install.sh

pip3 install -r requirements.txt
