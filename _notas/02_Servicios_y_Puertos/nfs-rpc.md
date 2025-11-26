---
title: "NFS & Rpcbind (111/2049)"
layout: "single"
category: "Servicios"
slug: "servicios/nfs-rpc"
date: "2025-11-26"
---

### Enumeración
```bash
showmount -e <IP>
nmap -p 111 --script nfs-ls,nfs-showmount,nfs-statfs <IP>
```

### Montar NFS
```bash
mkdir /tmp/nfs
mount -t nfs <IP>:/home /tmp/nfs -o nolock
```

### Escalada (Root Squashing)
Si tiene `no_root_squash`, sube un binario SUID y ejecútalo.
