# Telegram Bot for Vacancy Statistics
This project is a Telegram bot designed to provide statistics on job vacancies from a robota.ua with keyword "junior". The bot fetches vacancy data, stores it in an SQLite database, and allows users to retrieve and view statistics through a simple command. The bot also generates an Excel file with the statistics for the current day.

Features
 - Fetch Vacancy Data: The bot retrieves the latest job vacancy data from a specified source.
 - Database Storage: Stores vacancy data in an SQLite database with timestamp and change from the previous entry.
 - Statistics Command: Users can request the bot to generate and send an Excel file containing today's statistics using the /get_today_statistic command.
 - Scheduled Data Fetching: The bot periodically fetches and updates the vacancy data to keep the database current.

# Requirements
 - Python 3.8 or higher
 - Required Python packages (listed in requirements.txt):
   - aiogram
   - pandas
   - requests
   - schedule
   - sqlite3

# Project Structure
 - vacancy_parser.py: Main script to run the Telegram bot.
 - config.py: Configuration file containing API token and request data.
 - requirements.txt: List of required Python packages.
 - vacancies.db: SQLite database file to store vacancy data (created automatically).

# Usage
Start the bot:
 - The bot will start fetching vacancy data and storing it in the SQLite database as scheduled.

Get today's statistics:
 - Send the /get_today_statistic command to the bot in Telegram. The bot will respond with an Excel file containing today's statistics.

# To run this project locally:
1) Go to Telegram and find BotFather bot, get your token for bot.
2) Rename file config.py.example to --> config.py and paste your token as API_TOKEN
3) Open terminal and run "pip install -r requirements.txt"
4) Run vacancy_parser.py file and enjoy ;)
