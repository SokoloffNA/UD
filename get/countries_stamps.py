import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_countries_in_section(root):
    def find_countries():
        section_str = entry_section.get()

        if not section_str:
            messagebox.showerror("Ошибка", "Номер раздела обязателен для заполнения")
            return

        try:
            section_number = int(section_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат номера раздела")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Запрос для получения стран, чьи марки содержатся в заданном разделе
            cursor.execute('''
                SELECT DISTINCT s.country
                FROM Stamps s
                JOIN StampLocation sl ON s.stampID = sl.stampID
                JOIN Location l ON sl.locationID = l.locationID
                WHERE l.section_number = ?
            ''', (section_number,))

            countries = cursor.fetchall()

            if not countries:
                messagebox.showinfo("Результаты", f"В разделе {section_number} нет марок")
                return

            # Формируем список стран
            country_list = "\n".join([country[0] for country in countries])

            messagebox.showinfo("Страны в разделе", f"Марки следующих стран содержатся в разделе {section_number}:\n\n{country_list}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    countries_window = tk.Toplevel(root)
    countries_window.title("Поиск стран по разделу")

    tk.Label(countries_window, text="Номер раздела:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_section = tk.Entry(countries_window)
    entry_section.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(countries_window, text="Найти страны", command=find_countries).grid(row=1, column=0, columnspan=2, pady=10)
