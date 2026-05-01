import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ===== КОНСТАНТЫ =====
DATA_FILE = "weather_data.json"
DATE_FORMAT = "%Y-%m-%d"

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        self.records = self.load_records()
        self.current_filter_date = None
        self.current_filter_temp = None

        self.create_widgets()
        self.update_display()

    # ===== РАБОТА С JSON =====
    def load_records(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки: {e}")
                return []
        return []

    def save_records(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    # ===== ВАЛИДАЦИЯ =====
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def validate_temperature(self, temp_str):
        try:
            float(temp_str)
            return True
        except ValueError:
            return False

    # ===== ИНТЕРФЕЙС =====
    def create_widgets(self):
        # Рамка добавления записи
        add_frame = ttk.LabelFrame(self.root, text="➕ Добавить запись о погоде", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        # Дата
        ttk.Label(add_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(add_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))

        # Температура
        ttk.Label(add_frame, text="Температура (°C):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.temp_entry = ttk.Entry(add_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)

        # Описание
        ttk.Label(add_frame, text="Описание:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.desc_entry = ttk.Entry(add_frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Осадки
        self.precipitation_var = tk.BooleanVar()
        ttk.Checkbutton(add_frame, text="🌧 Осадки", variable=self.precipitation_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Кнопка добавления
        self.add_btn = ttk.Button(add_frame, text="📝 Добавить запись", command=self.add_record)
        self.add_btn.grid(row=2, column=2, columnspan=2, pady=5)

        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Температура выше (°C):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_temp_entry = ttk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5, pady=5)

        self.apply_filter_btn = ttk.Button(filter_frame, text="🔍 Применить", command=self.apply_filter)
        self.apply_filter_btn.grid(row=0, column=4, padx=5, pady=5)

        self.reset_filter_btn = ttk.Button(filter_frame, text="🔄 Сбросить", command=self.reset_filter)
        self.reset_filter_btn.grid(row=0, column=5, padx=5, pady=5)

        # Рамка списка записей
        records_frame = ttk.LabelFrame(self.root, text="📋 Дневник погоды", padding=10)
        records_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица
        columns = ("№", "Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(records_frame, columns=columns, show="headings", height=12)
        self.tree.heading("№", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура", text="Температура")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")

        self.tree.column("№", width=40)
        self.tree.column("Дата", width=100)
        self.tree.column("Температура", width=100)
        self.tree.column("Описание", width=350)
        self.tree.column("Осадки", width=80)

        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.delete_btn = ttk.Button(btn_frame, text="❌ Удалить выбранную", command=self.delete_record)
        self.delete_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="🗑 Очистить весь дневник", command=self.clear_all)
        self.clear_btn.pack(side="left", padx=5)

    # ===== ДОБАВЛЕНИЕ ЗАПИСИ =====
    def add_record(self):
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = self.precipitation_var.get()

        # Валидация
        if not self.validate_date(date):
            messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД\nПример: 2024-12-25")
            return

        if not self.validate_temperature(temp):
            messagebox.showwarning("Ошибка", "Температура должна быть числом\nПример: -5, 10, 23.5")
            return

        if not description:
            messagebox.showwarning("Ошибка", "Описание погоды не может быть пустым!")
            return

        # Добавление
        record = {
            "date": date,
            "temperature": float(temp),
            "description": description,
            "precipitation": precipitation,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.records.append(record)
        self.save_records()

        # Очистка полей
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)

        self.update_display()
        messagebox.showinfo("Успех", "Запись добавлена!")

    # ===== ФИЛЬТРАЦИЯ =====
    def apply_filter(self):
        filter_date = self.filter_date_entry.get().strip()
        filter_temp = self.filter_temp_entry.get().strip()

        if filter_date:
            if not self.validate_date(filter_date):
                messagebox.showwarning("Ошибка", "Неверный формат даты фильтра")
                return
            self.current_filter_date = filter_date
        else:
            self.current_filter_date = None

        if filter_temp:
            if not self.validate_temperature(filter_temp):
                messagebox.showwarning("Ошибка", "Температура фильтра должна быть числом")
                return
            self.current_filter_temp = float(filter_temp)
        else:
            self.current_filter_temp = None

        self.update_display()

    def reset_filter(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.current_filter_date = None
        self.current_filter_temp = None
        self.update_display()

    # ===== ОТОБРАЖЕНИЕ =====
    def update_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered = self.records.copy()

        if self.current_filter_date:
            filtered = [r for r in filtered if r["date"] == self.current_filter_date]

        if self.current_filter_temp is not None:
            filtered = [r for r in filtered if r["temperature"] > self.current_filter_temp]

        filtered.sort(key=lambda x: x["date"], reverse=True)

        for idx, record in enumerate(filtered, 1):
            precip_text = "🌧 Да" if record["precipitation"] else "☀️ Нет"
            self.tree.insert("", "end", values=(
                idx,
                record["date"],
                f"{record['temperature']}°C",
                record["description"],
                precip_text
            ))

        # Обновляем заголовок
        if self.current_filter_date or self.current_filter_temp:
            status = []
            if self.current_filter_date:
                status.append(f"дата={self.current_filter_date}")
            if self.current_filter_temp is not None:
                status.append(f"температура > {self.current_filter_temp}°C")
            self.root.title(f"Weather Diary - Фильтр: {', '.join(status)}")
        else:
            self.root.title("Weather Diary - Дневник погоды")

    # ===== УДАЛЕНИЕ =====
    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        item = self.tree.item(selected[0])
        date = item["values"][1]
        temp_str = item["values"][2].replace("°C", "")
        temp = float(temp_str)
        description = item["values"][3]

        for i, record in enumerate(self.records):
            if record["date"] == date and record["temperature"] == temp and record["description"] == description:
                del self.records[i]
                break

        self.save_records()
        self.update_display()
        messagebox.showinfo("Успех", "Запись удалена")

    def clear_all(self):
        if not self.records:
            messagebox.showinfo("Инфо", "Дневник уже пуст")
            return

        if messagebox.askyesno("Подтверждение", "Удалить ВСЕ записи? Отменить нельзя!"):
            self.records.clear()
            self.save_records()
            self.reset_filter()
            self.update_display()
            messagebox.showinfo("Успех", "Дневник очищен")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
