import qrcode

def genQR():
	my_url = "test"
	qr = qrcode.QRCode(version=1, box_size=10, border=5)
	qr.add_data(my_url)
	qr.make(fit=True)

	img = qr.make_image(fill='black', back_color='white')
	img.save('my_codelearn.png')