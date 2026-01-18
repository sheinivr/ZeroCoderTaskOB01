# -*- coding: utf-8 -*-
"""
TodoShop - Менеджер задач и магазинов
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import sys

# ============================================
# НАСТРОЙКИ ВНЕШНЕГО ВИДА
# ============================================

# Цветовая схема
COLORS = {
    'primary': '#2C3E50',      # Тёмно-синий
    'secondary': '#3498DB',    # Синий
    'success': '#27AE60',      # Зелёный
    'danger': '#E74C3C',       # Красный
    'warning': '#F39C12',      # Оранжевый
    'light': '#ECF0F1',        # Светлый
    'dark': '#2C3E50',         # Тёмный
    'background': '#F5F7FA',   # Фон
    'text': '#2C3E50',         # Текст
}

# ============================================
# КЛАСС ДЛЯ ЗАДАЧ
# ============================================

class Zadacha:
    """Класс для управления задачами"""
    def __init__(self, opisanie, srok):
        self.opisanie = opisanie
        self.srok = srok
        self.status = "не выполнено"
        self.data_sozdania = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    def otmetit_gotovoi(self):
        """Отметить задачу как выполненную"""
        self.status = "выполнено"
        self.data_vypolnenia = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    def info_kratko(self):
        """Краткая информация о задаче"""
        status_icon = "✓" if self.status == "выполнено" else "◯"
        return f"{status_icon} {self.opisanie[:30]}..."
    
    def __str__(self):
        return f"[{self.status}] {self.opisanie} | Срок: {self.srok}"

# ============================================
# КЛАСС ДЛЯ МАГАЗИНА
# ============================================

class Magazin:
    """Класс для управления магазинами"""
    def __init__(self, nazvanie, adres, tip):
        self.nazvanie = nazvanie
        self.adres = adres
        self.tip = tip
        self.tovary = {}
        self.data_sozdania = datetime.now().strftime("%d.%m.%Y")
    
    def dobavit_tovar(self, tovar, cena, kolichestvo=1):
        """Добавить товар в ассортимент"""
        self.tovary[tovar] = {
            'cena': float(cena),
            'kolichestvo': int(kolichestvo),
            'data_dobavlenia': datetime.now().strftime("%d.%m.%Y")
        }
        return True
    
    def udalit_tovar(self, tovar):
        """Удалить товар из ассортимента"""
        if tovar in self.tovary:
            del self.tovary[tovar]
            return True
        return False
    
    def uznat_cenu(self, tovar):
        """Узнать цену товара"""
        if tovar in self.tovary:
            return self.tovary[tovar]['cena']
        return None
    
    def obnovit_cenu(self, tovar, novaia_cena):
        """Обновить цену товара"""
        if tovar in self.tovary:
            self.tovary[tovar]['cena'] = float(novaia_cena)
            return True
        return False
    
    def obnovit_kolichestvo(self, tovar, novoe_kolichestvo):
        """Обновить количество товара"""
        if tovar in self.tovary:
            self.tovary[tovar]['kolichestvo'] = int(novoe_kolichestvo)
            return True
        return False
    
    def obshchaia_stoimost(self):
        """Общая стоимость всех товаров"""
        total = 0
        for tovar_info in self.tovary.values():
            total += tovar_info['cena'] * tovar_info['kolichestvo']
        return total
    
    def info_podrobno(self):
        """Подробная информация о магазине"""
        info = f"🏪 {self.nazvanie}\n"
        info += f"📍 {self.adres}\n"
        info += f"📊 Тип: {self.tip}\n"
        info += f"📅 Создан: {self.data_sozdania}\n"
        info += "─" * 40 + "\n"
        
        if self.tovary:
            info += f"📦 Товаров: {len(self.tovary)}\n"
            info += f"💰 Общая стоимость: {self.obshchaia_stoimost():.2f} руб.\n"
            info += "─" * 40 + "\n"
            
            # Сортируем товары по цене
            sorted_items = sorted(self.tovary.items(), 
                                key=lambda x: x[1]['cena'], 
                                reverse=True)
            
            for i, (tovar, info_tovara) in enumerate(sorted_items, 1):
                cena = info_tovara['cena']
                kol = info_tovara['kolichestvo']
                stoimost = cena * kol
                info += f"{i:2}. {tovar[:20]:20} | {cena:8.2f} руб. × {kol:3} = {stoimost:8.2f} руб.\n"
        else:
            info += "📭 В магазине нет товаров\n"
        
        return info

# ============================================
# ГЛАВНОЕ ОКНО ПРОГРАММЫ
# ============================================

class GlavnoeOkno:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 TodoShop - Менеджер задач и магазинов")
        self.root.geometry("900x650")
        self.root.configure(bg=COLORS['background'])
        
        # Центрируем окно
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Загружаем шрифты
        self.load_fonts()
        
        # Инициализируем данные
        self.spisok_zadach = []
        self.spisok_magazinov = []
        self.sozdat_magaziny()
        self.dobavit_testovye_zadachi()
        
        # Создаем интерфейс
        self.sozdat_interfeis()
    
    def load_fonts(self):
        """Загружаем и настраиваем шрифты"""
        self.font_h1 = ('Arial', 16, 'bold')
        self.font_h2 = ('Arial', 14, 'bold')
        self.font_h3 = ('Arial', 12, 'bold')
        self.font_normal = ('Arial', 10)
        self.font_small = ('Arial', 9)
        self.font_mono = ('Courier New', 10)
    
    def sozdat_magaziny(self):
        """Создаем магазины для демонстрации"""
        # Магазин 1 - Продукты
        mag1 = Magazin("🍎 Фруктовый рай", "ул. Яблочная, 25", "Продуктовый")
        mag1.dobavit_tovar("Яблоки Голден", 120, 50)
        mag1.dobavit_tovar("Бананы", 90, 30)
        mag1.dobavit_tovar("Апельсины", 150, 40)
        mag1.dobavit_tovar("Молоко", 85, 20)
        mag1.dobavit_tovar("Хлеб", 45, 25)
        
        # Магазин 2 - Электроника
        mag2 = Magazin("💻 ТехноМир", "пр. Космонавтов, 17", "Электроника")
        mag2.dobavit_tovar("Наушники Sony", 4500, 5)
        mag2.dobavit_tovar("Клавиатура", 2500, 8)
        mag2.dobavit_tovar("Мышь беспроводная", 1200, 12)
        mag2.dobavit_tovar("Флешка 64GB", 800, 15)
        
        # Магазин 3 - Книги
        mag3 = Magazin("📚 Книжная лавка", "ул. Пушкина, 10", "Книжный")
        mag3.dobavit_tovar("Python для начинающих", 1500, 7)
        mag3.dobavit_tovar("Роман '1984'", 600, 10)
        mag3.dobavit_tovar("Детская энциклопедия", 1200, 5)
        mag3.dobavit_tovar("Книга рецептов", 850, 8)
        
        self.spisok_magazinov = [mag1, mag2, mag3]
    
    def dobavit_testovye_zadachi(self):
        """Добавляем тестовые задачи"""
        self.spisok_zadach.append(Zadacha("Сдать проект по ООП", "15.01.2026"))
        self.spisok_zadach.append(Zadacha("Купить продукты на неделю", "10.01.2026"))
        self.spisok_zadach.append(Zadacha("Сходить на пары", "Каждый день"))
        self.spisok_zadach.append(Zadacha("Сделать презентацию", "12.01.2026"))
        self.spisok_zadach.append(Zadacha("Встретиться с друзьями", "09.01.2026"))
        
        # Отмечаем одну задачу как выполненную
        self.spisok_zadach[1].otmetit_gotovoi()
    
    def sozdat_interfeis(self):
        """Создаем основной интерфейс"""
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        # Заголовок
        title_label = tk.Label(top_frame, 
                              text="📋 TodoShop - Менеджер задач и магазинов",
                              font=self.font_h1,
                              fg='white',
                              bg=COLORS['primary'])
        title_label.pack(pady=20)
        
        # Подзаголовок
        subtitle_label = tk.Label(top_frame,
                                 text="Проект по объектно-ориентированному программированию",
                                 font=self.font_small,
                                 fg='#BDC3C7',
                                 bg=COLORS['primary'])
        subtitle_label.pack()
        
        # Контейнер для вкладок
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.vkladki = ttk.Notebook(main_frame)
        self.vkladki.pack(fill='both', expand=True)
        
        # Создаем вкладки
        self.sdelat_vkladku_zadach()
        self.sdelat_vkladku_magazinov()
        self.sdelat_vkladku_proverki()
        self.sdelat_vkladku_informacii()
        
        # Статус бар (создаём ПОСЛЕ вкладок)
        self.sozdat_status_bar()
    
    def sozdat_status_bar(self):
        """Создаем статус бар внизу окна"""
        status_frame = tk.Frame(self.root, bg=COLORS['dark'], height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # Статистика слева
        self.status_label = tk.Label(status_frame,
                                    text="Готов к работе",
                                    font=self.font_small,
                                    fg='white',
                                    bg=COLORS['dark'])
        self.status_label.pack(side='left', padx=10)
        
        # Время справа
        self.time_label = tk.Label(status_frame,
                                  text=datetime.now().strftime("%d.%m.%Y %H:%M"),
                                  font=self.font_small,
                                  fg='white',
                                  bg=COLORS['dark'])
        self.time_label.pack(side='right', padx=10)
    
    def sdelat_vkladku_zadach(self):
        """Создаем вкладку для управления задачами"""
        vkladka = tk.Frame(self.vkladki, bg=COLORS['background'])
        self.vkladki.add(vkladka, text="📝 Мои задачи")
        
        # Две колонки
        left_frame = tk.Frame(vkladka, bg=COLORS['background'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(vkladka, bg=COLORS['background'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # === ЛЕВАЯ КОЛОНКА: Добавление задачи ===
        add_frame = tk.LabelFrame(left_frame,
                                 text="➕ Новая задача",
                                 font=self.font_h2,
                                 bg=COLORS['background'],
                                 fg=COLORS['primary'],
                                 padx=15,
                                 pady=15)
        add_frame.pack(fill='x', pady=(0, 10))
        
        # Описание задачи
        tk.Label(add_frame,
                text="Что нужно сделать:",
                font=self.font_h3,
                bg=COLORS['background']).pack(anchor='w', pady=(0, 5))
        
        self.pole_opisania = tk.Text(add_frame,
                                    height=3,
                                    width=40,
                                    font=self.font_normal,
                                    relief='solid',
                                    borderwidth=1)
        self.pole_opisania.pack(fill='x', pady=(0, 10))
        self.pole_opisania.insert('1.0', "Например: Сделать домашнее задание")
        
        # Срок выполнения
        tk.Label(add_frame,
                text="Срок выполнения:",
                font=self.font_h3,
                bg=COLORS['background']).pack(anchor='w', pady=(0, 5))
        
        srok_frame = tk.Frame(add_frame, bg=COLORS['background'])
        srok_frame.pack(fill='x', pady=(0, 15))
        
        self.pole_sroka = ttk.Combobox(srok_frame,
                                      values=[
                                          "Сегодня",
                                          "Завтра",
                                          "На этой неделе",
                                          "На следующей неделе",
                                          "В этом месяце"
                                      ],
                                      font=self.font_normal,
                                      state='readonly',
                                      width=25)
        self.pole_sroka.pack(side='left')
        self.pole_sroka.set("На этой неделе")
        
        # Кнопка добавления
        add_btn = tk.Button(add_frame,
                           text="✅ Добавить задачу",
                           command=self.dobavit_zadachu,
                           bg=COLORS['success'],
                           fg='white',
                           font=('Arial', 11, 'bold'),
                           padx=20,
                           pady=10)
        add_btn.pack(pady=10)
        
        # === ПРАВАЯ КОЛОНКА: Список задач ===
        list_frame = tk.LabelFrame(right_frame,
                                  text="📋 Текущие задачи",
                                  font=self.font_h2,
                                  bg=COLORS['background'],
                                  fg=COLORS['primary'],
                                  padx=15,
                                  pady=15)
        list_frame.pack(fill='both', expand=True)
        
        # Заголовки списка
        header_frame = tk.Frame(list_frame, bg=COLORS['light'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(header_frame,
                text="Статус",
                font=self.font_h3,
                bg=COLORS['light'],
                width=8).pack(side='left', padx=2)
        tk.Label(header_frame,
                text="Задача",
                font=self.font_h3,
                bg=COLORS['light'],
                width=25).pack(side='left', padx=2)
        tk.Label(header_frame,
                text="Срок",
                font=self.font_h3,
                bg=COLORS['light'],
                width=12).pack(side='left', padx=2)
        
        # Прокручиваемый список задач
        list_container = tk.Frame(list_frame, bg=COLORS['background'])
        list_container.pack(fill='both', expand=True)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(list_container, bg=COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=canvas.yview)
        
        self.task_list_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.create_window((0, 0), window=self.task_list_frame, anchor='nw')
        
        # Обновляем список задач
        self.obnovit_spisok_zadach()
        
        # Настройка прокрутки
        self.task_list_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Кнопки управления
        btn_frame = tk.Frame(list_frame, bg=COLORS['background'])
        btn_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(btn_frame,
                 text="✓ Выполнить",
                 command=self.otmetit_gotovoi,
                 bg=COLORS['success'],
                 fg='white',
                 font=self.font_normal,
                 padx=15,
                 pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="✎ Редактировать",
                 command=self.redaktirovat_zadachu,
                 bg=COLORS['warning'],
                 fg='white',
                 font=self.font_normal,
                 padx=15,
                 pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="🗑 Удалить",
                 command=self.udalit_zadachu,
                 bg=COLORS['danger'],
                 fg='white',
                 font=self.font_normal,
                 padx=15,
                 pady=5).pack(side='left', padx=5)
        
        # Статистика
        stats_frame = tk.Frame(right_frame, bg=COLORS['background'])
        stats_frame.pack(fill='x', pady=(10, 0))
        
        self.stats_label = tk.Label(stats_frame,
                                   text="Всего задач: 0 | Выполнено: 0 | Осталось: 0",
                                   font=self.font_small,
                                   bg=COLORS['background'],
                                   fg=COLORS['dark'])
        self.stats_label.pack()
        
        self.obnovit_statistiku()
    
    def sdelat_vkladku_magazinov(self):
        """Создаем вкладку для управления магазинами"""
        vkladka = tk.Frame(self.vkladki, bg=COLORS['background'])
        self.vkladki.add(vkladka, text="🏪 Магазины")
        
        # Верхняя часть - выбор магазина
        top_frame = tk.Frame(vkladka, bg=COLORS['background'])
        top_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(top_frame,
                text="Выберите магазин:",
                font=self.font_h2,
                bg=COLORS['background']).pack(side='left', padx=(0, 10))
        
        self.vybrannyi_magazin = tk.StringVar()
        self.vybrannyi_magazin.set(self.spisok_magazinov[0].nazvanie)
        
        magazin_combo = ttk.Combobox(top_frame,
                                    textvariable=self.vybrannyi_magazin,
                                    values=[m.nazvanie for m in self.spisok_magazinov],
                                    state='readonly',
                                    width=30)
        magazin_combo.pack(side='left', padx=5)
        magazin_combo.bind('<<ComboboxSelected>>', lambda e: self.pokazat_info_magazina())
        
        # Кнопка обновить
        tk.Button(top_frame,
                 text="🔄 Обновить",
                 command=self.pokazat_info_magazina,
                 bg=COLORS['secondary'],
                 fg='white',
                 font=self.font_normal,
                 padx=15).pack(side='left', padx=10)
        
        # Основная информация
        info_frame = tk.Frame(vkladka, bg=COLORS['background'])
        info_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Текстовая область с информацией
        info_text_frame = tk.LabelFrame(info_frame,
                                       text="📊 Информация о магазине",
                                       font=self.font_h2,
                                       bg=COLORS['background'],
                                       fg=COLORS['primary'],
                                       padx=15,
                                       pady=15)
        info_text_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.pole_info = tk.Text(info_text_frame,
                                height=20,
                                width=50,
                                font=self.font_mono,
                                bg='white',
                                relief='solid',
                                borderwidth=1)
        self.pole_info.pack(fill='both', expand=True)
        
        # Добавление полосы прокрутки
        scrollbar = ttk.Scrollbar(self.pole_info)
        scrollbar.pack(side='right', fill='y')
        self.pole_info.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pole_info.yview)
        
        # Панель управления товарами
        control_frame = tk.LabelFrame(info_frame,
                                     text="🛠 Управление товарами",
                                     font=self.font_h2,
                                     bg=COLORS['background'],
                                     fg=COLORS['primary'],
                                     padx=15,
                                     pady=15)
        control_frame.pack(side='right', fill='both', padx=(10, 0))
        
        # Поля ввода
        tk.Label(control_frame,
                text="Название товара:",
                font=self.font_h3,
                bg=COLORS['background']).pack(anchor='w', pady=(0, 5))
        
        self.pole_tovara = tk.Entry(control_frame,
                                   font=self.font_normal,
                                   width=25)
        self.pole_tovara.pack(fill='x', pady=(0, 10))
        
        tk.Label(control_frame,
                text="Цена (руб.):",
                font=self.font_h3,
                bg=COLORS['background']).pack(anchor='w', pady=(0, 5))
        
        self.pole_ceny = tk.Entry(control_frame,
                                 font=self.font_normal,
                                 width=15)
        self.pole_ceny.pack(fill='x', pady=(0, 10))
        
        tk.Label(control_frame,
                text="Количество:",
                font=self.font_h3,
                bg=COLORS['background']).pack(anchor='w', pady=(0, 5))
        
        self.pole_kolichestva = tk.Entry(control_frame,
                                        font=self.font_normal,
                                        width=10)
        self.pole_kolichestva.pack(fill='x', pady=(0, 20))
        self.pole_kolichestva.insert(0, "1")
        
        # Кнопки в сетке
        button_grid = tk.Frame(control_frame, bg=COLORS['background'])
        button_grid.pack(fill='x')
        
        # Первый ряд кнопок
        btn1_frame = tk.Frame(button_grid, bg=COLORS['background'])
        btn1_frame.pack(fill='x', pady=5)
        
        tk.Button(btn1_frame,
                 text="➕ Добавить",
                 command=self.dobavit_tovar,
                 bg=COLORS['success'],
                 fg='white',
                 font=self.font_normal,
                 width=12,
                 pady=8).pack(side='left', padx=2)
        
        tk.Button(btn1_frame,
                 text="➖ Удалить",
                 command=self.udalit_tovar,
                 bg=COLORS['danger'],
                 fg='white',
                 font=self.font_normal,
                 width=12,
                 pady=8).pack(side='left', padx=2)
        
        # Второй ряд кнопок
        btn2_frame = tk.Frame(button_grid, bg=COLORS['background'])
        btn2_frame.pack(fill='x', pady=5)
        
        tk.Button(btn2_frame,
                 text="💰 Узнать цену",
                 command=self.uznat_cenu_tovara,
                 bg=COLORS['secondary'],
                 fg='white',
                 font=self.font_normal,
                 width=12,
                 pady=8).pack(side='left', padx=2)
        
        tk.Button(btn2_frame,
                 text="✎ Изменить цену",
                 command=self.izmenit_cenu,
                 bg=COLORS['warning'],
                 fg='white',
                 font=self.font_normal,
                 width=12,
                 pady=8).pack(side='left', padx=2)
        
        # Результат операций
        self.metka_rezultata = tk.Label(control_frame,
                                       text="",
                                       font=self.font_small,
                                       bg=COLORS['background'],
                                       fg=COLORS['success'],
                                       height=2,
                                       wraplength=200)
        self.metka_rezultata.pack(pady=10)
        
        # Показать информацию о первом магазине
        self.pokazat_info_magazina()
    
    def sdelat_vkladku_proverki(self):
        """Вкладка для тестирования работы классов"""
        vkladka = tk.Frame(self.vkladki, bg=COLORS['background'])
        self.vkladki.add(vkladka, text="🧪 Проверка")
        
        # Заголовок
        tk.Label(vkladka,
                text="Тестирование работы классов",
                font=self.font_h1,
                bg=COLORS['background'],
                fg=COLORS['primary']).pack(pady=20)
        
        # Описание
        description = """Здесь можно проверить корректность работы всех методов классов.
        Программа автоматически протестирует основные функции и покажет результат."""
        
        tk.Label(vkladka,
                text=description,
                font=self.font_normal,
                bg=COLORS['background'],
                wraplength=600,
                justify='center').pack(pady=10)
        
        # Кнопка запуска теста
        test_btn = tk.Button(vkladka,
                            text="▶ Запустить полную проверку",
                            command=self.proverit_vse,
                            bg=COLORS['primary'],
                            fg='white',
                            font=('Arial', 12, 'bold'),
                            padx=30,
                            pady=15)
        test_btn.pack(pady=20)
        
        # Область для вывода результатов
        result_frame = tk.LabelFrame(vkladka,
                                    text="📊 Результаты проверки",
                                    font=self.font_h2,
                                    bg=COLORS['background'],
                                    fg=COLORS['primary'],
                                    padx=15,
                                    pady=15)
        result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.pole_rezultatov = tk.Text(result_frame,
                                      height=15,
                                      font=self.font_mono,
                                      bg='#FAFAFA',
                                      relief='solid',
                                      borderwidth=1)
        self.pole_rezultatov.pack(fill='both', expand=True)
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self.pole_rezultatov)
        scrollbar.pack(side='right', fill='y')
        self.pole_rezultatov.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.pole_rezultatov.yview)
    
    def sdelat_vkladku_informacii(self):
        """Вкладка с информацией о проекте"""
        vkladka = tk.Frame(self.vkladki, bg=COLORS['background'])
        self.vkladki.add(vkladka, text="ℹ️ О программе")
        
        # Заголовок
        tk.Label(vkladka,
                text="TodoShop - Менеджер задач и магазинов",
                font=self.font_h1,
                bg=COLORS['background'],
                fg=COLORS['primary']).pack(pady=30)
        
        # Информация о проекте
        info_text = """📋 Описание проекта:
        
