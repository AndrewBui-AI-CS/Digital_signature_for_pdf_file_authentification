#from QrScan import generateCamera
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from genPDF2 import *
from sign import *

# from genPDF import Window
import json
from QrScan import generateCamera


def genPDF(textBox, words, author, fileName):

    if len(author) == 0 or len(fileName) == 0:
        messagebox.showinfo("Lỗi", "Thiếu thông tin")
        return

    global pk, sk, choose
    try:
        if choose == 0:
            sk, pk = generateKey()
            f = open('data/public_key/public_key_'+author+'.pem', 'wb')
            f.write(pk.publickey().exportKey('PEM'))
            f.close()

            f = open('data/private_key/private_key_'+author+'.pem', 'wb')
            f.write(sk.exportKey('PEM'))
            f.close()

            messagebox.showinfo("Tạo tệp", "Đã tạo tệp key")

        data = {
            'sk': sk,
            'fileName': fileName,
            'customer': author,
            'content': textBox,
            'words': words
        }
        # print(data)
        pdf = Generator(data)
        pdf.gen()
        messagebox.showinfo("Tạo tệp", "Đã tạo tệp PDF thành công")
    except:
        messagebox.showinfo("Lỗi", "Tạo tệp gặp lỗi")


def addGenerateTab():
    tab1.columnconfigure(0, weight=1)

    label1 = Label(tab1, text="Người viết", fg='#e6f406',
                   bg='#b172ec', font='bold')
    label1.grid(row=0, pady=(20, 0), padx=(0, 220))
    author = Entry(tab1, width=50, borderwidth=3)
    author.grid(row=1, pady=5)

    label2 = Label(tab1, text="Tên tệp", fg='#ff0', bg='#b172ec', font='bold')
    label2.grid(row=2, pady=(20, 0), padx=(0, 220))
    fileName = Entry(tab1, width=50, borderwidth=3)
    fileName.grid(row=4, pady=5)

    uploadButton = Button(tab1, text="Chọn tệp khóa bí mật nếu có",
                          command=lambda: load_key(), fg='blue', bg='#8cd56c', font='bold')
    uploadButton.grid(row=5, sticky="ew", padx=(240, 240), pady=20)

    keyFileLabel.grid(row=6, pady=5)

    label3 = Label(tab1, text="Viết văn bản",
                   fg='#ff0', bg='#a053e7', font='bold')
    label3.grid(row=7, pady=(20, 0), padx=(0, 0))

    textBox = Text(tab1, height=5, width=20)
    textBox.grid(row=10, columnspan=3, sticky="ew", pady=5, padx=(50, 50))

    label4 = Label(tab1, text="Viết dữ liệu cần ký",
                   fg='#ff0', bg='#a053e7', font='bold')
    label4.grid(row=9, pady=(20, 0), padx=(0, 0))

    textBox2 = Text(tab1, height=5, width=20)
    textBox2.grid(row=8, columnspan=1, sticky="ew", pady=5, padx=(50, 50))

    encodeButton = Button(tab1, text="Tạo PDF", command=lambda: genPDF(str(textBox.get("1.0", END)), str(
        textBox2.get("1.0", END)), str(author.get()), str(fileName.get())), fg='blue', bg='#8cd56c', font=('bold', 20))
    encodeButton.grid(row=11, sticky="ew", padx=(250, 250), pady=30)


def load_key():
    global keyFile, sk, pk, choose
    keyFile = filedialog.askopenfilename()
    if keyFile:
        try:
            print(str(keyFile))
            f = open(keyFile, 'rb')
            sk = RSA.importKey(f.read())
            choose = 1
            f.close()

            print(sk)

            keyFileLabel['text'] = 'Tệp được chọn: ' + str(keyFile)

        except:
            messagebox.showinfo("Mở tệp", "Lỗi đọc tệp\n'%s'" % fname)
        return


def load_file(checkButton):
    global fname, fileNameLabel
    fname = filedialog.askopenfilename()
    if fname:
        try:
            print(str(fname))
            fileNameLabel['text'] = 'Tệp được chọn: ' + str(fname)
            checkButton['state'] = 'normal'

        except:
            messagebox.showinfo("Mở tệp", "Lỗi đọc tệp\n'%s'" % fname)
        return


def check():
    # pdf-->ảnh, sau đó dùng opencv detect QR từ ảnh, sau đó check
    pass


def cameraCheck():
    generateCamera()


def addCheckTab():
    global pk
    tab2.columnconfigure(0, weight=1)

    label6 = Label(tab2, text="* Hướng dẫn: Để mã QR lên trước camera để kiểm tra *",
                   fg='red', bg='#b172ec', font='bold')
    label6.grid(row=2, pady=(20, 0))

    cameraButton = Button(tab2, text="Mở camera", command=lambda: cameraCheck(
    ), fg='blue', bg='#8cd56c', font=('bold', 20))
    cameraButton.grid(row=4, sticky="ew", padx=(250, 250), pady=200)


if __name__ == "__main__":
    root = Tk()
    root.title("QR-PDF")
    root.geometry("800x780")

    # root.state("zoomed")

    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    key1Label = Label(tab2, text="")
    key2Label = Label(tab2, text="")
    key3Label = Label(tab2, text="")

    tabControl.add(tab1, text="  --- Tạo QR-PDF --- ")
    tabControl.add(tab2, text="  --- Xác thực ---")

    background_image = PhotoImage(file='./image/background/bg11.png')
    bg1 = Label(tab1, image=background_image)
    bg1.place(x=0, y=0, relwidth=1, relheight=1)

    bg2 = Label(tab2, image=background_image)
    bg2.place(x=0, y=0, relwidth=1, relheight=1)

    keyFileLabel = Label(tab1, text="")
    fileNameLabel = Label(tab2, text="")

    choose = 0

    addGenerateTab()
    addCheckTab()

    tabControl.pack(expand=1, fill='both')
    root.mainloop()
