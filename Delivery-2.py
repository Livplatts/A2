

import pexpect



def telnet_session(ip_address, username, password):
    session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)
    result = session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Creating a session for:', ip_address)
      

    session.sendline(username)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering username:', username)
      

    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering password:', password)
        

    print('--- Success! Connected to:', ip_address)
    
    # Terminate Session
    session.sendline('quit')
    session.close()

def task1_ssh (ip_address, username, password, password_enable):
    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Creating a session for:', ip_address)
        

    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering enable mode after password is correct')
       

    session.sendline('configure terminal')
    result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering configuration mode')
        

    session.sendline('hostname Liv')
    result = session.expect([r'Liv\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Setting hostname...')
       

    session.sendline('exit')
    session.sendline('exit')

    print('--- Success! Connected to:', ip_address)

    session.close()

def task2_harden (ip_address, username, password, hardening_items):
    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    hardening_items() = {
    'SSH enabled': 'ip ssh  version 2',
    'Telnet disabled': 'no service telnet',
    'Password encryption': 'service password-encryption',
    'Logging enable': 'logging buffered',
    'NTP configured': 'ntp server'
}

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Creating a session for:', ip_address)
        

    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering enable mode after password is correct')
       

    runningConfig = session.sendline('show running-config')
    
    for check, rule in hardening_items.items():
        if rule in runningConfig:
            print(f"[PASS] {check}")
        else:
            print(f"[FAIL] {check}")
    
    session.close()
def task2_syslog (ip_address, username, password, hardening_items):
    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline("access-list 100 pemit ip 192.168.56.0 0.0.0.255 any")
    session.sendline("access-list deny ip any any ")
    session.sendline("logging host 192.168.56.101")
    session.sendline("logging trap information")

    session.close()

def main():
    ip_address = '192.168.56.101'
    username = 'cisco'
    password = 'cisco123!'
    password_enable = 'class123!'

    while True:
        print("Select connection type:")
        print("1. Task 1 Telnet")
        print("2. Task 1 SSH")
        print("3. Task 2 Compare config to hardening" )
        print("4. Task 2 Enable syslog")
        print("q. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            telnet_session(ip_address, username, password)
        elif choice == '2':
            task1_ssh(ip_address, username, password, password_enable)
        elif choice == '3':
            task2_harden(ip_address, username, password, password_enable)
        elif choice == '4':
            task2_syslog(ip_address, username, password, password_enable)
        elif choice.lower() == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == '__main__':
    main()