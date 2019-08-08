# -*- mode: ruby -*-
# vi: set ft=ruby :


$PYTHON_ENV = <<SCRIPT
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install python3 -y
  sudo DEBIAN_FRONTEND=noninteractive apt-get install python3-pip -y
  sudo python3 -m pip install -r /vagrant/CAS_WEB/requirements.txt --no-cache-dir
  sudo python3 -m pip install coverage
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.ssh.forward_agent = true
  config.vm.provision "shell", inline: $PYTHON_ENV

  config.vm.define :ubuntu do |host|
    host.vm.hostname = "ubuntu"
    host.vm.network "private_network", ip: "192.168.56.22", netmask: "255.255.255.0", mac: "080027a7feb1"
  end
end
