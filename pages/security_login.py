import pymysql
import streamlit as st
import re

def initialize_database():
    try:
        mysql_config = st.secrets["mysql"]
        host = mysql_config["host"]
        user = mysql_config["user"]
        password = mysql_config["password"]
        port = mysql_config["port"]
        db = "Chickpea"

        mydb = pymysql.connect(host=host,user=user,password=password,port=port,ssl={"ssl_disabled": True})
        mycursor = mydb.cursor()

        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        mydb.commit()
        mycursor.execute(f"USE {db}")

        query1 = """
        CREATE TABLE IF NOT EXISTS Authentication (
            SNo INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(20) NOT NULL UNIQUE,
            Password VARCHAR(255) NOT NULL
        )
        """
        mycursor.execute(query1)
        mydb.commit()

        query2 = """
        CREATE TABLE IF NOT EXISTS Identity (
            Username VARCHAR(20) PRIMARY KEY,
            FirstName VARCHAR(30) NOT NULL,
            LastName VARCHAR(30),
            Email VARCHAR(255) NOT NULL UNIQUE,
            FOREIGN KEY (Username) REFERENCES Authentication(Username)
        )
        """
        mycursor.execute(query2)
        mydb.commit()

        query3 = """
        CREATE TABLE IF NOT EXISTS History (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(20) NOT NULL,
            tid VARCHAR(20),
            mtid VARCHAR(255),
            locid VARCHAR(20),
            mlocid VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Username) REFERENCES Authentication(Username)
        )
        """
        mycursor.execute(query3)
        mydb.commit()

        query4 = """
        CREATE TABLE IF NOT EXISTS Visitor (
            Visitor_number INT AUTO_INCREMENT PRIMARY KEY,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mycursor.execute(query4)
        mydb.commit()
        st.success(f"Database '{db}' and tables created successfully.")
        return mydb, mycursor

    except pymysql.Error as e:
        st.error(f"Error: {e}")
        return None, None

# Function to check if a user exists in the Authentication table
def check_user(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Authentication WHERE Username = %s AND Password = %s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to add a new user to the Authentication and Identity tables
def add_user(username, password, first_name, last_name, email):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Authentication (Username, Password) VALUES (%s, %s)", (username, password))
        cursor.execute("INSERT INTO Identity (Username, FirstName, LastName, Email) VALUES (%s, %s, %s, %s)", (username, first_name, last_name, email))
        conn.commit()
        conn.close()
        return True
    except pymysql.Error as e:
        st.error(f"Error: {e}")
        conn.close()
        return False

# Function to validate email
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Function to validate username
def validate_username(username):
    pattern = r"^[a-zA-Z0-9!@#$%^&*_+\-\/?]{1,20}$"
    return re.match(pattern, username) is not None

# Function to validate password length
def validate_password(password):
    return len(password) >= 8

# Function to connect to the database
def connect_to_db():
    mysql_config = st.secrets["mysql"]
    return pymysql.connect(host=mysql_config["host"],user=mysql_config["user"],password=mysql_config["password"],port=mysql_config["port"],database="Chickpea",ssl={"ssl_disabled": True})

def basic_stats():
    conn3 = connect_to_db()
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT COUNT(*) FROM Authentication")
    total_members = cursor3.fetchone()[0]
    #st.sidebar.subheader(f"Total Members : {total_members}")    #change

    cursor3.execute("SELECT COUNT(*) FROM History")
    total_searches = cursor3.fetchone()[0]
    #st.sidebar.subheader(f"Total Searches : {total_searches}")  #change

    conn3.commit()
    conn3.close()
    return total_members, total_searches

def update_visitor_count():
    conn4 = connect_to_db()
    cursor4 = conn4.cursor()
    if st.session_state.get("first_access",False):
        if st.session_state.current_page !="HOME":
            query = "INSERT INTO Visitor (Timestamp) VALUES (NOW())"
            cursor4.execute(query)
            conn4.commit()
            st.session_state.first_access = False

    query = "SELECT COUNT(*) FROM Visitor"
    cursor4.execute(query)
    result = cursor4.fetchone()
    conn4.close()
    return result[0]

# Streamlit app
def security_login():
    st.title("Login and Registration")

    # Initialize database and tables
    if "db_initialized" not in st.session_state:
        st.session_state.mydb, st.session_state.mycursor = initialize_database()
        if st.session_state.mydb and st.session_state.mycursor:
            st.session_state.db_initialized = True

    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        choice = st.radio("Choose an option", ["Login", "Register"])

        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if check_user(username, password):
                    st.session_state['authenticated'] = True
                    st.success("Logged in successfully!")
                    st.title(f"Welcome user")
                    conn = connect_to_db()
                    cursor = conn.cursor()
                    #main part to confirm
                    query5 = "SELECT FirstName FROM Identity WHERE Username = %s"
                    cursor.execute(query5, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                    query6 = "SELECT LastName FROM Identity WHERE Username = %s"
                    cursor.execute(query6, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                    query7 = "SELECT Email FROM Identity WHERE Username = %s"
                    cursor.execute(query7, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                else:
                    st.error("Invalid username or password")

        elif choice == "Register":
            st.subheader("Register")
            username = st.text_input("Username (max 20 chars, allowed: a-z, A-Z, 0-9, !@#$%^&*_+-/?)")
            password = st.text_input("Password (min 8 chars)", type="password")
            first_name = st.text_input("First Name (max 30 chars)")
            last_name = st.text_input("Last Name (max 30 chars, optional)", "")
            email = st.text_input("Email")

            if st.button("Register"):
                if not validate_username(username):
                    st.error("Invalid username. Only a-z, A-Z, 0-9, and !@#$%^&*_+-/? are allowed.")
                elif not validate_email(email):
                    st.error("Invalid email. Must contain @ and .com.")
                elif not validate_password(password):
                    st.error("Password must be at least 8 characters long.")
                else:
                    if add_user(username, password, first_name, last_name, email):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists.")

    else:
        st.subheader("Search Page")
        st.write("Welcome to the Search Page!")

if __name__ == "__main__":
    security_login()
