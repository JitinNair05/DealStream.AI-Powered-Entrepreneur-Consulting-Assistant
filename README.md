# DealStream AI – AI-Powered Entrepreneur Consulting Assistant

DealStream AI is a hackathon project that demonstrates an AI-powered workflow for interacting with potential entrepreneurs/leads and assisting with early-stage business consulting.

The application uses OpenAI-powered agents to guide users through different stages of the interaction, while SQLite stores user information and conversation history.

## Features

- AI-powered conversational workflow using the OpenAI API
- Multi-stage lead interaction:
  - Cold Caller
  - Lead Caller
  - Decision Caller
- Automatic progression of users through conversation stages
- Persistent conversation history using SQLite
- User and Admin interfaces
- Admin dashboard for viewing users, calls, events, and bookings
- Appointment/booking slot demonstration
- Streamlit-based interactive interface
- Secure API key management using environment variables

## Technologies Used

- Python
- Streamlit
- OpenAI API
- SQLite
- Pandas
- python-dotenv

## Project Structure

```text
DealStream.AI-Powered-Entrepreneur-Consulting-Assistant/
│
├── app.py                  # Main Streamlit application
├── simulated_bots.py       # AI conversation and lead-stage logic
├── create_tables.py        # SQLite database initialization
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment configuration
├── .gitignore              # Files excluded from Git
└── README.md               # Project documentation
```

## How It Works

1. A user registers through the application.
2. The application starts the initial cold-calling stage.
3. User responses are processed using the OpenAI API.
4. The conversation can progress through lead and decision stages.
5. Conversation messages and user information are stored in SQLite.
6. The Admin interface provides an overview of stored users, calls, events, and bookings.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/JitinNair05/DealStream.AI-Powered-Entrepreneur-Consulting-Assistant.git
cd DealStream.AI-Powered-Entrepreneur-Consulting-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the OpenAI API Key

Create a `.env` file in the project directory:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Initialize the Database

```bash
python create_tables.py
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Security

The OpenAI API key is loaded through an environment variable using `python-dotenv`.

Sensitive files such as `.env` and local database files are excluded from version control.

## Current Scope

This repository demonstrates the core AI conversation, lead-stage management, database persistence, booking interface, and administrative dashboard.

Payment processing and external calendar/reminder integrations are currently placeholders/demo functionality.

## Project Type

Hackathon Project

## Author

Jitin R. Nair
