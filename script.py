# generate_diary.py
import sqlite3
import random
from datetime import datetime, timedelta

def generate_diary_db(db_path="diary.db", days=90):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS entries")
    cursor.execute("""
        CREATE TABLE entries (
            date TEXT PRIMARY KEY,
            mood INTEGER,
            sleep_hours REAL,
            activity TEXT,
            notes TEXT
        )
    """)

    activities = ["work", "sport", "rest", "party", "learning", "meditation", "gaming", "walk"]
    start_date = datetime(2025, 3, 1)  # произвольная дата

    # Базовые параметры для правдоподобной генерации
    prev_mood = 7
    data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        
        # Сон: обычно 6-9 часов, но зависит от активности накануне
        if i > 0 and data[-1][2] in ["party", "gaming"]:
            sleep = round(random.uniform(4.5, 7.0), 1)
        else:
            sleep = round(random.uniform(6.0, 9.0), 1)
        
        # Настроение: зависит от предыдущего настроения и сна
        mood_change = random.uniform(-1.5, 1.5)
        if sleep < 6:
            mood_change -= 1
        elif sleep > 8:
            mood_change += 0.5
        mood = max(1, min(10, round(prev_mood + mood_change)))
        
        # Выбор активности: не случайно, а чтобы создать паттерны
        if mood <= 3:
            activity = random.choice(["rest", "gaming", "work"])
        elif mood >= 8:
            activity = random.choice(["sport", "walk", "meditation", "party"])
        else:
            activity = random.choice(activities)
        
        notes = f"Day {i+1}: {activity}, slept {sleep}h"
        data.append((current_date.strftime("%Y-%m-%d"), mood, sleep, activity, notes))
        prev_mood = mood
    
    cursor.executemany("INSERT INTO entries VALUES (?,?,?,?,?)", data)
    conn.commit()
    conn.close()
    print(f"Сгенерировано {days} записей в {db_path}")

if __name__ == "__main__":
    generate_diary_db()
