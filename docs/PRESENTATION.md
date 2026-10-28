# Présentation orale — 3 à 5 minutes

## 1. Le problème

« Préparer plusieurs machines, installer Kubernetes, configurer un répartiteur et assurer la persistance des données à la main est répétitif et difficile à reproduire. Mon objectif est de décrire l'infrastructure sous forme de code versionné. »

## 2. La solution

« Vagrant déclare sept machines Ubuntu. Ansible configure DNS, HAProxy, NFS et les nœuds Kubernetes. kubeadm assemble deux control-planes et deux workers. Enfin, un PV et un PVC NFS ainsi qu'un Pod BusyBox permettent de vérifier une écriture persistante. Un playbook séparé installe ArgoCD pour montrer la piste GitOps. »

## 3. Architecture à montrer

Présenter le fichier Vagrantfile, puis ansible-playbooks/etc/hosts.

- infra01 : 192.168.56.2
- control-planes : 192.168.56.4 et 192.168.56.5
- workers : 192.168.56.6 et 192.168.56.7
- HAProxy : 192.168.56.8:6443
- NFS : 192.168.56.9:/srv/kubernetes

## 4. Démonstration

Depuis infra01, dans /vagrant/ansible-playbooks :

```bash
ansible -i etc/hosts k8s_cplanes,k8s_workers,haproxy,dns,nfsha -m ping
ansible-playbook -i etc/hosts playbooks/verify_cluster.yml
kubectl get nodes -o wide
kubectl get pods -A
kubectl get pvc
kubectl logs test-nfsha-pod
```

Montrer la sortie réelle uniquement si le laboratoire a été démarré. Sinon, présenter les playbooks et préciser que les tests fonctionnels restent à exécuter.

## 5. Questions possibles

**Pourquoi Vagrant et Ansible ?** Vagrant gère les VM ; Ansible automatise la configuration des systèmes et des services.

**Pourquoi HAProxy ?** Il fournit un endpoint TCP stable pour l'API Kubernetes et répartit les connexions vers les control-planes.

**Quelle est la différence entre PV et PVC ?** Le PV représente le stockage disponible ; le PVC exprime la demande consommée par un Pod.

**Le cluster est-il totalement hautement disponible ?** Non. HAProxy fournit un endpoint commun, mais deux membres etcd ne garantissent pas le quorum lors de la panne de l'un d'eux.

**Qu'est-ce qui reste à prouver ?** Les nœuds Ready, l'accès via HAProxy, le PVC Bound et le fichier écrit sur le partage NFS.
