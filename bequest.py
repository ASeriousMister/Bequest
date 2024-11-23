import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
import os
import string
import random


def gen_qr_codes(text, block_size=180):
    # Divides text into blocks of the desired size
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]

    # Pad the last block with random characters if it's less than block_size characters
    if len(blocks) > 0 and len(blocks[-1]) < block_size:
        padding_length = block_size - len(blocks[-1])
        blocks[-1] += ''.join(random.choices(string.ascii_letters + string.digits, k=padding_length))

    # Create QR codes for each block and save them as .png files
    for i, block in enumerate(blocks):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )      
        try:
            # Encode block in UTF-8 and add it to the QR code
            qr.add_data(block.encode('utf-8'))
            qr.make(fit=True)
            # Generate and save the QR code image
            img = qr.make_image(fill='black', back_color='white')
            file_name = f"qr_code_{i + 1}.png"
            img.save(file_name)
            print(f"Saved: {file_name}")
        except Exception as e:
            print(f"Error creating QR code for block {i + 1}: {e}")


# Create a generator that yields the shift value for each letter based on the ASCII values of the word series.
def get_shift(key_phrase_l):
    shift_string = ''.join(key_phrase_l)
    while True:
        for char in shift_string:
            yield ord(char.lower()) - ord('a')


def encrypt_text():
    mode = 'encrypt'
    text = input_text_box.get("1.0", tk.END).strip()
    key_phrase = encryption_phrase_box.get().strip()
    if not text or not key_phrase:
        messagebox.showwarning("Input Error", "Please provide both text and encryption phrase.")
        return
    if select_folder == '':
        messagebox.showwarning("Please select the folder where to save files.")
        return

    key_phrase_l = key_phrase.split()
    shift_generator = get_shift(key_phrase_l)
    new_text = []

    for char in text:
        if char.isalpha():  # Only shift alphabet characters
            shift = next(shift_generator)
            if mode == "decrypt":
                shift = -shift  # Reverse the shift for decryption
            
            base = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap within the alphabet range
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            new_text.append(shifted_char)
        else:
            new_text.append(char)  # Keep non-alphabet characters unchanged
    if mode == 'encrypt':
        #create QR codes
        text_4_qr = ''.join(new_text)
        print(f'Encrypted text: {text_4_qr}')
        gen_qr_codes(text_4_qr)
        messagebox.showinfo("Success", f"QR_codes saved to {selected_folder}!")
    elif mode == 'decrypt':
        with open('output.txt', 'w') as f:
            f.write(''.join(new_text))
            messagebox.showinfo("Success", f"Decrypted text saved to {selected_folder}!")


def decrypt_text():
    mode = 'decrypt'
    text = input_text_box.get("1.0", tk.END).strip()
    key_phrase = encryption_phrase_box.get().strip()
    if not text or not key_phrase:
        messagebox.showwarning("Input Error", "Please provide both text and encryption phrase.")
        return
    if select_folder == '':
        messagebox.showwarning("Please select the folder where to save files.")
        return

    key_phrase_l = key_phrase.split()
    shift_generator = get_shift(key_phrase_l)
    new_text = []

    for char in text:
        if char.isalpha():  # Only shift alphabet characters
            shift = next(shift_generator)
            if mode == "decrypt":
                shift = -shift  # Reverse the shift for decryption
            
            base = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap within the alphabet range
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            new_text.append(shifted_char)
        else:
            new_text.append(char)  # Keep non-alphabet characters unchanged
    if mode == 'encrypt':
        #create QR codes
        gen_qr_codes(''.join(new_text))
        messagebox.showinfo("Success", f"QR_codes saved to {selected_folder}!")
    elif mode == 'decrypt':
        with open('output.txt', 'w') as f:
            f.write(''.join(new_text))
            messagebox.showinfo("Success", f"Decrypted text saved to {selected_folder}!")


def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.config(text=f"Selected Folder: {selected_folder}")
        os.chdir(selected_folder)
        dir = os.listdir(selected_folder)
        if len(dir) != 0:
            messagebox.showinfo("Warning!", "The selected folder is not empty and some files might be overwritten")
    else:
        folder_label.config(text="No folder selected")


def manual():
    messagebox.showinfo("About the tool", "This tool creates a series of QR codes containiing the provided text encrypted with the key phrase. To decrypt QR codes read them in order with a reader like QtQR, paste content in the box and provide the same key phrase. Keep QR codes in safe places, like documents that usually contain QR codes like a boarding pass.")


# Create the main window
root = tk.Tk()
root.title("The Bequest tool")
root.geometry("505x480")

# Large Text Box for input text
input_text_box_label = tk.Label(root, text="Input your text:")
input_text_box_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
input_text_box = tk.Text(root, height=10, width=60)
input_text_box.grid(row=1, column=0, padx=10, pady=5)

# One line Text Box for encryption phrase
encryption_phrase_label = tk.Label(root, text="Encryption phrase:")
encryption_phrase_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
encryption_phrase_box = tk.Entry(root, width=60)
encryption_phrase_box.grid(row=3, column=0, padx=10, pady=5)

# Button to select the folder
select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

# Label to display selected folder
folder_label = tk.Label(root, text="No folder selected")
folder_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

# Encrypt Button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_button.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

# Decrypt Button
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_text)
decrypt_button.grid(row=6, column=0, padx=10, pady=10, sticky=tk.E)

# Instruction Button
instruction_button = tk.Button(root, text="?", command=manual)
instruction_button.grid(row=7, column=0, padx=10, pady=10, sticky=tk.E)

# Initialize selected folder variable
selected_folder = None

# Run the tool
root.mainloop()

