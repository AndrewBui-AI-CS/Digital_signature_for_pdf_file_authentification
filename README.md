# DS_for_pdf_file_authentification
In this project, we built an application based mainly on some cryptopagraphic algorithms that we have learnt from school.
Hopefully, this demo app will satisfy our mentor and all of you, our visitors.


**Contributor**:
- Nguyễn Nam Hán
- Nguyễn Duy Tùng 
- Bùi Việt Hoàng

# Create virtual environment and install dependencies
Run the command below to create a virtual environment.
```ruby
virtualenv --python=/usr/bin/python3 myvenv
```

Then activate the virtual environment.
```ruby
. myvenv/bin/activate
```

Finally, install the dependencies.
```ruby
pip install -r requirements.txt
```

# Data
We divided data into 3 main parts: 
- Public key
- Private key
- Pdf file

All these data were saved under data folder


## Usage
```ruby
python main.py
```
Fill in all fields required

And then hit the create button

## For the purpose of verifying
From the pop-up interface: 
- Go to next page by click authentifying button
- Open the camera
- Then checking the qr code using your devices and see if a red or green rectangle shows up

## License
[Not yet](https://en.wikipedia.org/wiki/MIT_License)
