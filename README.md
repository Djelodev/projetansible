# Projet Ansible — Infrastructure Kubernetes multi-nœuds

Laboratoire pédagogique **Infrastructure as Code** combinant Vagrant, VirtualBox, Ansible, kubeadm, HAProxy, NFS, Ingress et ArgoCD.

## Architecture

| VM | Adresse Host-Only | Fonction |
|---|---:|---|
| infra01 | 192.168.56.2 | Administration Ansible et DNS BIND9 |
| k8s-cplane01 | 192.168.56.4 | Initialisation du cluster Kubernetes |
| k8s-cplane02 | 192.168.56.5 | Second control-plane |
| k8s-worker01 | 192.168.56.6 | Worker Kubernetes |
| k8s-worker02 | 192.168.56.7 | Worker Kubernetes |
| hap01 | 192.168.56.8 | Endpoint de l'API Kubernetes sur TCP/6443 |
| nfsha | 192.168.56.9 | Stockage NFS sous /srv/kubernetes |

## Démarrage

Prérequis : VirtualBox, Vagrant, Git et environ 10,75 Gio de RAM disponible pour les VM.

À la racine du dépôt :

```bash
vagrant validate
vagrant up
vagrant ssh infra01 -c "bash /vagrant/scripts/bootstrap-ssh.sh"
vagrant ssh infra01
```

Dans la session infra01 :

```bash
cd /vagrant/ansible-playbooks
ansible-galaxy collection install -r requirements.yml
ansible-inventory -i etc/hosts --graph
ansible -i etc/hosts k8s_cplanes,k8s_workers,haproxy,dns,nfsha -m ping
ansible-playbook -i etc/hosts playbooks/site.yml
```

Le playbook principal configure BIND9, prépare containerd et Kubernetes, configure HAProxy et NFS, initialise les quatre nœuds, puis déploie un test de stockage persistant.

## Application HTTP avec Ingress

Après la réussite du playbook principal, déployer le contrôleur Ingress et l'application web de démonstration :

```bash
ansible-playbook -i etc/hosts playbooks/install_ingress_nginx.yml
kubectl get pods -n nginx-ingress
kubectl get svc -n nginx-ingress
kubectl get ingress -n demo-app
```

Récupérer le NodePort HTTP affiché par le Service du contrôleur, puis tester depuis une machine qui accède au réseau Host-Only, en remplaçant `<NODEPORT_HTTP>` par la valeur relevée :

```bash
curl -H "Host: demo.esgi.net" http://192.168.56.6:<NODEPORT_HTTP>/
```

Cette ressource illustre le flux Client → Ingress → Service → Deployment/Pods.

## Vérifier le stockage

```bash
ansible-playbook -i etc/hosts playbooks/verify_cluster.yml
kubectl get nodes -o wide
kubectl get pods -A
kubectl get storageclass,pv,pvc
kubectl logs test-nfsha-pod
```

Le Pod BusyBox écrit un fichier dans son PVC, dont le PV est hébergé sur le serveur NFS. Vérifier aussi, sur nfsha, la présence de `/srv/kubernetes/test-volume/test.txt`.

## ArgoCD

```bash
ansible-playbook -i etc/hosts playbooks/install_argocd.yml
kubectl get pods,svc -n argocd
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Guide de déploiement](docs/DEPLOIEMENT.md)
- [Diagnostic et limites connues](docs/DIAGNOSTIC.md)
- [Présentation orale (3–5 minutes)](docs/PRESENTATION.md)

## CI et limites connues

GitHub Actions vérifie la syntaxe YAML, Ruby et des playbooks Ansible à chaque push et pull request. Il ne démarre pas les VM et ne prouve pas la disponibilité réelle du cluster. Il faut vérifier les nœuds Ready, l'accès à l'API derrière HAProxy, le routage HTTP et la persistance NFS dans le laboratoire.

Cette version est un laboratoire pédagogique. Deux control-planes ne garantissent pas le quorum etcd si l'un des membres tombe en panne. Éviter de présenter cette topologie comme une architecture de production hautement disponible.
