#!/usr/bin/env bash
set -euo pipefail

# Lance ce script depuis infra01 avec le compte vagrant.
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
if [[ ! -f "$HOME/.ssh/id_ed25519" ]]; then
  ssh-keygen -t ed25519 -N "" -f "$HOME/.ssh/id_ed25519" -C "infra01-k8s-lab"
fi

for host in 192.168.56.4 192.168.56.5 192.168.56.6 192.168.56.7 192.168.56.8 192.168.56.9; do
  echo "Installation de la clé SSH sur $host"
  ssh-copy-id -o StrictHostKeyChecking=accept-new "vagrant@$host"
done

ssh-keyscan -H 192.168.56.2 192.168.56.4 192.168.56.5 192.168.56.6 192.168.56.7 192.168.56.8 192.168.56.9 >> "$HOME/.ssh/known_hosts" 2>/dev/null || true
echo "Bootstrap SSH terminé."
