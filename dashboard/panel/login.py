import streamlit as st
from dashboard.storage.role import Role


class Login:
    user_credentials = {
        "Pouya": "1234",
        "user456": "password456",
    }

    role = {
        'Pouya': Role.User,
    }

    def __init__(self):
        self.username = None

    def activate(self):
        """Return Role and Username"""
        print("Initiating Login Page...")

        st.title("Login Page")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        row = st.columns(4)
        # Login button
        if row[0].button("Login"):
            if username in Login.user_credentials and Login.user_credentials[username] == password:
                st.success("Login Successful!")
                self.username = username
                st.experimental_rerun()
            else:
                st.error("Invalid Username or Password")

    def get_user(self):
        if self.username is None:
            return None, None
        return self.role[self.username], self.username.title()

    def logout(self):
        self.username = None
