#!/usr/bin/env bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ansible bind9-dnsutils openssh-client sshpass python3 python3-yaml git curl
