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

Le script copie la clé SSH vers chaque VM ; il doit être lancé depuis infra01 avec le compte du laboratoire.

## 3. Lancer le playbook principal

```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i etc/hosts playbooks/site.yml
```

Le playbook installe BIND9, prépare containerd et les paquets Kubernetes, configure HAProxy et NFS, initialise le cluster, joint les autres nœuds et déploie un test NFS. L'exécution demande une connexion Internet et peut durer selon les téléchargements.

## 4. Déployer l'application HTTP avec Ingress

```bash
ansible-playbook -i etc/hosts playbooks/install_ingress_nginx.yml
kubectl get pods -n nginx-ingress
kubectl get svc -n nginx-ingress
kubectl get ingress -n demo-app
```

Le playbook installe le contrôleur NGINX Ingress, puis applique un Deployment Nginx à deux réplicas, un Service ClusterIP et une ressource Ingress pour le nom d'hôte `demo.esgi.net`.

Relever le NodePort HTTP :

```bash
kubectl get svc -n nginx-ingress
```

Tester depuis un poste connecté au réseau Host-Only, en remplaçant `<NODEPORT_HTTP>` par le port affiché :

```bash
curl -H "Host: demo.esgi.net" http://192.168.56.6:<NODEPORT_HTTP>/
```

## 5. Vérifier le cluster et NFS

```bash
ansible-playbook -i etc/hosts playbooks/verify_cluster.yml
kubectl get nodes -o wide
kubectl get pods -A
kubectl get storageclass,pv,pvc
kubectl logs test-nfsha-pod
```

Sur la VM nfsha, vérifier que `/srv/kubernetes/test-volume/test.txt` existe. L'application du manifeste seule ne prouve pas qu'un fichier a été écrit.

## 6. ArgoCD (optionnel)

```bash
ansible-playbook -i etc/hosts playbooks/install_argocd.yml
kubectl get pods,svc -n argocd
```

## Dépannage rapide

- VM non démarrée : contrôler la virtualisation matérielle, la mémoire disponible et VirtualBox.
- Échec SSH : contrôler le réseau Host-Only et l'installation de la clé depuis infra01.
- Nœud NotReady : consulter `kubectl get pods -A` et `journalctl -u kubelet`.
- PVC Pending : vérifier le StorageClass, le PV, le chemin NFS et la connectivité au serveur NFS.
- Ingress inaccessible : contrôler les Pods et le NodePort dans le namespace nginx-ingress, puis le champ host de la ressource Ingress.
- API inaccessible : contrôler HAProxy et tester `curl -k https://192.168.56.8:6443/version`.
