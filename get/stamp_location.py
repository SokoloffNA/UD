import tkinter as tk
from tkinter import messagebox
from database import connect_db


def get_stamp_by_location(root):
    def show_stamp_by_location():
        section = entry_section.get()
        volume = entry_volume.get()
        page = entry_page.get()
        position = entry_position.get()

        if not section or not volume or not page or not position:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return

        try:
            section = int(section)
            volume = int(volume)
            page = int(page)
            position = int(position)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных (проверьте числа)")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Ищем марку по местоположению
            cursor.execute('''SELECT S.country, S.stamp_number, L.section_number, L.volume_number, 
                                      L.page_number, L.position_on_page
                              FROM Stamps S
                              JOIN StampLocation SL ON S.stampID = SL.stampID
                              JOIN Location L ON SL.locationID = L.locationID
                              WHERE L.section_number = ? AND L.volume_number = ? 
                                    AND L.page_number = ? AND L.position_on_page = ?''',
                           (section, volume, page, position))

            result = cursor.fetchone()

            if result:
                country, stamp_number, section, volume, page, position = result
                result_text = f"Марка номер {stamp_number} из страны {country} находится в следующем месте:\n"
                result_text += f"Раздел: {section}, Том: {volume}, Страница: {page}, Позиция: {position}"
                messagebox.showinfo("Информация", result_text)
            else:
                messagebox.showinfo("Информация", "Марка не найдена в указанном месте")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    search_window = tk.Toplevel(root)
    search_window.title("Поиск марки по местоположению")

    tk.Label(search_window, text="Раздел:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_section = tk.Entry(search_window)
    entry_section.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(search_window, text="Том:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_volume = tk.Entry(search_window)
    entry_volume.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(search_window, text="Страница:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    entry_page = tk.Entry(search_window)
    entry_page.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(search_window, text="Позиция на странице:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    entry_position = tk.Entry(search_window)
    entry_position.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(search_window, text="Показать марку", command=show_stamp_by_location).grid(row=4, column=0, columnspan=2, pady=10)
