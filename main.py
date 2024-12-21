import tkinter as tk
from tkinter import messagebox
import bcrypt
from database import create_tables, connect_db
from change.add_stamp import add_stamp
from change.delete_stamp import delete_stamps_by_theme
from change.change_location import update_stamp_location
from get.countries_stamps import get_countries_in_section
from get.take_volume import get_volume_by_series
from get.places_theme import get_stamp_locations_by_theme
from get.themes_by_size import get_themes_by_stamp_size
from get.stamp_location import get_stamp_by_location
from get_report.countries_by_theme import get_countries_by_theme
from get_report.collection_report import generate_collection_report

#def add_user(username, password, role="user"):
#    """Добавляет нового пользователя в базу данных."""
#    conn = connect_db()
#    cursor = conn.cursor()
#    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#    try:
#        cursor.execute("INSERT INTO Users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
#        conn.commit()
#    except Exception as e:
#        print(f"Ошибка добавления пользователя: {e}")
#    finally:
#        conn.close()


def authenticate_user(username, password):
    """Проверяет имя пользователя и пароль."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, role FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return result[1]
    return None

def add_stamp_for_user(root, user_role):
    """Добавление марки только для админа."""
    if user_role != "admin":
        messagebox.showerror("Ошибка доступа", "У вас нет прав на добавление марок.")
        return
    add_stamp(root)

def delete_stamps_for_user(root, user_role):
    """Удаление марок только для админа."""
    if user_role != "admin":
        messagebox.showerror("Ошибка доступа", "У вас нет прав на удаление марок.")
        return
    delete_stamps_by_theme(root)

def update_location_for_user(root, user_role):
    """Изменение местоположения марок только для админа."""
    if user_role != "admin":
        messagebox.showerror("Ошибка доступа", "У вас нет прав на изменение местоположения.")
        return
    update_stamp_location(root)

def get_data_for_user(root, user_role):
    """Получение данных - доступно всем пользователям."""
    get_data_window = tk.Toplevel(root)
    get_data_window.title("Получить сведения")

    btn_add_mark = tk.Button(get_data_window, text="Марки каких стран содержатся в данном разделе", command=lambda: get_countries_in_section(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_add_mark = tk.Button(get_data_window, text="В каком томе коллекции находится марка определенной серии", command=lambda: get_volume_by_series(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_add_mark = tk.Button(get_data_window, text="В каких местах коллекции находятся марки указанной темы", command=lambda: get_stamp_locations_by_theme(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_add_mark = tk.Button(get_data_window, text="Какие темы у серий, включающих марки определенного размера", command=lambda: get_themes_by_stamp_size(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_add_mark = tk.Button(get_data_window, text="Марка какой страны находится в данном месте", command=lambda: get_stamp_by_location(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

def main_menu(user_role):
    """Основное меню приложения с проверкой прав доступа."""
    btn_change_data = tk.Button(root, text="Изменить сведения", command=lambda: change_data(user_role))
    btn_change_data.pack(fill=tk.X, padx=10, pady=5)

    btn_get_data = tk.Button(root, text="Получить сведения", command=lambda: get_data_for_user(root, user_role))
    btn_get_data.pack(fill=tk.X, padx=10, pady=5)

    btn_get_report = tk.Button(root, text="Получить отчет", command=get_report)
    btn_get_report.pack(fill=tk.X, padx=10, pady=5)

def change_data(user_role):
    """Меню изменения данных с проверкой прав доступа."""
    change_data_window = tk.Toplevel(root)
    change_data_window.title("Изменить сведения")

    btn_add_mark = tk.Button(change_data_window, text="Добавить марку новой темы", command=lambda: add_stamp_for_user(root, user_role))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_delete_mark = tk.Button(change_data_window, text="Удалить марки одной темы", command=lambda: delete_stamps_for_user(root, user_role))
    btn_delete_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_change_location = tk.Button(change_data_window, text="Изменение места расположения марки в коллекции", command=lambda: update_location_for_user(root, user_role))
    btn_change_location.pack(fill=tk.X, padx=10, pady=5)

def login():
    """Окно для ввода имени пользователя и пароля."""
    login_window = tk.Toplevel(root)
    login_window.title("Авторизация")

    tk.Label(login_window, text="Введите имя пользователя:").pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Введите пароль:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    def verify_credentials():
        username = username_entry.get()
        password = password_entry.get()
        user_role = authenticate_user(username, password)
        if user_role:
            login_window.destroy()
            main_menu(user_role)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    tk.Button(login_window, text="Войти", command=verify_credentials).pack(pady=10)


def get_report():
    get_data_window = tk.Toplevel(root)
    get_data_window.title("Получить отчет")

    btn_add_mark = tk.Button(get_data_window, text="Справка о странах, на основе темы марок", command=lambda: get_countries_by_theme(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

    btn_add_mark = tk.Button(get_data_window, text="Общий отчет по коллекции", command=lambda: generate_collection_report(root))
    btn_add_mark.pack(fill=tk.X, padx=10, pady=5)

if __name__ == "__main__":
    create_tables()

    # Добавление пользователей при первом запуске (для тестирования)
    #add_user("admin", "admin", "admin")
    #add_user("user", "user")

    root = tk.Tk()
    root.title("Коллекция марок")

    login()

    root.mainloop()
