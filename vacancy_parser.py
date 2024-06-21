import asyncio
import sqlite3
from datetime import datetime

import pandas as pd
import requests
import schedule
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from config import *

# Here you should place your token for the bot
# For this bot we importing token from config.py file
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def get_today_statistics():
    """
    This function retrieves today's statistics from the database.

    Returns:
        list: A list of tuples containing the ID, timestamp, vacancy count, and change for each row.
    """

    conn = sqlite3.connect("vacancies.db")
    cursor = conn.cursor()

    today_date = datetime.now().date()
    cursor.execute(
        "SELECT timestamp, vacancy_count, change FROM vacancies WHERE DATE(timestamp) = ?",
        (today_date,),
    )
    rows = cursor.fetchall()
    conn.close()

    return rows


def create_excel_file(data):
    """
    This function creates an Excel file with the provided data.

    Args:
        data (list): A list of tuples containing the ID, timestamp, vacancy count, and change.

    Returns:
        str: The name of the created Excel file.
    """

    df = pd.DataFrame(data, columns=["Timestamp", "Vacancy Count", "Change"])
    file_name = "today_statistics.xlsx"
    df.to_excel(file_name, index=False)
    return file_name


@dp.message(Command("get_today_statistic"))
async def send_statistics(message: types.Message):
    """
    This function sends today's statistics as an Excel file to the user.
    Args:
        message (types.Message): The command from the user "/get_today_statistic" from bot.
    """

    data = get_today_statistics()
    if not data:
        await message.answer("We don't have statistics for today yet, try later ;)")
        return

    file_name = create_excel_file(data)

    await message.answer_document(
        document=FSInputFile(file_name), caption="Statistics for today"
    )


def get_vacancies_count():
    """
    This function retrieves the count of published vacancies from the API.
    It sends a POST request to the specified URL with the provided headers and data (robota.ua with keyword "junior").
    If an error occurs, it returns 0 as the count.

    Returns:
        int: The count of published vacancies.
    """

    url = "https://dracula.robota.ua/?q=getPublishedVacanciesList"
    headers = {
        "Content-Type": "application/json",
    }
    # For this request we importing DATA_FOR_REQUEST from config.py file
    # To make code more readable, because DATA_FOR_REQUEST - is big
    data = DATA_FOR_REQUEST

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        data = response.json()
        vacancies_count = data["data"]["publishedVacancies"]["totalCount"]

    except Exception as e:
        print(f"An error occurred: {e}")
        vacancies_count = 0

    return vacancies_count


def save_to_db(vacancies_count):
    """
    This function saves the count of published vacancies to the database SQLite.
    It creates a new table called "vacancies" if it doesn't exist, with columns for ID, timestamp, vacancy count, and change.
    It then inserts a new row with the current timestamp, vacancy count, and change (calculated from the last record).
    If there are no previous records, the change is set to 0.

    Args:
        vacancies_count (int): The count of published vacancies.
    """

    conn = sqlite3.connect("vacancies.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            vacancy_count INTEGER,
            change INTEGER
        )
    """
    )

    cursor.execute(
        "SELECT vacancy_count FROM vacancies ORDER BY timestamp DESC LIMIT 1"
    )
    last_record = cursor.fetchone()

    if last_record:
        last_count = last_record[0]
        change = vacancies_count - last_count
    else:
        change = 0

    cursor.execute(
        "INSERT INTO vacancies (vacancy_count, change) VALUES (?, ?)",
        (vacancies_count, change),
    )
    conn.commit()
    conn.close()
    print(f"Vacancies count: {vacancies_count} saved to database. Change: {change}")


def job():
    count = get_vacancies_count()
    save_to_db(count)


async def scheduler():
    """
    This function sets up a schedule to run the `job` function every hour.
    """
    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
