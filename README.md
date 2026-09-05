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
