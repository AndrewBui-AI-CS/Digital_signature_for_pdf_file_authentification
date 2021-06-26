import qrcode
from PIL import Image
from pyzbar import pyzbar
#sinh qr
def genQR(data, name):

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(name)
    
#doc data tu QR
def getQRDATA(png):
    img = Image.open(png)
    data = pyzbar.decode(img)

    print("qr-code.png decode:" )
    
    return data[0][0]

genQR('message', 'testQR.png')
print(getQRDATA('testQR.png'))