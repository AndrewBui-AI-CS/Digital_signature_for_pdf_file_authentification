from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from genPDF2 import *
from sign import *

# from genPDF import Window

def genPDF(textBox, author, fileName):
    global pk,sk
    try:
        if sk=='' or pk=='':
            sk, pk= generateKey()
            f=open('key.txt', 'w')
            f.writelines (str(sk)+'\n'+str(pk)) 
            messagebox.showinfo("Tạo tệp", "Đã tạo tệp key.txt")        
        
        print(textBox+author+fileName)
        data = {
                'sk': sk,
                'pk':pk,
                'fileName': fileName,
                'customer': author,
                'content': textBox
            }
        pdf=Generator(data)
        pdf.gen()
        messagebox.showinfo("Tạo tệp", "Đã tạo tệp PDF thành công")
    except:
        showerror("Lỗi", "Tạo tệp gặp lỗi")
        


def addGenerateTab():
    tab1.columnconfigure(0, weight=1)

    label1 = Label(tab1, text="Người viết")
    label1.grid(row=1, pady=10)
    author = Entry(tab1, width=50, borderwidth=3)
    author.grid(row=2, pady=0)

    label2 = Label(tab1, text="Tên tệp")
    label2.grid(row=3, pady=10)
    fileName = Entry(tab1, width=50, borderwidth=3)
    fileName.grid(row=4, pady=0)
    
    uploadButton = Button(tab1, text="Chọn tệp", command=lambda: load_key())
    uploadButton.grid(row=5, sticky="ew", padx=(250,250), pady=10)

    keyFileLabel.grid(row=6,pady=5)

    textBox = Text(tab1, height=15, width=20)
    textBox.grid(row=7, columnspan=3, sticky="ew", pady=20, padx=(50,50))

    encodeButton = Button(tab1, text="Tạo PDF", command=lambda: genPDF(str(textBox.get("1.0", END)), str(author.get()),str(fileName.get())))
    encodeButton.grid(row=8, sticky="ew", padx=(250,250), pady=30)
def load_key():
    global keyFile, sk, pk
    keyFile = filedialog.askopenfilename()
    if keyFile:
        try:
            print(str(keyFile))
            f=open(keyFile, 'r')
            sk=f.readline()
            pk=f.readline()
            
            keyFileLabel['text'] = 'Tệp được chọn: ' + str(keyFile)  
            
        except:            
            showerror("Mở tệp", "Lỗi đọc tệp\n'%s'" % fname)
        return
    
def load_file(checkButton):
    global fname, fileNameLabel
    fname = filedialog.askopenfilename()
    if fname:
        try:
            print(str(fname))
            fileNameLabel['text'] = 'Tệp được chọn: ' + str(fname)
            checkButton['state']= 'normal'         

        except:            
            showerror("Mở tệp", "Lỗi đọc tệp\n'%s'" % fname)
        return

def check():
#pdf-->ảnh, sau đó dùng opencv detect QR từ ảnh, sau đó check
    pass
def cameraCheck():
    print('đã mở cam')

def addCheckTab():
    tab2.columnconfigure(0, weight=1)
    textBox = Text(tab2, height=5, width=20)
    textBox.grid(row=3, sticky="ew", padx=(50,50), pady=20)
    
    cameraButton = Button(tab2, text="Mở camera", command=lambda: cameraCheck())
    cameraButton.grid(row=4, sticky="ew", padx=(250,250), pady=10)

    uploadButton = Button(tab2, text="Chọn tệp", command=lambda: load_file(checkButton))
    uploadButton.grid(row=5, sticky="ew", padx=(250,250), pady=10)

    fileNameLabel.grid(row=6,pady=5)

    checkButton = Button(tab2, text="Xác thực", state=DISABLED, command=lambda: check())
    checkButton.grid(row=8, sticky="ew", padx=(250,250), pady=10)


if __name__ == "__main__":
    root = Tk()
    root.title("QR-PDF")
    root.geometry("800x600")

    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    key1Label = Label(tab2, text="" )
    key2Label = Label(tab2, text="" )
    key3Label = Label(tab2, text="" )

    tabControl.add(tab1, text="  Tạo QR-PDF ")
    tabControl.add(tab2, text="  Xác thực ")

    keyFileLabel = Label(tab1, text="" )
    fileNameLabel = Label(tab2, text="" )
    
    sk=''
    pk=''
    

    addGenerateTab()
    addCheckTab()

    tabControl.pack(expand=1,fill='both')
    root.mainloop()


