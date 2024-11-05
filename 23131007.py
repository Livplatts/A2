

import pexpect

def telnet_session(ip_address, username, password):
    session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8', timeout=20)
    result = session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Creating a session for:', ip_address)
        return

    session.sendline(username)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering username:', username)
        return

    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering password:', password)
        return

    print('--- Success! Connected to:', ip_address)
    
    # Terminate Session
    session.sendline('quit')
    session.close()

def ssh_session(ip_address, username, password, password_enable):
    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Creating a session for:', ip_address)
        return

    session.sendline(password)
    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering password:', password)
        return

    session.sendline('enable')
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering enable mode...')
        return

    session.sendline(password_enable)
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering enable mode after password is correct')
        return

    session.sendline('configure terminal')
    result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Entering configuration mode')
        return

    session.sendline('hostname R1')
    result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Setting hostname...')
        return

    session.sendline('exit')
    session.sendline('exit')

    print('--- Success! Connected to:', ip_address)

    session.close()

def main():
    ip_address = '192.168.56.101'
    username = 'cisco'
    password = 'cisco123!'
    password_enable = 'class123!'

    while True:
        print("Select connection type:")
        print("1. Telnet")
        print("2. SSH")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            telnet_session(ip_address, username, password)
        elif choice == '2':
            ssh_session(ip_address, username, password, password_enable)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == '__main__':
    main()