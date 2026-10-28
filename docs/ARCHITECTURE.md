# Architecture

## Composants

- **infra01 — 192.168.56.2** : machine d'administration Ansible et serveur DNS BIND9.
- **k8s-cplane01 — 192.168.56.4** : premier control-plane, initialisé avec kubeadm.
- **k8s-cplane02 — 192.168.56.5** : second control-plane, joint au cluster.
- **k8s-worker01 / worker02 — 192.168.56.6 / .7** : exécution des applications Kubernetes.
- **hap01 — 192.168.56.8:6443** : endpoint TCP partagé de l'API Kubernetes.
- **nfsha — 192.168.56.9** : serveur NFS, export /srv/kubernetes.

## Flux applicatifs et infra

Client kubectl → HAProxy:6443 → API Server d'un control-plane.

Pod de test → PVC → PV statique → NFS (nfsha:/srv/kubernetes/test-volume).

Vagrant décrit et crée les VM. Ansible configure les OS, les services d'infrastructure, containerd, kubeadm et les applications du cluster. ArgoCD est installé par un playbook optionnel.

## Limite de haute disponibilité

HAProxy peut retirer un backend indisponible, mais l'état du control-plane dépend aussi du quorum etcd. Deux membres etcd ne tolèrent pas la perte d'un membre. C'est un laboratoire pédagogique et non une architecture de production.
