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

To disable an account through Computer Management right click on the account select properties and you should see a properties box appear. From there select account is disabled.

![](/assets/Windows/aid.png)

Once you have checked all accounts you will need to look into the groups on the machine to see if there are any that are non-default or contain accounts that they should not.

![](/assets/Windows/allgroups.png)

Check these groups

![](/assets/Windows/checkthesegroups.png)

If you are on Windows 10 Home open Control Panel > User Accounts > User Accounts > Manage Another Account
From here follow the same steps as above for hunting down accounts that do not belong.

## Firewall

First things first on the firewall if it is not enabled ensure that there is an exception rule for however you are connecting to the machine (Likely port 3389) otherwise you will lose your connection to the machine and not be able to get it back without some technical approaches.

Once you have added your RDP exception enable the firewall and then select Advanced Settings.
You should now see something like this

![](/assets/Windows/firewall.png)

Since Inbound rules are the most important we are going to focus on them first

As you go through the firewall rules if you happen to notice any that simply allow a connection inbound over any port that is BAD and you will want to disable it.

Next we will want to block RPC on port 135 SMB on port 445 and 139 (if it is not necessary for the servers function) SNMP on port 161 MSRPC on port 593 WINRM on port 5985 and 5986

## Locking Down RDP

So for most RDP is a very useful service that enables remote management of a machine, however it is often full of vulnerabilities. To mitigate this we can change the default RDP port to something that an attacker may not find such as 64423 or another extremely high port that would require an extra flag on the nmap scan.

To do this we can modify the registry key

```HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp``` and modify ```PortNumber``` set the value to decimal and enter a number to connect over (YOU WILL NEED TO UPDATE THE RDP EXCEPTION IN THE FIREWALL TO INCLUDE THIS PORT).

## Locking Down SMB

You cannot always just disable SMB through the firewall due to it being a requirement for the server's service. To mitigate this we can do a few things.

Number 1 Enforce SMB Signing 

Open Local Security Policy
You should be greeted by this window

![](/assets/Windows/lsp.png)

Then navigate to Local Policies > Security Options and find ```Microsoft network server: Digitally sign communications (always)``` and ```Microsoft network client: Digitally sign communications (always)``` and set them to Enabled

Alternatively you can do this through the Windows registry by creating a key named RequireSecuritySignature  with a value of 1 under 
```HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\LanManWorkstation\Parameters``` and ```HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters```

You will also want to disable SMBv1 and to do this open Powershell as administrator and run 

```Get-SmbServerConfiguration | Select EnableSMB1Protocol``` to see if it is enabled and then ```Set-SmbServerConfiguration -EnableSMB1Protocol $false``` to disable it. You will also want to run ```Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol``` to see if the feature is installed and ```Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol``` to remove the feature (This will prompt the machine to restart you should decline till later).

## Lock Down LLMNR

LLMNR stands for link locak multicast name resolution and it is generally used for networks that do not have DNS set up properly to allow computers to communicate, however it allows for an attacker to poison traffic to gain account NetNTLMv2 hashes so we want to disable it.

Open Edit Group Policy
You should see

![](/assets/Windows/gpo.png)

Then navigate to ```Computer Configuration > Administrative Templates > Network > DNS Client > Turn off multicast name resolution``` and set it to enabled or in regedit navigate to ```HKEY_LOCAL_MACHINE\Software\policies\Microsoft\Windows NT\DNSClient``` and create a key named ```EnableMulticast``` as a ```REG_DWORD``` value and set it to ```0```

## Disable IPV6

if(ipv6 == notInUse):
  disable(ipv6)
  
If IPV6 addresses are not being leased out by DHCP disable it because it is a MITM attack vector that you dont need.

## Remove Remote Registry

Open CMD as an admin and run ```sc delete RemoteRegistry``` it is not necessary and is only an attack vector.

## Lock Down LSASS

Edit the registry key ```HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa``` and create a key names ```RunAsPPL``` as a ```REG_DWORD``` with the value of ```2```

## Other Security Policies to Check

Open ```Local Security Policy > Local Polocoes > Security Options```
```
Policy Name : Optimal setting

Accounts: Administrator account status : Disabled
Accounts: Guest account status : Disabled
Accounts: Limit local account use of blank passwords to console logon only : Enabled
Accounts: Rename administrator account : Anything other than Administrator
Accounts: Rename guest account : Anything other than Guest
Devices: Prevent users from installing printer drivers when connecting to shared printers : Enabled
Domain member: Digitally encrypt or sign secure channel data (always) : Enabled
Microsoft network client: Digitally sign communications (always) : Enabled
Microsoft network client: Send unencrypted password to connect to third-party SMB servers : Disabled
Microsoft network server: Digitally sign communications (always) : Enabled
Network access: Do not allow anonymous enumeration of SAM accounts : Enabled
Network access: Do not allow anonymous enumeration of SAM accounts and shares : Enabled
Network access: Let Everyone permissions apply to anonymous users : Disabled
Network access: Remotely accessible registry paths : Make it empty
Network access: Remotely accessible registry paths and subpaths : make it empty
Network access: Restrict anonymous access to Named Pipes and Shares : Enabled
Network access: Restrict clients allowed to make remote calls to SAM : Click Edit Security and then change from Allow to Deny
User Account Control: Use Admin Approval Mode for the built-in Administrator account : Enabled
User Account Control: Behavior of the elevation prompt for administrators in Admin Approval Mode : Prompt for conesent for non-windows binaries
User Account Control: Behavior of the elevation prompt for standard users : Prompt for credentials
User Account Control: Only elevate executable files that are signed and validated : Enabled is optimal if it does not break anything
User Account Control: Turn on Admin Approval Mode : Enabled
```
## Block things that help redteam

Open ```Local Security Policy``` and right-click on ```Software Restriction Policies``` then click ```New Software Restriction Policys``` now navigate to ```Additional Rules``` now right click in the area and select ```New Path Rule```

![](/assets/Windows/rc.png)

Now you should see

![](/assets/Windows/dis.png)

Ensure that Security level is set to disabled and press browse. Now find the executable you want to disable.
Some good ones are 

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe
C:\Windows\System32\regsvr32.exe  Maybe not this one as I am unsure how much it is used by windows and other programs
C:\Windows\SysWOW64\regsvr32.exe  Maybe not this one as I am unsure how much it is used by windows and other programs
C:\Windows\SysWOW64\cmd.exe
C:\Windows\System32\cmd.exe
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell_ise.exe
C:\WINDOWS\syswow64\WindowsPowerShell\v1.0\powershell.exe
C:\WINDOWS\syswow64\WindowsPowerShell\v1.0\powershell_ise.exe
```

## Uninstall Windows Features

Delete the Windows Store

Open ```Turn Windows features on or off``` then Uninstall/Uncheck

```
Internet Explorer 11
SMB 1.0/CIFS File Sharing Support
Telnet Client
TFTP Client
Windows Powershell 2.0
```
