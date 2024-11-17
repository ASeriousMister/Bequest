import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
import os


def gen_qr_codes(text, block_size=200):
    # Divides text in blocks of a desired size
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]

    # Create QR codes for each block and save them in .png files
    for i, block in enumerate(blocks):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(block)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        file_name = f"qr_code_{i + 1}.png"
        img.save(file_name)
        print(f"Saved: {file_name}")


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

    new_text = []
    alphabet = 'abcdefghijklmnopqrstuvwxyzàèéìòù'
    alphabet_cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÌÒÙ'
    alphabet_lenght = len(alphabet)
    
    # Prepare key as list of indexes
    index_key = [(alphabet.index(letter) if letter in alphabet else alphabet_cap.index(letter))
                     for letter in key_phrase if letter in alphabet or letter in alphabet_cap]
    key_lenght = len(index_key)
    # encrypting    
    for i, letter in enumerate(text):
        if letter in alphabet:
            index_letter = alphabet.index(letter)
            index_shift = index_key[i % key_lenght]           
            if mode == 'decrypt':
                index_shift = -index_shift           
            new_letter = alphabet[(index_letter + index_shift) % alphabet_lenght]
            new_text.append(new_letter)
        elif letter in alphabet_cap:
            index_letter = alphabet_cap.index(letter)
            index_shift = index_key[i % key_lenght]           
            if mode == 'decrypt':
                index_shift = -index_shift           
            new_letter = alphabet_cap[(index_letter + index_shift) % alphabet_lenght]
            new_text.append(new_letter)
        else:
            new_text.append(letter)
    if mode == 'encrypt':
        #create QR codes
        gen_qr_codes(''.join(new_text))
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

    new_text = []
    alphabet = 'abcdefghijklmnopqrstuvwxyzàèéìòù'
    alphabet_cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÌÒÙ'
    alphabet_lenght = len(alphabet)
    
    # Prepare key as list of indexes
    index_key = [(alphabet.index(letter) if letter in alphabet else alphabet_cap.index(letter))
                     for letter in key_phrase if letter in alphabet or letter in alphabet_cap]
    key_lenght = len(index_key)  
    # Decrypting 
    for i, letter in enumerate(text):
        if letter in alphabet:
            index_letter = alphabet.index(letter)
            index_shift = index_key[i % key_lenght]           
            if mode == 'decrypt':
                index_shift = -index_shift           
            new_letter = alphabet[(index_letter + index_shift) % alphabet_lenght]
            new_text.append(new_letter)
        elif letter in alphabet_cap:
            index_letter = alphabet_cap.index(letter)
            index_shift = index_key[i % key_lenght]
            
            if mode == 'decrypt':
                index_shift = -index_shift
            
            new_letter = alphabet_cap[(index_letter + index_shift) % alphabet_lenght]
            new_text.append(new_letter) 
        else:
            new_text.append(letter)
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
    messagebox.showinfo("About the Bequest tool", "This tool creates a series of QR codes containiing the provided text encrypted with the key phrase. To decrypt QR codes read them in order with a reader like QtQR, paste content in the box and provide the same key phrase. More info at https://github.com/ASeriousMister/Bequest.")


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

