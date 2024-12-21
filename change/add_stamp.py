import tkinter as tk
from tkinter import messagebox
from database import connect_db
import random


def add_stamp(root):
    def save_mark():
        country = entry_country.get()
        series = entry_series.get()
        year_str = entry_year.get()
        color = entry_color.get()
        size = entry_size.get()
        price_str = entry_price.get()
        theme = entry_theme.get()
        
        section_str = entry_section.get()
        volume_str = entry_volume.get()
        page_str = entry_page.get()
        position_str = entry_position.get()

        if not country or not theme or not section_str or not volume_str or not page_str or not position_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return

        try:
            year = int(year_str) if year_str else None
            price = float(price_str) if price_str else None
            section = int(section_str)
            volume = int(volume_str)
            page = int(page_str)
            position = int(position_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных (проверьте числа)")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            # Проверка или добавление темы
            cursor.execute("SELECT themeID FROM Themes WHERE theme_name = ?", (theme,))
            theme_id = cursor.fetchone()
            if theme_id:
                theme_id = theme_id[0]
            else:
                cursor.execute("INSERT INTO Themes (theme_name) VALUES (?)", (theme,))
                theme_id = cursor.lastrowid

            # Проверка или добавление серии
            cursor.execute("SELECT seriesID FROM Series WHERE series_name = ? AND themeID = ?", (series, theme_id))
            series_id = cursor.fetchone()
            if series_id:
                series_id = series_id[0]
            else:
                cursor.execute("INSERT INTO Series (themeID, series_name) VALUES (?, ?)", (theme_id, series))
                series_id = cursor.lastrowid

            # Уникальный номер марки
            stamp_number = random.randint(1, 999999)

            # Добавление марки
            cursor.execute('''INSERT INTO Stamps (stamp_number, country, seriesID, year, color, size, price, stamp_theme)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (stamp_number, country, series_id, year, color, size, price, theme))
            stamp_id = cursor.lastrowid

            # Добавление местоположения
            cursor.execute('''INSERT INTO Location (section_number, volume_number, page_number, position_on_page)
                              VALUES (?, ?, ?, ?)''', 
                           (section, volume, page, position))
            location_id = cursor.lastrowid

            # Связываем марку с местоположением
            cursor.execute('''INSERT INTO StampLocation (stampID, locationID) VALUES (?, ?)''', 
                           (stamp_id, location_id))

            conn.commit()
            messagebox.showinfo("Успех", f"Марка успешно добавлена с номером {stamp_number}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()
            stamp_window.destroy()

    stamp_window = tk.Toplevel(root)
    stamp_window.title("Добавление марки новой темы")

    tk.Label(stamp_window, text="Страна:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_country = tk.Entry(stamp_window)
    entry_country.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Серия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_series = tk.Entry(stamp_window)
    entry_series.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    entry_year = tk.Entry(stamp_window)
    entry_year.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Цвет:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    entry_color = tk.Entry(stamp_window)
    entry_color.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Размер:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    entry_size = tk.Entry(stamp_window)
    entry_size.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Цена:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
    entry_price = tk.Entry(stamp_window)
    entry_price.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Новая тема:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
    entry_theme = tk.Entry(stamp_window)
    entry_theme.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Раздел:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
    entry_section = tk.Entry(stamp_window)
    entry_section.grid(row=7, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Том:").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    entry_volume = tk.Entry(stamp_window)
    entry_volume.grid(row=8, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Страница:").grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
    entry_page = tk.Entry(stamp_window)
    entry_page.grid(row=9, column=1, padx=5, pady=5)

    tk.Label(stamp_window, text="Позиция на странице:").grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
    entry_position = tk.Entry(stamp_window)
    entry_position.grid(row=10, column=1, padx=5, pady=5)

    tk.Button(stamp_window, text="Сохранить", command=save_mark).grid(row=11, column=0, columnspan=2, pady=10)
