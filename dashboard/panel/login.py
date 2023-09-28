import streamlit as st


class Login:
    user_credentials = {
        "Pouya": "password123",
        "user456": "password456",
    }

    role = {
        'Pouya': 'specialist',
    }

    @staticmethod
    def run():
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
                st.write("Welcome, " + username)
                return Login.role[username], username.title()
            else:
                st.error("Invalid Username or Password")
        return None, None
