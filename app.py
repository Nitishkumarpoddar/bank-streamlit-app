import streamlit as st
import json
import random
import string
from pathlib import Path

# ---------- DATA FILE ----------
DB = "data.json"

def load_data():
    if Path(DB).exists():
        with open(DB) as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------- HELPERS ----------
def generate_acc():
    digit = random.choices(string.digits, k=4)
    alpha = random.choices(string.ascii_letters, k=4)
    acc = digit + alpha
    random.shuffle(acc)
    return "".join(acc)

def find_user(acc, pin):
    for user in data:
        if user["accountNo"] == acc and user["pin"] == pin:
            return user
    return None


# ---------- UI ----------
st.set_page_config(page_title="Bank System", page_icon="🏦", layout="centered")

st.title("🏦 Bank Management System")
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Create Account",
        "Deposit",
        "Withdraw",
        "Check Details",
        "Update Account",
        "Delete Account",
        "View All Accounts"
    ]
)




# ---------- CREATE ACCOUNT ----------
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", 0, 120)
    pin = st.text_input("Pin", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    if st.button("Create"):
        if age > 18 and len(pin) == 4 and len(phone) == 10:
            acc = generate_acc()
            user = {
                "Name": name.title(),
                "Age": age,
                "pin": int(pin),
                "Email": email,
                "Phone_No": phone,
                "accountNo": acc,
                "Balance": 0
            }
            data.append(user)
            save_data(data)

            st.success("Account Created Successfully")
            st.info(f"Your Account Number: {acc}")

        else:
            st.error("Invalid Details")


# ---------- DEPOSIT ----------
elif menu == "Deposit":
    st.subheader("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")
    amount = st.number_input("Amount", 0)

    if st.button("Deposit"):
        user = find_user(acc, int(pin)) if pin else None
        if user:
            user["Balance"] += amount
            save_data(data)
            st.success("Amount Deposited")
            st.write(user)
        else:
            st.error("User Not Found")


# ---------- WITHDRAW ----------
elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")
    amount = st.number_input("Amount", 0)

    if st.button("Withdraw"):
        user = find_user(acc, int(pin)) if pin else None
        if user:
            if amount < user["Balance"]:
                user["Balance"] -= amount
                save_data(data)
                st.success("Withdrawal Successful")
                st.write(user)
            else:
                st.error("Insufficient Balance")
        else:
            st.error("User Not Found")


# ---------- DETAILS ----------
elif menu == "Check Details":
    st.subheader("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")

    if st.button("Check"):
        user = find_user(acc, int(pin)) if pin else None
        if user:
            st.json(user)
        else:
            st.error("User Not Found")


# ---------- UPDATE ----------
elif menu == "Update Account":
    st.subheader("Update Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")

    if "auth" not in st.session_state:
        st.session_state.auth = None

    if st.button("Verify"):
        user = find_user(acc, int(pin)) if pin else None
        if user:
            st.session_state.auth = user
        else:
            st.error("Invalid Credentials")

    if st.session_state.auth:
        user = st.session_state.auth

        name = st.text_input("Name", user["Name"])
        age = st.text_input("Age", user["Age"])
        email = st.text_input("Email", user["Email"])
        newpin = st.text_input("Pin", type="password")

        if st.button("Update"):
            user["Name"] = name.title()
            user["Age"] = int(age)
            user["Email"] = email
            if newpin:
                user["pin"] = int(newpin)

            save_data(data)
            st.success("Updated Successfully")
            st.session_state.auth = None


# ---------- DELETE ----------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")

    if st.button("Delete"):
        user = find_user(acc, int(pin)) if pin else None
        if user:
            data.remove(user)
            save_data(data)
            st.success("Account Deleted")
        else:
            st.error("User Not Found")


elif menu == "View All Accounts":
    st.subheader("All Bank Accounts Data")

    if data:
        st.success(f"Total Accounts: {len(data)}")
        st.json(data)
    else:
        st.warning("No accounts found")