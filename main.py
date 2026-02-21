
from pathlib import Path

import json
import random
import string

class Bank:

    database = "data.json"
    data = []
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
                print(data)
        else:
            print("No such file Exits  ------")
    except Exception as err:
        print(f"Error occured {err}")

    @classmethod
    def update(cls):
        with open(cls.database,"w") as fs:
            fs.write(json.dumps(cls.data))
    
    #gernate account number :-
    @staticmethod
    def gernateaccountNo():
        digit = random.choices(string.digits , k=4)
        alpha = random.choices(string.ascii_letters , k=4)
        id = digit + alpha
        random.shuffle(id)
        return " ".join(id)


    #create account 
    def createaccount(self):

        info = {
            "Name" : input("Enter name :- ").title(),
            "Age" : int(input("ENter age :- ")),
            "pin": int(input("Enter pin :- ")),
            "Email":input("enter email :- "),
            "Phone_No": input("Enter your phone number :- "),
            "accountNo" : Bank.gernateaccountNo(),
            "Balance": 0
        }

        if info["Age"] >18 and len(str(info["pin"])) ==4 and len(info["Phone_No"]) ==10 :
            Bank.data.append(info)
            Bank.update()
            print("-----create account successfull ------")
        else:
            print("Credintial are not valid ")
    
    # Deposit money
    def deposit(self):
        name = input("Enter name :- ")
        account_number =input("Enter account number :- ")
        pin = int(input("Enter your pin :- "))
        for i in Bank.data:
            if i["Name"] == name and i["accountNo"] ==account_number and i["pin"] ==pin:
                amount = int(input("Enter amount :- "))
                if amount >0 :
                    i["Balance"] +=amount
                    print("credit successfull ")
                    Bank.update()
                    print(i)
                    break
                else:
                    print("Invlid amount ----")
                    break
        else:
            print("not create account ")
    
    
    #withdraw money
    def withdraw(self):
        name = input("Enter name :- ")
        account_number = input("Enter account number :- ")
        pin = int(input("Enter pin :- "))
        for i in Bank.data:
            if i["Name"] == name and i["accountNo"] ==account_number and i["pin"] ==pin:
                amount = int(input("Enter amount :-  "))
                if amount <i["Balance"] :
                    i["Balance"] -= amount
                    print("debit amount successful ----")
                    Bank.update()
                    print(i)
                    break
                else:
                    print("Check amount -----")
                    break
        else:
            print("not create account ")
    
    #detail 
    def detail(self):
        account_no = input("Enter account number :- ")
        pin = int(input("Enter pin :- "))

        user_data = [i for i in Bank.data if i["accountNo"] == account_no and i["pin"] == pin ]
        if not user_data:
            print("user not found ")
        else:
            print("-----check detail ------")

            for i in user_data[0]:
                print(f"{i} : {user_data[0][i]}")
            return user_data[0]
    
    # update detail
    # def update_detail(self):
    #     user=self.detail()
    #     print(user)

    #     if user == False:
    #         print("not found in data \ncheck detail ")
    #     else:
    #         print("press 1 for update for name ,gmail,phone number:- ")
    #         print("press 2 for update age and pin :- ")
    #         res = int(input("Enter your response :- "))
    #         if res ==1:
    #             name = input("enter what you want to change (name,phone number ,gmail) :- ")
    #             rename= input("Enter  update (name,phone number ,gmail):-  ")

    #             user[name] = rename
    #             Bank.update()
    #             print("update successfull----")
    #         else:
    #             name = input("update pin or age :- ")
    #             rename = int(input("ENter new update name :- "))
    #             user[name] = rename
    #             Bank.update()
    #             print("Update successful -----")
    
    def update_detail(self):
        account_no = input("Enter account number :- ")
        pin = int(input("Enter pin :- "))
        user_data = [i for i in Bank.data if i["accountNo"] == account_no and i["pin"] == pin ]
        if not user_data:
            print("user not found ")
        else:
            print("app account number or balance nahi change kar sakte hai ")
            print("enter your detail to update and press enter to skip them : ")

            new_data = {
            "Name" : input("Enter name :- "),
            "Age" : input("ENter age :- "),
            "pin": input("Enter pin :- "),
            "Email":input("enter email :- ")
            }

            if new_data =="":
                new_data["Name"] = user_data[0]["Name"]
            else:
                user_data[0]["Name"] = new_data["Name"]
            
            if new_data ["Age"] =="":
                new_data["Age"] = user_data[0]["Age"]
            else:
                user_data[0]["Age"] = int(new_data["Age"]) 

            if new_data["Email"] =="":
                new_data["Email"] =user_data[0]["Email"]
            else:
                user_data[0]["Email"] = new_data["Email"] 
            
            if new_data["pin"] =="":
                new_data["pin"] = user_data[0]["pin"]
            else:
                user_data[0]["pin"] = int(new_data["pin"])

            new_data["accountNo"] = user_data[0]["accountNo"]
            new_data["Balance"] = user_data[0]["Balance"]
            
            Bank.update()
            print(user_data)
            print("update successfull -- ")


    
    #delete account 
    def delete(self):
        account_no = input("Enter account number :- ")
        pin = int(input("Enter pin :- "))
        user_data = [i for i in Bank.data if i["accountNo"] == account_no and i["pin"] == pin ]
        if user_data == False:
            print("user not found ")
        else:
            ind = Bank.data.index(user_data[0])
            choice = input("are you sure delete account ? (yes or no ) : - ")
            if choice == "yes":
                Bank.data.pop(ind)
                Bank.update()
                print("delete account successful ---")
            else:
                print("not delete account ---")


obj = Bank()
while True:
    print(" ")
    print("Press 1 for creating accout :- ")
    print("press 2 for deposit money :- ")
    print("Press 3 for withdraw money :- ")
    print("Press 4 for detail account :- ")
    print("press 5 for update account : - ")
    print("press 6 for delete account :- ")
    print("press 0 for exists in bank:- ")

    choice = int(input("Enter your choice :- "))

    if choice == 1:
        obj.createaccount()
    elif choice ==2:
        obj.deposit()
    elif choice ==3:
        obj.withdraw()
    elif choice ==4:
        obj.detail()
    elif choice ==5:
        obj.update_detail()
    elif choice ==6:
        obj.delete()
    elif choice ==0:
        break


# 





















