# Linux

Step 1 of hardening Linux is to determine what accounts are present on the system to do this run:

```
cat /etc/passwd
```

You should get an output that resembles the images below.
![](/assets/Linux/etcpasswd_output.png)
![](/assets/Linux/etcpasswd_output1.png)

Now this does look incredibly overwhelming to someone who is not very used to the Linux operating system, however lets break it down. The format is

```
username:x:userID::homeDirectory:accessToSystem
```
The big thing we want to look for is the accessToSystem piece of the account 99% of the default accounts should haves access of /usr/sbin/nologin 

![](/assets/Linux/nologon.png)

While some will have others if the account has /bin/bash and is not an account that you are familiar with you should likely remove that account as it has SSH access and can access the command line.

![](/assets/Linux/redflag.png)

If the root account is set to /bin/bash or any other non disabled state you will want to promote another user to the administrator group via

```usermod -aG wheel account```    for CentOS/RHEL
or
```usermod -aG sudo account```    for Debian/Ubuntu

You will then want to verify that this worked by running ```sudo su```
