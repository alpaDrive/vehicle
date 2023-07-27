'''
    Module that handles the credential management.
    The vid is simply stored in the OS keychain. This obviously isn't secure as the name & key are constants.
    This'll stay until we figure out a better way.
'''
import keyring

def is_authenticated():
    return keyring.get_password("alpaDrive", "vehicle") is not None

def get_creds():
    creds = keyring.get_password("alpaDrive", "vehicle")
    return creds if creds is not None else ""

def set_creds(value):
    keyring.set_password("alpaDrive", "vehicle", value)