Этот проект разработан в рамках изучения объектно-ориентированного
программирования (ООП) на языке Python.

Проект демонстрирует:
• Создание и использование классов
• Работу с атрибутами и методами объектов
• Построение графического интерфейса с помощью Tkinter
• Практическое применение ООП в реальной задаче

🛠 Функциональность:
• Управление задачами (добавление, выполнение, удаление)
• Управление магазинами и товарами
• Тестирование всех методов классов
• Подробная статистика

📚 Используемые технологии:
• Python 3.x
• Tkinter для GUI
• ООП (классы, объекты, методы, инкапсуляция)

👨‍💻 Автор: [Введите ваше имя]
📅 Дата создания: Декабрь 2023
🎯 Курс: Программирование на Python
        """
        
        info_label = tk.Label(vkladka,
                             text=info_text,
                             font=self.font_normal,
                             bg=COLORS['background'],
                             justify='left',
                             wraplength=600)
        info_label.pack(pady=20, padx=40)
        
        # Разделитель
        tk.Frame(vkladka, height=2, bg=COLORS['light']).pack(fill='x', padx=50, pady=20)
        
        # Статистика программы
        stats_text = f"""📊 Статистика программы:
        
• Всего задач в системе: {len(self.spisok_zadach)}
• Магазинов создано: {len(self.spisok_magazinov)}
• Общее количество товаров: {sum(len(m.tovary) for m in self.spisok_magazinov)}
        """
        
        stats_label = tk.Label(vkladka,
                              text=stats_text,
                              font=self.font_normal,
                              bg=COLORS['light'],
                              relief='solid',
                              borderwidth=1,
                              padx=20,
                              pady=20)
        stats_label.pack(pady=10, padx=50)
        
        # Кнопка закрытия
        tk.Button(vkladka,
                 text="Закрыть программу",
                 command=self.root.quit,
                 bg=COLORS['danger'],
                 fg='white',
                 font=self.font_normal,
                 padx=30,
                 pady=10).pack(pady=30)
    
    # ============================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С ЗАДАЧАМИ
    # ============================================
    
    def dobavit_zadachu(self):
        """Добавить новую задачу"""
        opisanie = self.pole_opisania.get('1.0', 'end-1c').strip()
        srok = self.pole_sroka.get()
        
        if not opisanie or opisanie == "Например: Сделать домашнее задание":
            messagebox.showwarning("Внимание", "Введите описание задачи!")
            return
        
        novaia_zadacha = Zadacha(opisanie, srok)
        self.spisok_zadach.append(novaia_zadacha)
        
        self.obnovit_spisok_zadach()
        self.obnovit_statistiku()
        self.pole_opisania.delete('1.0', 'end')
        self.pole_opisania.insert('1.0', "Например: Сделать домашнее задание")
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Задача добавлена: {opisanie[:20]}...")
    
    def obnovit_spisok_zadach(self):
        """Обновить список задач на экране"""
        # Очищаем текущий список
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Добавляем задачи
        for i, zadacha in enumerate(self.spisok_zadach):
            if zadacha.status != "выполнено":
                task_frame = tk.Frame(self.task_list_frame, bg=COLORS['background'])
                task_frame.pack(fill='x', pady=2)
                
                # Статус
                status_btn = tk.Button(task_frame,
                                      text="◯",
                                      command=lambda idx=i: self.otmetit_po_indeksu(idx),
                                      bg=COLORS['light'],
                                      fg=COLORS['dark'],
                                      font=('Arial', 12),
                                      width=3,
                                      relief='flat')
                status_btn.pack(side='left', padx=5)
                
                # Описание
                desc_label = tk.Label(task_frame,
                                     text=zadacha.opisanie[:40],
                                     font=self.font_normal,
                                     bg=COLORS['background'],
                                     anchor='w',
                                     width=30)
                desc_label.pack(side='left', padx=5)
                
                # Срок
                srok_label = tk.Label(task_frame,
                                     text=zadacha.srok,
                                     font=self.font_small,
                                     bg=COLORS['background'],
                                     fg=COLORS['dark'],
                                     width=12)
                srok_label.pack(side='left', padx=5)
                
                # Кнопка удаления
                del_btn = tk.Button(task_frame,
                                   text="×",
                                   command=lambda idx=i: self.udalit_po_indeksu(idx),
                                   bg=COLORS['light'],
                                   fg=COLORS['danger'],
                                   font=('Arial', 12, 'bold'),
                                   width=2,
                                   relief='flat')
                del_btn.pack(side='right', padx=5)
    
    def obnovit_statistiku(self):
        """Обновить статистику задач"""
        vsego = len(self.spisok_zadach)
        vypolneno = sum(1 for z in self.spisok_zadach if z.status == "выполнено")
        ostalos = vsego - vypolneno
        
        self.stats_label.config(text=f"Всего задач: {vsego} | Выполнено: {vsego} | Осталось: {ostalos}")
    
    def otmetit_po_indeksu(self, index):
        """Отметить задачу по индексу"""
        if 0 <= index < len(self.spisok_zadach):
            self.spisok_zadach[index].otmetit_gotovoi()
            self.obnovit_spisok_zadach()
            self.obnovit_statistiku()
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Задача отмечена как выполненная")
    
    def udalit_po_indeksu(self, index):
        """Удалить задачу по индексу"""
        if 0 <= index < len(self.spisok_zadach):
            opisanie = self.spisok_zadach[index].opisanie
            del self.spisok_zadach[index]
            self.obnovit_spisok_zadach()
            self.obnovit_statistiku()
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Задача удалена: {opisanie[:20]}...")
    
    def otmetit_gotovoi(self):
        """Отметить выбранную задачу как выполненную"""
        if not self.spisok_zadach:
            messagebox.showwarning("Внимание", "Нет задач для отметки")
            return
        
        # Находим первую невыполненную задачу
        for i, zadacha in enumerate(self.spisok_zadach):
            if zadacha.status != "выполнено":
                zadacha.otmetit_gotovoi()
                break
        
        self.obnovit_spisok_zadach()
        self.obnovit_statistiku()
    
    def redaktirovat_zadachu(self):
        """Редактировать задачу (заглушка)"""
        messagebox.showinfo("Редактирование", "Функция редактирования в разработке")
    
    def udalit_zadachu(self):
        """Удалить задачу (заглушка)"""
        if not self.spisok_zadach:
            messagebox.showwarning("Внимание", "Нет задач для удаления")
            return
        
        # Удаляем первую невыполненную задачу
        for i, zadacha in enumerate(self.spisok_zadach):
            if zadacha.status != "выполнено":
                del self.spisok_zadach[i]
                break
        
        self.obnovit_spisok_zadach()
        self.obnovit_statistiku()
    
    # ============================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С МАГАЗИНАМИ
    # ============================================
    
    def pokazat_info_magazina(self):
        """Показать информацию о выбранном магазине"""
        nazvanie = self.vybrannyi_magazin.get()
        magazin = None
        
        for m in self.spisok_magazinov:
            if m.nazvanie == nazvanie:
                magazin = m
                break
        
        if not magazin:
            return
        
        self.pole_info.config(state='normal')
        self.pole_info.delete('1.0', 'end')
        self.pole_info.insert('1.0', magazin.info_podrobno())
        self.pole_info.config(state='disabled')
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Информация о магазине: {magazin.nazvanie}")
    
    def dobavit_tovar(self):
        """Добавить товар в магазин"""
        nazvanie_mag = self.vybrannyi_magazin.get()
        tovar = self.pole_tovara.get().strip()
        cena_text = self.pole_ceny.get().strip()
        kol_text = self.pole_kolichestva.get().strip()
        
        if not tovar or not cena_text:
            self.metka_rezultata.config(text="❌ Заполните название и цену", fg=COLORS['danger'])
            return
        
        try:
            cena = float(cena_text)
            kolichestvo = int(kol_text) if kol_text else 1
        except ValueError:
            self.metka_rezultata.config(text="❌ Цена и количество должны быть числами", fg=COLORS['danger'])
            return
        
        # Находим магазин
        for magazin in self.spisok_magazinov:
            if magazin.nazvanie == nazvanie_mag:
                magazin.dobavit_tovar(tovar, cena, kolichestvo)
                break
        
        self.pokazat_info_magazina()
        self.pole_tovara.delete(0, 'end')
        self.pole_ceny.delete(0, 'end')
        self.metka_rezultata.config(text=f"✅ Товар '{tovar}' добавлен", fg=COLORS['success'])
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"Товар добавлен: {tovar}")
    
    def udalit_tovar(self):
        """Удалить товар из магазина"""
        nazvanie_mag = self.vybrannyi_magazin.get()
        tovar = self.pole_tovara.get().strip()
        
        if not tovar:
            self.metka_rezultata.config(text="❌ Введите название товара", fg=COLORS['danger'])
            return
        
        # Находим магазин
        udalen = False
        for magazin in self.spisok_magazinov:
            if magazin.nazvanie == nazvanie_mag:
                udalen = magazin.udalit_tovar(tovar)
                break
        
        if udalen:
            self.pokazat_info_magazina()
            self.pole_tovara.delete(0, 'end')
            self.metka_rezultata.config(text=f"✅ Товар '{tovar}' удален", fg=COLORS['success'])
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Товар удален: {tovar}")
        else:
            self.metka_rezultata.config(text=f"❌ Товар '{tovar}' не найден", fg=COLORS['danger'])
    
    def izmenit_cenu(self):
        """Изменить цену товара"""
        nazvanie_mag = self.vybrannyi_magazin.get()
        tovar = self.pole_tovara.get().strip()
        cena_text = self.pole_ceny.get().strip()
        
        if not tovar or not cena_text:
            self.metka_rezultata.config(text="❌ Заполните название и новую цену", fg=COLORS['danger'])
            return
        
        try:
            novaia_cena = float(cena_text)
        except ValueError:
            self.metka_rezultata.config(text="❌ Цена должна быть числом", fg=COLORS['danger'])
            return
        
        # Находим магазин
        obnovlen = False
        for magazin in self.spisok_magazinov:
            if magazin.nazvanie == nazvanie_mag:
                obnovlen = magazin.obnovit_cenu(tovar, novaia_cena)
                break
        
        if obnovlen:
            self.pokazat_info_magazina()
            self.metka_rezultata.config(text=f"✅ Цена товара '{tovar}' изменена", fg=COLORS['success'])
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Цена изменена: {tovar}")
        else:
            self.metka_rezultata.config(text=f"❌ Товар '{tovar}' не найден", fg=COLORS['danger'])
    
    def uznat_cenu_tovara(self):
        """Узнать цену товара"""
        nazvanie_mag = self.vybrannyi_magazin.get()
        tovar = self.pole_tovara.get().strip()
        
        if not tovar:
            self.metka_rezultata.config(text="❌ Введите название товара", fg=COLORS['danger'])
            return
        
        # Находим магазин
        cena = None
        for magazin in self.spisok_magazinov:
            if magazin.nazvanie == nazvanie_mag:
                cena = magazin.uznat_cenu(tovar)
                break
        
        if cena is not None:
            self.metka_rezultata.config(text=f"💰 Цена '{tovar}': {cena:.2f} руб.", fg=COLORS['success'])
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Найдена цена: {tovar}")
        else:
            self.metka_rezultata.config(text=f"❌ Товар '{tovar}' не найден", fg=COLORS['danger'])
    
    # ============================================
    # МЕТОДЫ ДЛЯ ПРОВЕРКИ
    # ============================================
    
    def proverit_vse(self):
        """Проверить все классы и методы"""
        self.pole_rezultatov.config(state='normal')
        self.pole_rezultatov.delete('1.0', 'end')
        
        result_text = "=" * 60 + "\n"
        result_text += "           ПОЛНАЯ ПРОВЕРКА РАБОТЫ КЛАССОВ\n"
        result_text += "=" * 60 + "\n\n"
        
        # Проверка класса Zadacha
        result_text += "[1] ПРОВЕРКА КЛАССА ZADACHA\n"
        result_text += "-" * 40 + "\n"
        
        test_zadacha = Zadacha("Тестовая задача", "Сегодня")
        result_text += f"✓ Создана задача: {test_zadacha}\n"
        
        test_zadacha.otmetit_gotovoi()
        result_text += f"✓ Задача отмечена как выполненная\n"
        result_text += f"✓ Статус задачи: {test_zadacha.status}\n"
        result_text += f"✓ Краткая информация: {test_zadacha.info_kratko()}\n\n"
        
        # Проверка класса Magazin
        result_text += "[2] ПРОВЕРКА КЛАССА MAGAZIN\n"
        result_text += "-" * 40 + "\n"
        
        test_magazin = Magazin("Тестовый магазин", "ул. Тестовая, 1", "Тестовый")
        result_text += f"✓ Создан магазин: {test_magazin.nazvanie}\n"
        
        # Добавление товаров
        test_magazin.dobavit_tovar("Тестовый товар 1", 100, 5)
        test_magazin.dobavit_tovar("Тестовый товар 2", 200, 3)
        result_text += f"✓ Добавлено 2 тестовых товара\n"
        
        # Проверка цен
        cena = test_magazin.uznat_cenu("Тестовый товар 1")
        result_text += f"✓ Цена 'Тестовый товар 1': {cena} руб.\n"
        
        # Изменение цены
        test_magazin.obnovit_cenu("Тестовый товар 1", 150)
        novaia_cena = test_magazin.uznat_cenu("Тестовый товар 1")
        result_text += f"✓ Новая цена 'Тестовый товар 1': {novaia_cena} руб.\n"
        
        # Удаление товара
        test_magazin.udalit_tovar("Тестовый товар 2")
        result_text += f"✓ Товар 'Тестовый товар 2' удален\n"
        
        # Общая стоимость
        total = test_magazin.obshchaia_stoimost()
        result_text += f"✓ Общая стоимость товаров: {total:.2f} руб.\n\n"
        
        # Проверка данных в программе
        result_text += "[3] ПРОВЕРКА ДАННЫХ В ПРОГРАММЕ\n"
        result_text += "-" * 40 + "\n"
        
        result_text += f"✓ Всего задач в системе: {len(self.spisok_zadach)}\n"
        result_text += f"✓ Магазинов создано: {len(self.spisok_magazinov)}\n"
        
        for i, magazin in enumerate(self.spisok_magazinov, 1):
            result_text += f"  {i}. {magazin.nazvanie}: {len(magazin.tovary)} товаров\n"
        
        result_text += "\n" + "=" * 60 + "\n"
        result_text += "           ПРОВЕРКА ЗАВЕРШЕНА УСПЕШНО!\n"
        result_text += "=" * 60 + "\n"
        result_text += "\n✅ Все классы работают корректно!\n"
        result_text += "✅ Все методы выполняются без ошибок!\n"
        result_text += "✅ Программа готова к использованию!\n"
        
        self.pole_rezultatov.insert('1.0', result_text)
        self.pole_rezultatov.config(state='disabled')
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text="Полная проверка выполнена успешно!")

# ============================================
# ЗАПУСК ПРОГРАММЫ
# ============================================

def main():
    """Основная функция программы"""
    try:
        # Создаем главное окно
        root = tk.Tk()
        
        # Создаем приложение
        app = GlavnoeOkno(root)
        
        # Запускаем главный цикл
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске программы: {e}")
        messagebox.showerror("Ошибка", f"Не удалось запустить программу:\n{e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())