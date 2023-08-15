try:
    import obd, pynmea2, qrcode, serial, requests, websockets, qrcode
    print("You're good to go! All modules have been installed and appear to be working fine...")
except Exception as e:
    print("Some modules couldn't be imported. This is what the Python interpreter has to say...\n")
    print(e)
    print("\nYou have to fix this error before continuing...\nTry running sudo pip install -r requirements.txt instead of pip3.\nIf it persists, please open a detailed issue at https://github.com/alpaDrive/vehicle/issues.")