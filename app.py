import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import simulated_bots as bots

DB = "sales_ai.db"

# --------------------- DB Helpers ---------------------
def register_user(email, name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, name, stage, reg_date) VALUES (?,?,?,?)", 
                  (email, name, "cold_called", datetime.now().isoformat()))
        uid = c.lastrowid
        conn.commit()
        return uid, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

def find_user_by_email(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, email, name, stage, reg_date FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return row

def get_user_booking(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT slot_date, slot_time, status FROM bookings WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"slot_date": row[0], "slot_time": row[1], "status": row[2]}
    return None

def get_all_users():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

def get_all_calls():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM calls ORDER BY id DESC", conn)
    conn.close()
    return df

def get_all_events():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM events ORDER BY id DESC", conn)
    conn.close()
    return df

def get_all_bookings():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM bookings ORDER BY id DESC", conn)
    conn.close()
    return df

def get_user_calls(user_id):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT bot, transcript, call_time FROM calls WHERE user_id=? ORDER BY id ASC", conn, params=(user_id,))
    conn.close()
    return df

# --------------------- Role Selection ---------------------
if "role" not in st.session_state:
    st.session_state["role"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["role"] is None:
    st.title("Welcome to DealStream.AI")
    st.subheader("Please select your role")
    if st.button("I am a User"):
        st.session_state["role"] = "user"
        st.rerun()
    if st.button("I am an Admin"):
        st.session_state["role"] = "admin"
        st.rerun()
    st.stop()

# --------------------- Sidebar ---------------------
if st.session_state["role"] == "user":
    menu = st.sidebar.radio("User Menu", ["Portal", "Booking & Payment", "Reminders & Calendar", "Settings", "Logout"])
elif st.session_state["role"] == "admin":
    menu = st.sidebar.radio("Admin Menu", ["Admin Dashboard", "All Calls", "All Events", "All Bookings", "Settings", "Logout"])

# --------------------- Logout ---------------------
if menu == "Logout":
    st.session_state["role"] = None
    st.session_state["user"] = None
    st.rerun()

# --------------------- Settings ---------------------
if menu == "Settings":
    st.header("Settings")
    st.info("API key is loaded securely from the environment.")

# --------------------- User Portal ---------------------
if st.session_state["role"] == "user" and menu == "Portal":
    st.header("User Portal — Interactive Sales Flow")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Register")
        reg_email = st.text_input("Email for registration", key="reg_email")
        reg_name = st.text_input("Name", key="reg_name")
        if st.button("Register"):
            uid, err = register_user(reg_email, reg_name)
            if uid:
                st.success(f"Registered user id={uid}")
                st.session_state['user'] = {"id": uid, "email": reg_email, "name": reg_name, "stage": "cold_called", "reg_date": datetime.now().isoformat()}
                cold = bots.cold_caller(uid, reg_name)
                bots.save_message(uid, "cold caller", cold['transcript'])
            else:
                st.error(f"Registration failed: {err}")

    with col2:
        st.subheader("Login")
        login_email = st.text_input("Email to login", key="login_email")
        if st.button("Login"):
            user = find_user_by_email(login_email)
            if user:
                st.success(f"Logged in as {user[2] or user[1]} (id={user[0]})")
                st.session_state['user'] = {"id": user[0], "email": user[1], "name": user[2], "stage": user[3], "reg_date": user[4]}
            else:
                st.error("User not found. Please register first.")

    if st.session_state["user"]:
        user = st.session_state["user"]
        booking = get_user_booking(user['id'])

        st.markdown("---")
        st.subheader("Your Details")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Stage:** {user['stage']}")
        st.write(f"**Registration Date:** {user['reg_date']}")
        st.write(f"**Assigned Bot:** Cold Caller")
        if booking:
            st.success(f"📅 Decision call scheduled for {booking['slot_date']} at {booking['slot_time']} (Status: {booking['status']})")

        st.markdown("### Conversation History")
        history_df = get_user_calls(user['id'])
        for _, row in history_df.iterrows():
            color = "black"
            if row['bot'].lower() == "user":
                st.markdown(f"<div style='background:#DCF8C6;padding:8px;border-radius:5px;margin:5px 0;color:{color}'><b>You:</b> {row['transcript']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#F1F0F0;padding:8px;border-radius:5px;margin:5px 0;color:{color}'><b>{row['bot'].title()}:</b> {row['transcript']}</div>", unsafe_allow_html=True)

        user_msg = st.text_input("Type your message...")
        if st.button("Send"):
            if user_msg.strip():
                bots.save_message(user['id'], "user", user_msg)

                if user['stage'] == "cold_called":
                    reply = bots.lead_caller(user['id'], user['name'], user_msg)
                    bots.save_message(user['id'], "lead caller", reply['transcript'])
                    user['stage'] = "lead_called"
                    bots.update_stage(user['id'], "lead_called")

                elif user['stage'] == "lead_called":
                    reply = bots.decision_caller(user['id'], user['name'], user_msg)
                    bots.save_message(user['id'], "decision caller", reply['transcript'])
                    user['stage'] = "decision_done"
                    bots.update_stage(user['id'], "decision_done")

                st.rerun()

# --------------------- Booking ---------------------
if st.session_state["role"] == "user" and menu == "Booking & Payment":
    st.header("Booking slots & Payment")
    today = pd.Timestamp.today().date()
    slots = [{"date": (today + pd.Timedelta(days=i)).isoformat(), "time": f"{9+i}:00"} for i in range(5)]
    st.table(slots)
    st.info("Payment integration pending.")

# --------------------- Reminders ---------------------
if st.session_state["role"] == "user" and menu == "Reminders & Calendar":
    st.header("Reminders & Calendar")
    st.date_input("Select date")
    st.text_input("Preferred time (e.g., 15:30)")
    st.text_area("Reminder note (optional)")
    if st.button("Create Reminder"):
        st.success("Reminder created.")

# --------------------- Admin Dashboard ---------------------
if st.session_state["role"] == "admin" and menu == "Admin Dashboard":
    st.header("Admin Dashboard")
    st.subheader("Users")
    st.dataframe(get_all_users())
    st.subheader("Bookings")
    st.dataframe(get_all_bookings())

# --------------------- Admin: Calls ---------------------
if st.session_state["role"] == "admin" and menu == "All Calls":
    st.header("All Calls")
    st.dataframe(get_all_calls())

# --------------------- Admin: Events ---------------------
if st.session_state["role"] == "admin" and menu == "All Events":
    st.header("All Events")
    st.dataframe(get_all_events())

# --------------------- Admin: Bookings ---------------------
if st.session_state["role"] == "admin" and menu == "All Bookings":
    st.header("All Bookings")
    st.dataframe(get_all_bookings())
