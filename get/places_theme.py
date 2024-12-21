import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_stamp_locations_by_theme(root):
    def show_locations():
        theme_name = entry_theme_name.get()

        if not theme_name:
            messagebox.showerror("Ошибка", "Введите название темы")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Получаем themeID по названию темы
            cursor.execute("SELECT themeID FROM Themes WHERE theme_name = ?", (theme_name,))
            theme = cursor.fetchone()
            if theme is None:
                messagebox.showerror("Ошибка", f"Тема '{theme_name}' не найдена")
                return

            theme_id = theme[0]

            # Находим все серии, относящиеся к данной теме
            cursor.execute("SELECT seriesID FROM Series WHERE themeID = ?", (theme_id,))
            series_ids = cursor.fetchall()

            if not series_ids:
                messagebox.showinfo("Информация", "Нет серий для этой темы")
                return

            all_locations = []

            # Для каждой серии находим все марки и их местоположения
            for series_id in series_ids:
                cursor.execute("SELECT stamp_number FROM Stamps WHERE seriesID = ?", (series_id[0],))
                stamp_numbers = cursor.fetchall()

                for stamp_number in stamp_numbers:
                    # Получаем местоположение марки по её номеру
                    cursor.execute('''SELECT section_number, volume_number, page_number, position_on_page
                                      FROM Location
                                      WHERE locationID IN (SELECT locationID FROM StampLocation WHERE stampID = 
                                      (SELECT stampID FROM Stamps WHERE stamp_number = ?))''', 
                                   (stamp_number[0],))
                    location = cursor.fetchone()
                    if location:
                        all_locations.append((stamp_number[0], location))

            if not all_locations:
                messagebox.showinfo("Информация", "Марки не найдены в коллекции для данной темы")
                return

            result_text = "Местоположения марок в теме '{}':\n\n".format(theme_name)
            for stamp_number, location in all_locations:
                result_text += f"Марка №{stamp_number} - Раздел: {location[0]}, Том: {location[1]}, Страница: {location[2]}, Позиция: {location[3]}\n"

            messagebox.showinfo("Информация", result_text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    search_window = tk.Toplevel(root)
    search_window.title("Поиск местоположений марок по теме")

    tk.Label(search_window, text="Название темы:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_theme_name = tk.Entry(search_window)
    entry_theme_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(search_window, text="Показать местоположения", command=show_locations).grid(row=1, column=0, columnspan=2, pady=10)
