from cryptography.fernet import Fernet
import os

'''
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key) '''

def load_salt():
    if not os.path.exists("salt.salt"): #if theres no salt file, create one
        salt = os.urandom(16) #generate a 16-byte random salt
        with open("salt.salt", "wb") as f:
            f.write(salt) #save the salt for later use 
        
    else:
        with open("salt.salt", "rb") as f:
            salt = f.read() #Read existing salt
    return salt

import base64 #Needed to encode the key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(master_pwd, salt):
    #Derives a secure key from the master pass using PBKDF2" 
    kdf =PBKDF2HMAC(
        algorithm = hashes.SHA256(), #secure hashing algo
        length = 32, #We need a 32-byte key for Fernet
        salt = salt, #Use the stored salt 
        iterations=1_000_000, #A higher number of iterations, makes it harder to crack 
        
    )
    return base64.urlsafe_b64encode(kdf.derive(master_pwd.encode())) # COnvert to Fernet-Friendly format


master_pwd = input("What is the master password? ") 
salt = load_salt() # Load or creates the salt
key = derive_key(master_pwd, salt) # Derive a secure key from password
fer = Fernet(key) # Create a Fernet object with the correct key




#key + password + text => random text
#random text + key + password = text to encrypt 

def view():
    try: 
        with open("password.txt", "r") as f:
            for line in f.readlines():                
                user, encrypted_pass = line.strip().split("|") #List format string
                decrypted_pass = fer.decrypt(encrypted_pass.encode()).decode()
                print(f"User:{user} | Password:{decrypted_pass}") 

    except FileNotFoundError:
        print("No passwords stored yet!")

    pass



def add():
    #Add new pass# 

    name = input("Account Name: ")
    pwd = input("Password: ")
    encrypted_pwd = fer.encrypt(pwd.encode()).decode() # Encrypt before storing 
    #open(file, mode = "a" = append) 
    with open("password.txt", "a") as f:
        f.write(f"{name} |{encrypted_pwd}\n") #Store the encrypted password
    print("Password added succesfully!")

    


while True:
    mode = input("Would you like to add a new password or view existing ones? (view, add), press q to quit?").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
        pass
    elif mode == "add":
        add()
        pass
    else:
        print("Invalid mode")
        continue

