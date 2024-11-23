# Bequest
## About the tool
This tool aims to provide users with a simple and pretty safe way to store confidential information allowing only trusted parties to access them.\
This task is achieved by creating a series of QR codes containing text that was encrypted with a key phrase that has to be known by the trusted parties that might need to access the information.

## How to install the tool
The tool is a simple GUI written in python that usually works with native libraries.\
In Debian environments it is recommended to install python3-full:
```
sudo apt install python3-full
```
Then, once downloaded the tool, launch it:
```
python3 bequest.py
```

## How to use the tool
### Encryptiing text
To encrypt text it is enough to:
- write the text to encrypt in the big text box;
- write the key phrase in the smaller text box (parties that may need to access the text have to know it!);
- select a folder where to save the QR codes (it is recommended to select an empty folder. The tool is saving qr codes in `.png` files named as `qr_code_1.png`, `qr_code_2.png`,... and in case there are other files named this way, they will be overwritten prioritizing the need to save the encrypted text);
- click the *Encrypt* button.

### Decrypting text
To decrypt the text it is necessary to:
- read the Qr codes respecting the correct order with a tool like QtQR, which can be installed in Debian based environments with `sudo apt install qtqr` (in some cases it was noticed that QR codes aren't read properly with QtQR and CoBang but the same codes were read in the correct way by smartphones);
- paste the text in the bigger text box;
- type the key phrase in the smaller text box;
- select a folder where to save the decrypted text (it is recommended to select an empty folder. The tool is saving the text in a file named `output.txt` and will overwrite existing files with this name, prioritizing the need to access the decrypted information);
- click the *Decrypt* button.

## Recommendations
Before storing the QR codes it is recommended to check if the tool encrypted the text in the proper way and if it is able to decrypt it correctly.\
QR codes have to be stored in a safe place, that could be any kind of electronic device or even on paper using documents that usually contain QR codes (i.e. boarding pass) hiding them in plain sight.

## Disclaimer
THE BEQUEST TOOL IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.\
THE AUTHORS AND DISTRIBUTORS OF BEQUEST DISCLAIM ALL LIABILITY FOR ANY DAMAGES OR LOSSES RESULTING FROM THE USE OF THIS TOOL, INCLUDING BUT NOT LIMITED TO:\
DEFECTS OR ISSUES ARISING FROM THIRD-PARTY DEPENDENCIES OR LIBRARIES.\
PROBLEMS CAUSED BY USER ERROR, MISUSE, OR MODIFICATION OF THE TOOL.\
INCOMPATIBILITIES WITH SPECIFIC OPERATING SYSTEMS, ENVIRONMENTS, OR CONFIGURATIONS.\
BY USING BEQUEST, YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTAND, AND AGREE TO THIS DISCLAIMER OF WARRANTY AND LIMITATION OF LIABILITY.
