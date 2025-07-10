import streamlit as st
from pages.security_login import *
import time
import pandas as pd

def login_interface():
    #with st.container(border=True):
    with st.expander("⠀", expanded=st.session_state.get('expander_state', True)):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.title("Login")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Username")
        with col3:
            username = st.text_input("Username", key="login_username", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Password")
        with col3:
            password = st.text_input("Password", key="login_password", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
        with col4:
            if st.button("Continue", use_container_width=True):
                st.success("Checking credentials")
                if check_user(username, password):
                    st.success("Logged in successfully!")
                    st.write("By clicking Confirm you agree to the Code of Conduct. utilize the true potential of this amazing Explorer")
                    st.session_state["logged_in"] = True
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    #st.session_state['expander_state'] = False
                    if st.session_state.get("redirect_to_login", False):
                        st.session_state["redirect_to_login"] = False
                        #st.switch_page("pages/Search.py")
                        #time.sleep(2)
                        #st.rerun()
                else:
                    st.error("Invalid username or password")

def register_interface():
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.title("Register")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("First Name")
            fname = st.text_input("FirstName", label_visibility="collapsed")
        with col3:
            st.subheader("Last Name")
            lname = st.text_input("LastName", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Create Username")
        with col3:
            username1 = st.text_input("Username", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Email")
        with col3:
            email1 = st.text_input("Email", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Create Password")
        with col3:
            password1 = st.text_input("Password1", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Confirm Password")
        with col3:
            password2 = st.text_input("Password2", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
        with col4:
            if st.button("Register", use_container_width=True):
                if password1 == password2:
                    st.success("Password checked")
                    if not validate_username(username1):
                        st.error("Invalid username. Only a-z, A-Z, 0-9, and !@#$%^&*_+-/? are allowed.")
                    elif not validate_email(email1):
                        st.error("Invalid email. Must contain @ .com .ac .in ")
                    elif not validate_password(password1):
                        st.error("Password must be at least 8 characters long.")
                    else:
                        if add_user(username1, password1, fname, lname, email1):
                            st.success("Registration successful! Please login.")
                            st.session_state.current_interface='login'
                            st.rerun()
                        else:
                            st.error("Username or email already exists.")
                else:
                    st.warning("Passwords do not match. Please try again.")

def login_page():
    if 'current_interface' not in st.session_state:
        st.session_state.current_interface = None
    st.title("Security")

    if st.session_state.get("logged_in", False) and st.session_state.get("authenticated", False):
        username = st.session_state.get('username')
        details_button = st.expander("⠀", expanded=True)
        col1, col2, col4, col6, col7 = st.columns([1, 2, 1, 2, 1])
        history_button = col2.button("History", key="history_login")
        logout_button = col6.button("Logout", key="logout_login")
        conn2 = connect_to_db()
        cursor2 = conn2.cursor()
        query = "SELECT Username,FirstName, LastName, Email FROM Identity WHERE Username = %s"
        cursor2.execute(query, (username,))
        result = cursor2.fetchone()
        with details_button:
                col1,col2=st.columns(2)
                with col1:
                    st.subheader(f"**Name**: {result[1]} {result[2]}")
                    st.subheader(f"**Username**: {result[0]}")
                with col2:
                    st.subheader(f"**Email**: {result[3]}")
        cursor2.execute("SELECT COUNT(*) FROM History WHERE Username = %s", (username,))
        user_searches = cursor2.fetchone()[0]
        st.subheader(f"**Total Searches** for **{username}**: **{user_searches}**")
        conn2.commit()
        conn2.close()

        if history_button:
            conn2 = connect_to_db()
            cursor2 = conn2.cursor()
            con = st.container(border=True)
            con.write(f"**History** for **{username}** :-")
            cursor2.execute("SELECT * FROM History WHERE Username = %s", (username,))
            rows = cursor2.fetchall()
            column_names = [desc[0] for desc in cursor2.description]
            df = pd.DataFrame(rows, columns=column_names)
            con.dataframe(df, use_container_width=True)
            conn2.close()

        # Handle logout
        if logout_button:
            st.session_state["logged_in"] = False
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.success("You have been logged out successfully!")
            time.sleep(2)
            st.rerun()

    else:
        # User is not logged in, show login and register options
        col1, col2, col4, col6, col7 = st.columns([1, 2, 1, 2, 1])
        login_button = col2.button("Login")
        register_button = col6.button("Register")

        if login_button:
            st.session_state.current_interface = 'login'

        if register_button:
            st.session_state.current_interface = 'register'

        # Show the appropriate interface based on the current state
        if st.session_state.current_interface == 'login':
            login_interface()
            if st.session_state.get("authenticated", False):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
                col4.button("Confirm")
        elif st.session_state.current_interface == 'register':
            register_interface()

if __name__ == "__main__":
    login_page()