""" This module is a simple TCP connection to an SMTP server 
that allows you to send a message. """
import socket
import ssl
import base64
from pyfiglet import Figlet

# Choose a mail server (e.g. Google mail server) and call it MAILSERVER
MAILSERVER = ('smtp.gmail.com', 587)


def print_ascii_art():
    """ Prints the programs art to create a welcoming environment """
    art = Figlet(font='banner3-D')
    print(art.renderText('ShelMail'))


def print_instructions():
    """ Prints the instructions on how to use the program """
    INSTRUCTIONS = """
    Welcome to Shell Mail, a command line interface that allows
    you to use your GMail account to send an email to one recipient.
    Setup an App Password for your gmail like here:
    https://support.google.com/mail/answer/185833?hl=en#zippy=
    Note this password down and delete after using this program.
    """
    print(INSTRUCTIONS)


def prompt_username():
    """ Asks the user for their gmail account """
    return input("Enter your gmail: ")


def prompt_password():
    """ Asks the user for their app password """
    return input("Enter your app password you just generated: ")


def setup_connection(username, password):
    """ Returns a socket to use for communication """
    # Create socket called client_socket and establish a TCP connection with MAILSERVER
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(MAILSERVER)
    recv = client_socket.recv(1024).decode()

    # Send HELO command and print server response.
    heloCommand = f'EHLO {socket.gethostbyname(socket.gethostname())}\r\n'
    client_socket.send(heloCommand.encode())
    recv = client_socket.recv(1024).decode()

    # STARTTLS command needed to authenticate into server
    STARTTLS_MSG = 'STARTTLS\r\n'
    client_socket.send(STARTTLS_MSG.encode())
    recv = client_socket.recv(1024).decode()

    # Wrap the socket in SSL/TLS protocol
    context = ssl.create_default_context()

    client_socket = context.wrap_socket(
        client_socket, server_hostname=MAILSERVER[0])

    # AUTH LOGIN command
    AUTH_LOGIN_MSG = 'AUTH LOGIN\r\n'
    client_socket.send(AUTH_LOGIN_MSG.encode())
    recv = client_socket.recv(1024).decode()

    try:
        # Username Send
        USERNAME = username.encode()
        ENCODED_USERNAME = base64.b64encode(USERNAME) + b'\r\n'
        client_socket.send(ENCODED_USERNAME)
        recv = client_socket.recv(1024).decode()
        # Check the server response
        # SMTP error codes starting with '5' indicate permanent failures
        if recv.startswith("5"):
            raise Exception(f"SMTP Server Error: {recv}")

    except socket.error as e:
        print(f"Socket error: {e}")
        exit()

    except Exception as e:
        print(f"Error: {e}")
        exit()

    try:
        # Password Send
        PASSWORD = password.encode()
        ENCODED_PASSWORD = base64.b64encode(PASSWORD) + b'\r\n'
        client_socket.send(ENCODED_PASSWORD)
        recv = client_socket.recv(1024).decode()
        if recv.startswith("5"):
            raise Exception(f'SMTP Server Error: {recv}')

    except socket.error as e:
        print(f"Socket error: {e}")
        exit()

    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Send MAIL FROM command and print server response.
    MAIL_FROM_MSG = 'MAIL FROM:<' + username + '>\r\n'
    client_socket.send(MAIL_FROM_MSG.encode())
    recv = client_socket.recv(1024).decode()

    return client_socket


def prompt_recipient():
    """ Prompts user for an address """
    return input("Who would you like to send this to? ")


def prompt_subject():
    """ Prompts user for a subject """
    return input("What should the subject be? ")


def prompt_data():
    """ Prompts user for a message """
    print("Enter your text (press enter twice to stop):")

    user_input = []
    while True:
        line = input()
        if line:
            user_input.append(line)
        else:
            break

    # Joining the lines into a single string
    message_to_send = "\n".join(user_input)
    return message_to_send


def send_message(ssocket, recipient, subject, data):
    """ Executes the message on behalf of the user """
    try:
        # Send RCPT TO command and print server response.
        RCPT_TO_MSG = 'RCPT TO:<' + recipient + '>\r\n'
        ssocket.send(RCPT_TO_MSG.encode())
        recv = ssocket.recv(1024).decode()
        if recv.startswith('250') != True:
            raise Exception("SMTP Error for Recipient")

        # Send DATA command and print server response.
        DATA_MSG = 'DATA\r\n'
        ssocket.send(DATA_MSG.encode())
        recv = ssocket.recv(1024).decode()

        # Send message data.
        DATA_SEND_MSG = 'Subject: ' + subject + '\r\n' + data + '\r\n.\r\n'
        ssocket.send(DATA_SEND_MSG.encode())
        recv = ssocket.recv(1024).decode()
        if recv.startswith('5'):
            raise Exception("SMTP Server Error while building data")

        # Send QUIT command and get server response.
        QUIT_MSG = 'QUIT\r\n'
        ssocket.send(QUIT_MSG.encode())
        recv = ssocket.recv(1024).decode()
        if recv[:3] == '221':
            ssocket.close()

    except ssocket.error as e:
        print(f"Socket error: {e}")
        exit()

    except Exception as e:
        print(f'Exception: {e}')
        exit()


def main():
    """ Main function to send Email through secured TCP connection with
        GMails SMTP server."""
    # Print Ascii
    print_ascii_art()

    # Instructions with link to password setup
    print_instructions()

    # PROMPT USERNAME
    USERNAME = prompt_username()

    # PROMPT PASSWORD
    PASSWORD = prompt_password()

    # SETUP CONNECTION
    SOCKET = setup_connection(USERNAME, PASSWORD)

    # TO ADDR (ONLY 1 RECIPIENT)
    RECIPIENT = prompt_recipient()
    # MESSAGE
    SUBJECT = prompt_subject()
    DATA = prompt_data()
    send_message(SOCKET, RECIPIENT, SUBJECT, DATA)
    # THANKS
    print("Your message has been delivered, thanks!")


if __name__ == '__main__':
    main()
