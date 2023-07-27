import io, qrcode

def print_qr(data):    
    qr = qrcode.QRCode()
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f'    {f.read().strip()}')