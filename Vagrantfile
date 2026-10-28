Vagrant.configure("2") do |config|
  config.vm.box = ENV.fetch("VAGRANT_BOX", "bento/ubuntu-24.04")
  config.vm.boot_timeout = 600

  bridge_adapter = ENV["VAGRANT_BRIDGE_ADAPTER"]

  config.vm.define "infra01" do |vm|
    vm.vm.hostname = "infra01"
    vm.vm.network "public_network", bridge: bridge_adapter if bridge_adapter && !bridge_adapter.empty?
    vm.vm.network "private_network", ip: "192.168.56.2"
    vm.vm.provider "virtualbox" do |vb|
      vb.name = "infra01"
      vb.memory = 1536
      vb.cpus = 2
      vb.gui = false
    end
    vm.vm.provision "shell", path: "scripts/install_ansible.sh", privileged: true
  end

  {
    "master01" => ["k8s-cplane01", "192.168.56.4", 2560, 2],
    "master02" => ["k8s-cplane02", "192.168.56.5", 2048, 2],
    "worker01" => ["k8s-worker01", "192.168.56.6", 1536, 2],
    "worker02" => ["k8s-worker02", "192.168.56.7", 1536, 2],
    "haproxy" => ["hap01", "192.168.56.8", 768, 1],
    "nfsha" => ["nfsha", "192.168.56.9", 1024, 1]
  }.each do |vm_name, settings|
    hostname, ip, memory, cpus = settings
    config.vm.define vm_name do |vm|
      vm.vm.hostname = hostname
      vm.vm.network "private_network", ip: ip
      vm.vm.provider "virtualbox" do |vb|
        vb.name = hostname
        vb.memory = memory
        vb.cpus = cpus
        vb.gui = false
      end
    end
  end
end
