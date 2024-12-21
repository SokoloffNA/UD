import tkinter as tk
from tkinter import messagebox
from database import connect_db


def update_stamp_location(root):
    def update_location():

        stamp_number_str = entry_stamp_number.get()
        section_str = entry_section.get()
        volume_str = entry_volume.get()
        page_str = entry_page.get()
        position_str = entry_position.get()

        if not stamp_number_str or not section_str or not volume_str or not page_str or not position_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return

        try:
            stamp_number = int(stamp_number_str)
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

            # Проверяем, существует ли марка с данным stamp_number
            cursor.execute("SELECT * FROM Stamps WHERE stamp_number = ?", (stamp_number,))
            stamp = cursor.fetchone()
            if stamp is None:
                messagebox.showerror("Ошибка", f"Марка с номером {stamp_number} не найдена")
                return

            stamp_id = stamp[0]  # Получаем stampID из результата запроса

            # Находим существующее местоположение марки
            cursor.execute("SELECT locationID FROM StampLocation WHERE stampID = ?", (stamp_id,))
            location = cursor.fetchone()
            if location is None:
                messagebox.showerror("Ошибка", "Местоположение марки не найдено")
                return

            location_id = location[0]

            # Обновляем данные в таблице Location
            cursor.execute('''UPDATE Location 
                              SET section_number = ?, volume_number = ?, page_number = ?, position_on_page = ? 
                              WHERE locationID = ?''', 
                           (section, volume, page, position, location_id))

            # Обновляем запись в таблице StampLocation
            cursor.execute('''UPDATE StampLocation 
                              SET locationID = ? 
                              WHERE stampID = ?''', 
                           (location_id, stamp_id))

            conn.commit()
            messagebox.showinfo("Успех", "Местоположение марки успешно обновлено")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()
            update_window.destroy()

    update_window = tk.Toplevel(root)
    update_window.title("Изменение места расположения марки")

    tk.Label(update_window, text="Номер марки:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_stamp_number = tk.Entry(update_window)
    entry_stamp_number.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Раздел:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_section = tk.Entry(update_window)
    entry_section.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Том:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    entry_volume = tk.Entry(update_window)
    entry_volume.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Страница:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    entry_page = tk.Entry(update_window)
    entry_page.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Позиция на странице:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    entry_position = tk.Entry(update_window)
    entry_position.grid(row=4, column=1, padx=5, pady=5)

    tk.Button(update_window, text="Обновить местоположение", command=update_location).grid(row=5, column=0, columnspan=2, pady=10)
