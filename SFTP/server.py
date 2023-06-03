import pysftp
from getpass import getpass

def handle_file_transfer(event):
    if event == 'put': print("File uploaded")
    elif event == 'get': print("File downloaded")

def sftp_server():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('known_hosts')
    username = input("Username: "); password = getpass("Password: ")

    server_opts = {
        'cnopts': cnopts,
        'username': username,
        'password': password,
        'log': True
    }

    with pysftp.Connection('localhost', **server_opts) as sftp:
        sftp.cwd('/home')

        while True:
            try:
                command = input("SFTP Server > ")

                if command.startswith('put'):
                    local_file = command.split()[1]
                    remote_file = command.split()[2]
                    sftp.put(local_file, remote_file, callback=handle_file_transfer('put'))
                elif command.startswith('get'):
                    remote_file = command.split()[1]
                    local_file = command.split()[2]
                    sftp.get(remote_file, local_file, callback=handle_file_transfer('get'))
                elif command == 'quit': print("Closing SFTP server..."); break
                else: print("Invalid command")
            except Exception as e: print("Error:", str(e))

if __name__ == '__main__': sftp_server()
