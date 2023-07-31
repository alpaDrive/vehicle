'''
    Module that handles the credential management.
    The vid is simply stored in the OS keychain. This obviously isn't secure as the name & key are constants.
    This'll stay until we figure out a better way.
'''
import keyring
import keyring.backend
from keyrings.alt.file import PlaintextKeyring

# We can't use the default encrypted backend as that keeps asking for an encryption password in the console
# which is not viable for simplicity to the end user. ofc this is the same as using a text file but :(
keyring.set_keyring(PlaintextKeyring())

def is_authenticated():
    return keyring.get_password("alpaDrive", "vehicle") is not None

def get_creds():
    creds = keyring.get_password("alpaDrive", "vehicle")
    return creds if creds is not None else ""

def set_creds(value, encrypt=False):
    keyring.set_password("alpaDrive", "vehicle", value)