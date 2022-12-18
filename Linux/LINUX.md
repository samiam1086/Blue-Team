# Linux

## Accounts

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

If you already have an account you do not need to do this but then you want to run ```sudo nano /etc/passwd```
and modify 

```root:x:0:0:root:/root:/bin/bash```
to
```root:x:0:0:root:/root:/sbin/nologin```

## Connections and Execution

Once you have locked down your accounts you will want to keep an eye on who is connected via SSH. I have included a script titled limit-ssh.sh which will take an input of account names to allow access and will kill any connection or script run from another account.
