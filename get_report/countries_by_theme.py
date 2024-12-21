import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_countries_by_theme(root):
    def show_countries_by_theme():
        theme_name = entry_theme.get()

        if not theme_name:
            messagebox.showerror("Ошибка", "Поле 'Тема' обязательно для заполнения")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Ищем уникальные страны для указанной темы
            cursor.execute('''SELECT DISTINCT S.country
                              FROM Stamps S
                              JOIN Series SR ON S.seriesID = SR.seriesID
                              JOIN Themes T ON SR.themeID = T.themeID
                              WHERE T.theme_name = ?''', (theme_name,))

            countries = cursor.fetchall()

            if countries:
                result_text = f"Страны, чьи марки находятся в теме '{theme_name}':\n"
                for country in countries:
                    result_text += f"Страна: {country[0]}\n"
                messagebox.showinfo("Информация", result_text)
            else:
                messagebox.showinfo("Информация", f"В теме '{theme_name}' нет марок")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    search_window = tk.Toplevel(root)
    search_window.title("Поиск стран по теме")

    tk.Label(search_window, text="Тема:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_theme = tk.Entry(search_window)
    entry_theme.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(search_window, text="Показать страны", command=show_countries_by_theme).grid(row=1, column=0, columnspan=2, pady=10)
