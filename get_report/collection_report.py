import tkinter as tk
from tkinter import messagebox
from database import connect_db


def generate_collection_report(root):
    def show_collection_report():
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Получение списка всех разделов с темами и странами
            cursor.execute('''
                SELECT DISTINCT L.section_number, T.theme_name, S.country
                FROM Location L
                JOIN StampLocation SL ON L.locationID = SL.locationID
                JOIN Stamps S ON SL.stampID = S.stampID
                JOIN Series SR ON S.seriesID = SR.seriesID
                JOIN Themes T ON SR.themeID = T.themeID
                ORDER BY L.section_number, T.theme_name, S.country
            ''')
            sections = cursor.fetchall()

            # Сбор данных по маркам и страницам
            report_data = {}
            for section in sections:
                section_number = section[0]
                theme_name = section[1]
                country = section[2]

                # Если еще нет такого раздела в отчете, создаем его
                if section_number not in report_data:
                    report_data[section_number] = {
                        "themes": {},
                        "countries": {},
                        "page_count": 0
                    }

                # Если еще нет такой темы для раздела, добавляем
                if theme_name not in report_data[section_number]["themes"]:
                    report_data[section_number]["themes"][theme_name] = {
                        "countries": {},
                        "stamp_count": 0
                    }

                # Добавление страны и подсчет количества марок
                if country not in report_data[section_number]["themes"][theme_name]["countries"]:
                    report_data[section_number]["themes"][theme_name]["countries"][country] = 0

                # Подсчет количества марок для темы и страны
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM Stamps S
                    JOIN Series SR ON S.seriesID = SR.seriesID
                    JOIN Themes T ON SR.themeID = T.themeID
                    WHERE S.country = ? AND T.theme_name = ?
                ''', (country, theme_name))
                stamp_count = cursor.fetchone()[0]
                report_data[section_number]["themes"][theme_name]["countries"][country] += stamp_count
                report_data[section_number]["themes"][theme_name]["stamp_count"] += stamp_count

            # Получаем общее количество страниц
            cursor.execute('''
                SELECT COUNT(DISTINCT page_number)
                FROM Location
            ''')
            total_pages = cursor.fetchone()[0]

            # Формируем отчет
            result_text = "Отчет по коллекции:\n\n"
            for section_number, section_data in report_data.items():
                result_text += f"Раздел {section_number}:\n"
                for theme_name, theme_data in section_data["themes"].items():
                    result_text += f"  Тема: {theme_name}\n"
                    for country, stamp_count in theme_data["countries"].items():
                        result_text += f"    Страна: {country} - Количество марок: {stamp_count}\n"
                    result_text += f"  Общее количество марок в теме: {theme_data['stamp_count']}\n"
                result_text += f"Количество страниц в коллекции: {total_pages}\n\n"

            messagebox.showinfo("Отчет по коллекции", result_text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")
        finally:
            conn.close()

    report_button = tk.Button(root, text="Показать отчет по коллекции", command=show_collection_report)
    report_button.pack(pady=10)
