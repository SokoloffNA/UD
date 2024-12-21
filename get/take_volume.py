import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_volume_by_series(root):
    def show_volume_by_series():
        series_name = entry_series_name.get()

        if not series_name:
            messagebox.showerror("Ошибка", "Поле 'Серия' обязательно для заполнения")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Ищем seriesID по названию серии
            cursor.execute("SELECT seriesID FROM Series WHERE series_name = ?", (series_name,))
            series_result = cursor.fetchone()

            if not series_result:
                messagebox.showerror("Ошибка", "Серия не найдена")
                return

            series_id = series_result[0]

            # Ищем все тома, в которых находятся марки этой серии
            cursor.execute('''SELECT DISTINCT L.volume_number
                              FROM Stamps S
                              JOIN StampLocation SL ON S.stampID = SL.stampID
                              JOIN Location L ON SL.locationID = L.locationID
                              WHERE S.seriesID = ?''', (series_id,))

            volumes = cursor.fetchall()

            if volumes:
                result_text = f"Серия '{series_name}' содержится в следующих томах:\n"
                for volume in volumes:
                    result_text += f"Том {volume[0]}\n"
                messagebox.showinfo("Информация", result_text)
            else:
                messagebox.showinfo("Информация", "Марки этой серии не найдены в коллекции")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    search_window = tk.Toplevel(root)
    search_window.title("Поиск томов по серии")

    tk.Label(search_window, text="Серия:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_series_name = tk.Entry(search_window)
    entry_series_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(search_window, text="Показать тома", command=show_volume_by_series).grid(row=1, column=0, columnspan=2, pady=10)
