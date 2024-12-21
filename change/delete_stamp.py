import tkinter as tk
from tkinter import messagebox
from database import connect_db


def delete_stamps_by_theme(root):
    def delete_stamps():
        theme = entry_theme.get()

        if not theme:
            messagebox.showerror("Ошибка", "Поле 'Тема' обязательно для заполнения")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Находим ID темы по имени
            cursor.execute("SELECT themeID FROM Themes WHERE theme_name = ?", (theme,))
            theme_id = cursor.fetchone()

            if not theme_id:
                messagebox.showerror("Ошибка", "Тема не найдена")
                return
            
            theme_id = theme_id[0]

            # Находим все seriesID для этой темы
            cursor.execute("SELECT seriesID FROM Series WHERE themeID = ?", (theme_id,))
            series_ids = cursor.fetchall()

            if not series_ids:
                messagebox.showerror("Ошибка", "Не найдено серий для этой темы")
                return

            # Для каждого seriesID удаляем марки и их местоположения
            for series_id in series_ids:
                series_id = series_id[0]
                # Удаляем все записи о местоположении марок этой серии
                cursor.execute("DELETE FROM StampLocation WHERE stampID IN (SELECT stampID FROM Stamps WHERE seriesID = ?)", (series_id,))
                
                # Удаляем марки этой серии
                cursor.execute("DELETE FROM Stamps WHERE seriesID = ?", (series_id,))
                
                # Удаляем записи о местоположении, если они больше не используются
                cursor.execute("DELETE FROM Location WHERE locationID NOT IN (SELECT locationID FROM StampLocation)")

            # Опционально: Удалить тему, если больше нет марок для этой темы
            cursor.execute("SELECT COUNT(*) FROM Stamps WHERE seriesID IN (SELECT seriesID FROM Series WHERE themeID = ?)", (theme_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM Themes WHERE themeID = ?", (theme_id,))

            # Опционально: Удалить серию, если она больше не используется
            cursor.execute("SELECT COUNT(*) FROM Stamps WHERE seriesID = ?", (series_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM Series WHERE seriesID = ?", (series_id,))

            conn.commit()
            messagebox.showinfo("Успех", "Марки успешно удалены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()
            delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Удаление марок по теме")

    tk.Label(delete_window, text="Тема:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_theme = tk.Entry(delete_window)
    entry_theme.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(delete_window, text="Удалить марки", command=delete_stamps).grid(row=1, column=0, columnspan=2, pady=10)
