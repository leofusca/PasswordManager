master_pwd = input("What is the master password? ") 



def view():
    with open("password.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|") #List format string
            print("User:", user, "Password:", passw)


    pass



def add():
    name = input("Account Name: ")
    pwd = input("Password: ")
    #open(file, mode = "a" = append) 
    with open("password.txt", "a") as f:
        f.write(name + "|" + pwd + "\n")

    


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

