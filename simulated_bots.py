import sqlite3
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DB = "sales_ai.db"

# Load API key securely from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def update_stage(user_id, stage):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE users SET stage=? WHERE id=?", (stage, user_id))
    conn.commit()
    conn.close()


def save_message(user_id, role, text):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO calls (user_id, bot, transcript, outcome, call_time) VALUES (?,?,?,?,?)",
        (user_id, role, text, "", datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def cold_caller(user_id, name):
    prompt = f"Call the user named {name} and greet them warmly. Introduce yourself as a sales representative and explain our product in a conversational way."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly sales cold caller."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"transcript": completion.choices[0].message.content}


def lead_caller(user_id, name, user_msg):
    prompt = f"The user named {name} said: '{user_msg}'. As a lead caller, answer any doubts about the product in a helpful, professional tone."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful sales lead caller."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"transcript": completion.choices[0].message.content}


def decision_caller(user_id, name, user_msg):
    prompt = f"The user named {name} said: '{user_msg}'. As a decision caller, close the deal and confirm their preferred time slot."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a persuasive decision caller."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"transcript": completion.choices[0].message.content}


def detect_interest(user_msg):
    msg_lower = user_msg.lower()
    if "yes" in msg_lower or "interested" in msg_lower:
        return "interested"
    return "not interested"
