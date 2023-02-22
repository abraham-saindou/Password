import string
import json
from hashlib import sha256


class JsonHandling:  # Contains 2 functions: first add password hash to json, second check if a hash is in file.
    def addtojsonfile(self):  # User input a name for dictionary's key, then open file to add dict to json file.
        name = input("Enter a name for your  : ")
        tofile = {
            name: self.crypted_password
        }
        with open(self.filename, "r+") as file:
            data = json.load(file)
            data["Password"].append(tofile)
            file.seek(0)
            json.dump(data, file, indent=2)
        choice = input("Do you want to see all passwords ? 'Yes' or 'No'")
        if choice == 'Yes':
            with open(self.filename, 'r') as file:  # Open the same file to display its content.
                entries = json.load(file)
                print(entries)

    def checksame_hash(self):
        # Extract file content to make a list containing hash values,
        # then compares lastest hash with those of list
        with open(self.filename, 'r') as file:
            maybe = json.load(file)
            values = maybe.values()
            list_hash = []
            for x in values:
                for y in x:
                    for z in y.values():
                        list_hash.append(z)
        if self.crypted_password in list_hash:  # if same is active core_function() will loop again, else run() will continue
            print("This password is already in this file. Try another one")
            self.same = True
        else:
            print("Password is not json file. It will now be added to it.")
            self.same = False

# Main class
class Password(JsonHandling):
    def __init__(self):
        self.passwd = ""
        self.tip = "Type your password made of 8 characters, " \
                   "containing at least 1 Digit, 1 upper, 1 lower and 1 special character : "
        # Use string module to create 2 alphabets and numbers
        self.number = list(string.digits)
        self.lower = list(string.ascii_lowercase)
        self.upper = list(string.ascii_uppercase)
        self.spe_character = "!$%&?@"
        # Booleans to trigger some functions
        self.trycounter = False
        self.same = False
        self.filename = 'File.json'

    def makepwd(self):  # Get user input and convert it into str
        self.passwd = str(input(self.tip if not self.trycounter else "Enter a correct password : "))
        if self.trycounter or self.same:
            self.checkpwd()

    def checkpwd(self):
        # Check password length and if user input contains number lower upper and special characters.
        # Nested if checking if password follows requirements, every failure restart makepwd()
        if len(self.passwd) >= 8:
            charlist = list(self.passwd)
            if any(x in self.number for x in charlist):
                if any(x in self.lower for x in charlist):
                    if any(x in self.upper for x in charlist):
                        if any(x in self.spe_character for x in charlist):
                            fstring = "Password is : " + self.passwd
                            print(fstring)
                            if self.trycounter:
                                self.trycounter = False
                        else:
                            print("There is no special character")
                            self.trycounter = True
                            if self.trycounter:
                                self.makepwd()
                    else:
                        print("There is no uppercase")
                        self.trycounter = True
                        if self.trycounter:
                            self.makepwd()
                else:
                    print("There is no lowercase")
                    self.trycounter = True
                    if self.trycounter:
                        self.makepwd()
            else:
                print("There is no number")
                self.trycounter = True
                if self.trycounter:
                    self.makepwd()
        else:
            self.trycounter = True
            if self.trycounter:
                print("Password is too short.")
                self.makepwd()

    def crypt(self):  # Crypt user password with sha256
        self.crypted_password = sha256(self.passwd.encode('utf-8')).hexdigest()
        print("This is your hashed password : " + self.crypted_password)
        a = input("Interpreter is paused so that you may check check_samehash() \n "
                  "Copy hash and replace a value in file.json. Enter anything to continue.")

    def core_function(self):  # function calling other functions.
        self.makepwd()
        self.checkpwd()
        self.crypt()
        self.checksame_hash()

    def run(self):  # performed on an object it starts the program.
        self.core_function()
        if self.same:
            self.core_function()
        self.addtojsonfile()


if __name__ == "__main__":
    app = Password()
    app.run()