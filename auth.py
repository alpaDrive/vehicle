'''
    Module that handles the credential management.
    We'll be using plaintext in a file until the real credential management is figured out.
'''

def is_authenticated():
    try:
        f = open("creds.txt", "r")
        return len(f.read()) > 0
    except:
        return False

def get_creds():
    try:
        f = open("creds.txt", "r")
        return f.read()
    except FileNotFoundError:
        return ""

def set_creds(value):
    f = open("creds.txt", "w")
    f.write(value)
    f.close()