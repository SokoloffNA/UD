import sqlite3

def connect_db():
    return sqlite3.connect('StampsDB.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Таблица Тем
    cursor.execute('''CREATE TABLE IF NOT EXISTS Themes (
                    themeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    theme_name VARCHAR(50) NOT NULL,
                    is_open BOOLEAN DEFAULT 1
                  )''')

    # Таблица Серий марок
    cursor.execute('''CREATE TABLE IF NOT EXISTS Series (
                    seriesID INTEGER PRIMARY KEY AUTOINCREMENT,
                    themeID INT NOT NULL REFERENCES Themes(themeID),
                    series_name VARCHAR(50) NOT NULL
                  )''')

    # Таблица Марок
    cursor.execute('''CREATE TABLE IF NOT EXISTS Stamps (
                    stampID INTEGER PRIMARY KEY AUTOINCREMENT,
                    stamp_number INT NOT NULL UNIQUE,
                    country VARCHAR(60) NOT NULL,
                    seriesID INT REFERENCES Series(seriesID),
                    year INT,
                    color VARCHAR(50),
                    size VARCHAR(50),
                    price REAL,
                    stamp_theme VARCHAR(50)
                  )''')

    # Таблица местоположения
    cursor.execute('''CREATE TABLE IF NOT EXISTS Location (
                    locationID INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_number INT NOT NULL,
                    volume_number INT NOT NULL,
                    page_number INT NOT NULL,
                    position_on_page INT NOT NULL
                  )''')

    # Привязка марки к местоположению
    cursor.execute('''CREATE TABLE IF NOT EXISTS StampLocation (
                    stampID INT NOT NULL REFERENCES Stamps(stampID) ON DELETE CASCADE,
                    locationID INT NOT NULL REFERENCES Location(locationID),
                    PRIMARY KEY (stampID)
                  )''')

    # Таблица пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user'))
                  )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("База данных успешно создана!")
