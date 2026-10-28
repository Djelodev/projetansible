# Procédure de déploiement

## 1. Préparer l'hôte

Installer VirtualBox, Vagrant et Git. Les VM réservent ensemble environ 10,75 Gio de RAM, hors mémoire consommée par l'hôte. Si une interface pont est nécessaire, renseigner `VAGRANT_BRIDGE_ADAPTER` avec son nom exact.

```bash
vagrant validate
vagrant up
```

## 2. Bootstrap SSH et accès à infra01

```bash
vagrant ssh infra01 -c "bash /vagrant/scripts/bootstrap-ssh.sh"
vagrant ssh infra01
cd /vagrant/ansible-playbooks
ansible-inventory -i etc/hosts --graph
ansible -i etc/hosts k8s_cplanes,k8s_workers,haproxy,dns,nfsha -m ping
```

Le script demande une validation interactive pour copier la clé SSH sur chaque VM. Il doit être lancé depuis infra01 avec le compte du laboratoire.

## 3. Lancer l'automatisation

```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i etc/hosts playbooks/site.yml
```

Le playbook installe BIND9, prépare containerd et les paquets Kubernetes, configure HAProxy et NFS, initialise le cluster, joint les autres nœuds et déploie un test NFS. L'exécution demande une connexion Internet et peut durer selon la vitesse de téléchargement.

## 4. Contrôler les résultats

```bash
ansible-playbook -i etc/hosts playbooks/verify_cluster.yml
kubectl get nodes -o wide
kubectl get pods -A
kubectl get storageclass,pv,pvc
kubectl logs test-nfsha-pod
```

Connectez-vous à nfsha pour confirmer que `/srv/kubernetes/test-volume/test.txt` existe réellement. L'application d'un manifeste ne prouve pas que le Pod a écrit le fichier.

## 5. ArgoCD (optionnel)

```bash
ansible-playbook -i etc/hosts playbooks/install_argocd.yml
kubectl get pods,svc -n argocd
```

Identifier le NodePort avec la commande `kubectl get svc`.

## Dépannage rapide

- VM non démarrée : contrôler la virtualisation matérielle, la mémoire disponible et VirtualBox.
- Échec SSH : contrôler la connectivité Host-Only et l'installation de la clé depuis infra01.
- Nœud NotReady : consulter `kubectl get pods -A` et `journalctl -u kubelet`.
- PVC Pending : vérifier le StorageClass, le PV, le chemin NFS et la connectivité au serveur NFS.
- API inaccessible : vérifier la configuration HAProxy et exécuter `curl -k https://192.168.56.8:6443/version`.
