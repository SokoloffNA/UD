import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_themes_by_stamp_size(root):
    def show_themes_by_size():
        size = entry_size.get()

        if not size:
            messagebox.showerror("Ошибка", "Поле 'Размер' обязательно для заполнения")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Ищем seriesID для всех марок с указанным размером
            cursor.execute('''SELECT DISTINCT S.seriesID, T.theme_name
                              FROM Stamps S
                              JOIN Series SR ON S.seriesID = SR.seriesID
                              JOIN Themes T ON SR.themeID = T.themeID
                              WHERE S.size = ?''', (size,))

            themes = cursor.fetchall()

            if themes:
                unique_themes = set(theme[1] for theme in themes)
                
                result_text = f"Темы серий, включающих марки с размером '{size}':\n"
                for theme in unique_themes:
                    result_text += f"Тема: {theme}\n"
                messagebox.showinfo("Информация", result_text)
            else:
                messagebox.showinfo("Информация", f"Марки с размером '{size}' не найдены в коллекции")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    search_window = tk.Toplevel(root)
    search_window.title("Поиск тем по размеру марки")

    tk.Label(search_window, text="Размер:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_size = tk.Entry(search_window)
    entry_size.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(search_window, text="Показать темы", command=show_themes_by_size).grid(row=1, column=0, columnspan=2, pady=10)
