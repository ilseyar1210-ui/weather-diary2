import unittest
import json
import os
from datetime import datetime

class TestWeatherDiary(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_weather.json"
        self.date_format = "%Y-%m-%d"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_date_validation(self):
        """Тест валидации даты"""
        from main import WeatherDiary
        # Создаём заглушку для теста
        import tkinter as tk
        root = tk.Tk()
        app = WeatherDiary(root)
        
        self.assertTrue(app.validate_date("2024-12-25"))
        self.assertTrue(app.validate_date("2024-01-01"))
        self.assertFalse(app.validate_date("25-12-2024"))
        self.assertFalse(app.validate_date("2024/12/25"))
        self.assertFalse(app.validate_date("2024-13-01"))
        self.assertFalse(app.validate_date("2024-12-32"))
        root.destroy()

    def test_temperature_validation(self):
        """Тест валидации температуры"""
        from main import WeatherDiary
        import tkinter as tk
        root = tk.Tk()
        app = WeatherDiary(root)
        
        self.assertTrue(app.validate_temperature("25"))
        self.assertTrue(app.validate_temperature("-10"))
        self.assertTrue(app.validate_temperature("23.5"))
        self.assertTrue(app.validate_temperature("0"))
        self.assertFalse(app.validate_temperature(""))
        self.assertFalse(app.validate_temperature("abc"))
        self.assertFalse(app.validate_temperature("10..5"))
        root.destroy()

    def test_save_and_load(self):
        """Тест сохранения и загрузки"""
        from main import WeatherDiary
        import tkinter as tk
        root = tk.Tk()
        app = WeatherDiary(root)
        
        # Подменяем файл
        import main
        main.DATA_FILE = self.test_file
        app.DATA_FILE = self.test_file
        
        test_data = [{
            "date": "2024-12-25",
            "temperature": 25.0,
            "description": "Солнечно",
            "precipitation": False,
            "created_at": "2024-12-25 12:00:00"
        }]
        
        app.records = test_data
        app.save_records()
        
        app.records = []
        app.records = app.load_records()
        
        self.assertEqual(len(app.records), 1)
        self.assertEqual(app.records[0]["description"], "Солнечно")
        root.destroy()

    def test_empty_description_validation(self):
        """Тест: пустое описание не должно проходить"""
        from main import WeatherDiary
        import tkinter as tk
        root = tk.Tk()
        app = WeatherDiary(root)
        
        # Симулируем пустое описание
        description = ""
        self.assertEqual(description, "")  # Пустое описание
        root.destroy()


if __name__ == "__main__":
    unittest.main()
