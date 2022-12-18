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

Accounts go from top to bottom in the order that they were created in so any user created accounts or non built-in system accounts will apeear at the bottom of ```/etc/passwd```

![](/assets/Linux/nonsystemaccounts.png)

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

Once you have locked down your accounts you will want to keep an eye on who is connected via SSH. I have included a script titled limit-ssh.sh which will take an input of account names to allow access and will kill any connection or script run from another account. It is also a good idea to run the ```w``` command before you run it as many score tracking services may be running under specific accounts and you will need to ignore them by including them within the whitelist.

It is also recommended to run ```sudo find / -name authorized_keys``` which will search for the authorized_keys file. authorized_keys is a file normally contained in a .ssh directory and contains SSH public keys that allow for someone to connect to a machine without a password. If you are note meant to be connecting with SSH keys and only passwords it is recommended to open these files (they are flat text files that can be reat with cat or nano) and if they contain keys that you are unsure as to the source of it is recommended to remove the keys and file.

## Finding Interesting Items

Once you have connected it is recommended to start by searching the ```/home/``` directory with an ```ls -a``` as this will show all files and folders contained within. Then begin entering each folder and run the same command to see if there is any obvious files that do not belong. 

## Check Running Services

To check the running services on a Linux machine run ```sudo systemctl```

This will bring up a large wall of text showing each service and if it is running or not. To continue to the next page of services press ```Enter``` and to exit press ```q``` 
