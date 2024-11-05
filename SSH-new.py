import pexpect
import re

def telnet_session(ip_address, username, password):
    # WARNING: Telnet is insecure, use SSH instead.
    print("*** WARNING: Telnet is not recommended. Use SSH for better security. ***")
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

    # Additional Hardening (disable Telnet)
    session.sendline('configure terminal')
    session.expect(r'\(config\)#')
    session.sendline('no ip telnet server')
    session.expect(r'\(config\)#')

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

    session.sendline('hostname liv')
    result = session.expect([r'Liv\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('*** A Failure Has Occurred ***')
        print('Setting hostname...')
        return

    # Additional Hardening (disable HTTP, FTP, etc.)
    session.sendline('no ip http server')
    session.sendline('no ip ftp server')
    session.sendline('no ip domain-lookup')

    # Disable unused VTY lines
    session.sendline('line vty 0 4')
    session.sendline('transport input ssh')
    session.sendline('exit')

    session.sendline('exit')

    print('--- Success! Connected to:', ip_address)

    session.close()

def main():
    ip_address = '192.168.56.101'
    username = 'cisco'
    password = 'cisco123!'  # Use a stronger password in a real environment
    password_enable = 'class123!'  # Use a stronger password for enable mode

    while True:
        print("Select connection type:")
        print("1. Telnet (Not recommended)")
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
