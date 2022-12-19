# Windows

## Accounts

Locking accounts down is imparative to securing a Windows machine.

If your machine is Windows Pro, Enterprise, or Server editions follow these steps.

Step 1 open computer management

![](/assets/Windows/cm.png)

Step 2 browse to Local Users and Groups

![](/assets/Windows/luag.png)

Step 3 open Users

![](/assets/Windows/Users.png)

Now you will be able to see all the local users of the machine. You should look for any users that are non-default and have no purpose existing and delete them. Next you should verify that ALL built in accounts are disabled

![](/assets/Windows/allusers.png)

Delete accounts like this

![](/assets/Windows/susaccount.png)

Disabled (GOOD)

![](/assets/Windows/disabled.png)

Not Disabled (BAD)

![](/assets/Windows/notdisabled.png)

Once you have checked all accounts you will need to look into the groups on the machine to see if there are any that are non-default or contain accounts that they should not.

![](/assets/Windows/allgroups.png)

Check these groups

![](/assets/Windows/checkthesegroups.png)
