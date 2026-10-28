# Diagnostic et limites connues

Le dépôt contient une configuration destinée à être exécutée sur un hôte avec Vagrant et VirtualBox. La publication des fichiers ne prouve pas à elle seule que les VM ou le cluster ont été démarrés.

## Vérifications requises

1. Vérifier les interfaces réseau réelles des VM.
2. Vérifier la connectivité IP et SSH de tous les hôtes depuis infra01.
3. Confirmer que les quatre nœuds Kubernetes apparaissent en état Ready.
4. Tester l'accès à l'API via 192.168.56.8:6443.
5. Vérifier le PVC test-nfsha en état Bound et le Pod test-nfsha-pod prêt.
6. Vérifier le contenu de /srv/kubernetes/test-volume/test.txt sur nfsha.
7. Installer ArgoCD via le playbook optionnel et relever le NodePort attribué.

## Limites

- Les noms d'interfaces et la connectivité en mode pont dépendent de l'hôte.
- Le playbook utilise le dépôt Kubernetes v1.36 et un manifeste Calico versionné : réévaluer leur compatibilité si le dépôt upstream évolue.
- Les opérations Kubernetes utilisent /etc/kubernetes/admin.conf sur le premier control-plane.
- Le StorageClass utilise un provisioner statique : les PV sont créés explicitement, sans provisionnement dynamique.
- Deux control-planes ne garantissent pas le quorum etcd lors de la panne d'un membre.
- Le workflow GitHub Actions vérifie la syntaxe ; il ne lance pas d'infrastructure virtualisée.
