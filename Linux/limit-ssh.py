import os, sys
import subprocess


color_RED = '\033[91m'
color_reset = '\033[0m'


if __name__ == '__main__':
    if os.geteuid() != 0:
        print('[!] Must be run as sudo')
        sys.exit(1)

    default_ips = [':0', '::1', '127.0.0.1', 'localhost', '-'] # some defaults that we dont want to kill
    whitelisted_users = input('Enter a list of usernames seperated by commas to whitelist ex kali,test\n(NOTE SINCE WE ARE RUNNING THIS AS ROOT YOU MUST INCLUDE root IN THE LIST OR YOU GET KICKED OFF THE MACHINE): ')
    whitelisted_ips = input("Enter a list of IPS seperated by commas to whitelist ex 10.10.10.2\n(NOTE SINCE WE ARE CONNECTING TO THIS MACHINE WITHOUR SSH CONNECTION WHITELIST YOUR INTERNAL IP): ")
    ban_ips = input('Do you want to ban offenders IPS? y/n: ')

    while ban_ips != 'y' and ban_ips != 'n':
        print('invalid option for ban offenders')
        ban_ips = input('Do you want to ban offenders IPS? y/n: ')

    if whitelisted_users.find(',') != -1: # convert their string to a list but if they just give one thats ok too
        whitelisted_users = whitelisted_users.split(',')
    else:
        whitelisted_users = [whitelisted_users]

    if whitelisted_ips.find(',') != -1:# convert their string to a list but if they just give one thats ok too
        whitelisted_ips = whitelisted_ips.split(',')
    else:
        whitelisted_ips = [whitelisted_ips]

    for ip in default_ips: # add our default ips to whitelisted
        whitelisted_ips.append(ip)

    while True:
        try:
            proc = subprocess.run(['w'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # get a list of everyone whose sshed in
            dat = proc.stdout.decode().split('\n')

            for item in dat[2:]: # dat[2:] skips the first two items since they are not relevant
                if item != '': # make sure the string is not empty
                    item = ' '.join(item.split()) # go from multiple whitespaces to one
                    item = item.split(' ') # from string to list removing whitespace

                    if item[0] not in whitelisted_users: # item[0] will be the username
                        os.system('sudo killall -u {}'.format(item[0]))
                        print('WARNING: Non-Whitelisted account {}{}{} connected and their connection was terminated'.format(color_RED, item[0], color_reset))
                        if ban_ips == 'y':
                            os.system('sudo iptables -A INPUT -s {} -j DROP'.format(item[2]))
                            print('Blocking IP address {}{}{} to unblock the IP run: sudo iptables -D INPUT -s {} -j DROP'.format(color_RED, item[2], color_reset, item[2]))  # block the ip through iptables

                    if item[2] not in whitelisted_ips: # itemp[2] will be the from address (IP)
                        process = subprocess.run(['sudo ps -aux | grep ssh | grep \'{}@{}\' | grep -v \'grep\''.format(item[0], item[1])], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # if the ip is not whitelisted we need to get its pid
                        dat1 = process.stdout.decode()
                        dat1 = ' '.join(dat1.split()) # go from multiple whitespaces to one
                        dat1 = dat1.split(' ') # from string to list removing whitespace
                        os.system('sudo kill -9 {}'.format(dat1[1])) # dat1[1] is the pid
                        print('WARNING: Non-Whitelisted IP {}{}{} was found using account {}{}{} on PID {}{}{} was terminated'.format(color_RED, item[2], color_reset, color_RED, dat1[0], color_reset, color_RED, dat1[1], color_reset))
                        if ban_ips == 'y':
                            print('Blocking IP address {}{}{} to unblock the IP run: sudo iptables -D INPUT -s {} -j DROP'.format(color_RED, item[2], color_reset, item[2])) # block the ip through iptables
                            os.system('sudo iptables -A INPUT -s {} -j DROP'.format(item[2]))
        except KeyboardInterrupt:
            print('ctrl+c')
            sys.exit(0)
