'''
    Module that handles the credential management.
    We'll be using plaintext in a file until the real credential management is figured out.
'''

def is_authenticated():
    try:
        with open("creds.txt", "r") as f:
            return len(f.read()) > 0
    except:
        return False

def get_creds():
    try:
        with open("creds.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def set_creds(value):
    with open("creds.txt", "w") as f:
        f.write(value)