import cv2
import numpy as np
from pyzbar.pyzbar import decode

from src.sign import *


def generateCamera():
    # pk='' #lay tu ma qr ra
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            # print(myData)
            # print('next')
            data_list = myData.split('#')
            # print(data_list)
            # print(binascii.unhexlify(data_list[1]))
            # print(data_list[0])

            # Read key from file
            file_path = 'data/public_key/'
            f = open(file_path + 'public_key_' + data_list[2]+'.pem', 'rb')
            # print(data_list)
            # print('\n')
            publickey = RSA.importKey(f.read())
            # print(publickey)

            if verify_msg(bytes(data_list[0], 'utf-8'), publickey, binascii.unhexlify(data_list[1])):
                myOutput = 'Authorized'
                myColor = (0, 255, 0)
            else:
                myOutput = 'Un-Authorized'
                myColor = (0, 0, 255)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, myColor, 2)

        cv2.imshow('Result', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
# generateCamera()
