# Projet Kubernetes — Vagrant, Ansible, HAProxy et NFS

Ce dépôt accueille un laboratoire pédagogique d'Infrastructure as Code : 7 VM Ubuntu, un cluster Kubernetes kubeadm multi-nœuds, un endpoint API HAProxy, du stockage NFS persistant et un déploiement ArgoCD.

## Architecture

| Machine | IP | Rôle |
|---|---|---|
| infra01 | 192.168.56.2 | Administration Ansible et DNS |
| k8s-cplane01 | 192.168.56.4 | Control plane initial |
| k8s-cplane02 | 192.168.56.5 | Second control plane |
| k8s-worker01 | 192.168.56.6 | Worker Kubernetes |
| k8s-worker02 | 192.168.56.7 | Worker Kubernetes |
| hap01 | 192.168.56.8 | Équilibrage TCP de l'API sur 6443 |
| nfsha | 192.168.56.9 | Stockage partagé NFS |

## Contenu

- `Vagrantfile` : création des sept machines VirtualBox.
- `scripts/` : installation Ansible, initialisation SSH et validation statique.
- `ansible-playbooks/` : inventaire, dépendances, rôles et playbooks.
- `ansible-playbooks/manifests/` : ressources de test de stockage NFS.
- `docs/` : architecture, déploiement, diagnostic et présentation orale.
- `.github/workflows/validate.yml` : validation statique à chaque push/pull request.

## Prérequis

Installer VirtualBox, Vagrant et Git. La configuration réserve environ 10,75 Gio de RAM aux sept VM. Prévoir davantage de mémoire physique pour l'hôte et les applications en cours.

## Démarrage rapide

```bash
vagrant validate
vagrant up
vagrant ssh infra01 -c "bash /vagrant/scripts/bootstrap-ssh.sh"
vagrant ssh infra01
cd /vagrant/ansible-playbooks
ansible-galaxy collection install -r requirements.yml
ansible-inventory -i etc/hosts --graph
ansible -i etc/hosts k8s_cplanes,k8s_workers,haproxy,dns,nfsha -m ping
```

Voir [`docs/DEPLOIEMENT.md`](docs/DEPLOIEMENT.md) pour le déroulé complet. Pour les vérifications, consultez [`docs/DIAGNOSTIC.md`](docs/DIAGNOSTIC.md).

## Démonstration NFS

Après le déploiement du cluster et la configuration du serveur NFS :

```bash
cd /vagrant/ansible-playbooks
ansible-playbook -i etc/hosts playbooks/apply_nfs_storageclass.yml
ansible-playbook -i etc/hosts playbooks/manage_nfsha_volumes.yml --ask-become-pass -e "pvname=test-nfsha pvsize=1G"
ansible-playbook -i etc/hosts playbooks/deploy_nfs_smoke_test.yml
ansible-playbook -i etc/hosts playbooks/verify_cluster.yml
```

Le test doit aboutir à un PVC `Bound`, un Pod de test fonctionnel et un fichier côté serveur NFS. Les résultats doivent être recueillis sur les VM : la présence des manifestes ne prouve pas à elle seule le succès du déploiement.

## Présentation

Ouvrir [`docs/PRESENTATION.md`](docs/PRESENTATION.md) pour le pitch de 3 à 5 minutes, la démonstration et les questions probables.

## Limites connues

Ce dépôt constitue un laboratoire pédagogique. La configuration n'a pas été exécutée dans ce contexte contre sept VM réelles. Il faut vérifier les noms des interfaces, le démarrage VirtualBox, le kubeconfig, la liaison PV/PVC, l'accès à l'API derrière HAProxy et la persistance du fichier sur NFS avant d'affirmer que les tests de bout en bout passent. Avec deux control-planes uniquement, ne pas présenter etcd comme tolérant à toutes les pannes.
