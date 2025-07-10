import streamlit as st
from backend import user_input_menu, multi_user_input_menu, process_locid, process_mlocid
from pages.footer_all import base_footer
import time
from pages.security_login import connect_to_db
import pandas as pd
from pages.security_login import check_user
import pages as pg

def search_page():
    if st.session_state.get('authenticated', False):
        username = st.session_state.get('username')
    st.title("Search")
    st.write("**Begin the search by interacting with the backend process.**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con1, con2, con3 = st.columns([2, 2, 2])
    with con2:
        start_button = st.button("Search", use_container_width=True, key="Searchbutton1")

    if start_button:
        if not st.session_state.get("logged_in", False):
            if tid or mtid or locid or mlocid:
                st.warning("You need to login to perform this action. Redirecting to login page in 5 seconds...")
                time.sleep(5)
                st.session_state["redirect_to_login"] = True
                st.rerun()
        else:
            conn = connect_to_db()
            cursor = conn.cursor()
            if tid:
                result = user_input_menu(tid)
                st.write(result)
                st.toast("Task completed successfully.")
                query_tid = """
                INSERT INTO History (Username, tid)
                VALUES (%s, %s)
                """
                cursor.execute(query_tid, (username, tid))
            elif mtid:
                result = multi_user_input_menu(mtid)
                st.write(result)
                st.toast("Task completed successfully.")
                query_mtid = """
                INSERT INTO History (Username, mtid)
                VALUES (%s, %s)
                """
                cursor.execute(query_mtid, (username, mtid))
            elif locid:
                tid = process_locid(locid)
                result = user_input_menu(tid)
                st.write(result)
                st.toast("Task completed successfully.")
                query_locid = """
                INSERT INTO History (Username, locid)
                VALUES (%s, %s)
                """
                cursor.execute(query_locid, (username, locid))
            elif mlocid:
                mtid = process_mlocid(mlocid)
                result = multi_user_input_menu(mtid)
                st.write(result)
                st.toast("Task completed successfully.")
                query_mlocid = """
                INSERT INTO History (Username, mlocid)
                VALUES (%s, %s)
                """
                cursor.execute(query_mlocid, (username, mlocid))
            else:
                st.warning("Need either a Gene ID or NCBI ID to proceed.")
            conn.commit()
            conn.close()
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")
    c1,c2,c3,c4=st.columns([2,3,3,2])
    if st.session_state.get('authenticated', False):
        if c2.button("History", key="History_search",use_container_width=True):
            conn2= connect_to_db()
            cursor2= conn2.cursor()
            st.write(f"History for {username} :-")
            cursor2.execute("SELECT * FROM History WHERE Username = %s", (username,))
            rows = cursor2.fetchall()
            column_names = [desc[0] for desc in cursor2.description]
            df = pd.DataFrame(rows, columns=column_names)
            st.dataframe(df)
            conn2.close()
    if st.session_state.get('authenticated', False):
        if c3.button("Logout", key="logout_search",use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.success("You have been logged out successfully!")
            time.sleep(2)
            st.rerun()
    base_footer()

if __name__ == "__main__":
    search_page()
