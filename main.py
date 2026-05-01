import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("700x600")

        # 1. Список предопределенных цитат
        self.quotes_pool = [
            {"text": "Жизнь — это то, что случается с тобой, пока ты оживлённо строишь другие планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "theme": "Наука"},
            {"text": "Успех — это способность идти от одной неудачи к другой, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Ваше время ограничено, поэтому не тратьте его на чью-то чужую жизнь.", "author": "Стив Джобс", "theme": "Мотивация"},
            {"text": "Великие умы обсуждают идеи, средние умы обсуждают события, а мелкие умы обсуждают людей.", "author": "Элеонора Рузвельт", "theme": "Мудрость"}
        ]

        self.history = []
        self.history_file = "history.json"

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # --- СЕКЦИЯ ВЫВОДА ЦИТАТЫ ---
        quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        quote_frame.pack(fill="x", padx=10, pady=10)

        self.quote_label = tk.Label(quote_frame, text="Нажмите кнопку, чтобы получить цитату", wraplength=600, font=("Arial", 12, "italic"))
        self.quote_label.pack(pady=10)

        self.author_label = tk.Label(quote_frame, text="", font=("Arial", 10, "bold"))
        self.author_label.pack()

        # 2. Кнопка генерации
        tk.Button(self.root, text="СГЕНЕРИРОВАТЬ ЦИТАТУ", command=self.generate_quote, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # 4. СЕКЦИЯ ФИЛЬТРАЦИИ
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0)
        self.filter_author = tk.Entry(filter_frame)
        self.filter_author.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2)
        self.filter_theme = tk.Entry(filter_frame)
        self.filter_theme.grid(row=0, column=3, padx=5)


tk.Button(filter_frame, text="Применить", command=self.update_history_table).grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filters).grid(row=0, column=5, padx=5)

        # 3. ТАБЛИЦА ИСТОРИИ
        tk.Label(self.root, text="История сгенерированных цитат:").pack(pady=(10, 0))
        self.tree = ttk.Treeview(self.root, columns=("text", "author", "theme"), show="headings")
        self.tree.heading("text", text="Текст цитаты")
        self.tree.heading("author", text="Автор")
        self.tree.heading("theme", text="Тема")
        
        self.tree.column("text", width=350)
        self.tree.column("author", width=120)
        self.tree.column("theme", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_quote(self):
        # Случайный выбор
        quote = random.choice(self.quotes_pool)
        
        # Отображение
        self.quote_label.config(text=f"«{quote['text']}»")
        self.author_label.config(text=f"— {quote['author']} ({quote['theme']})")

        # Добавление в историю
        self.history.insert(0, quote)
        self.update_history_table()
        self.save_history()

    def update_history_table(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)

        author_query = self.filter_author.get().lower().strip()
        theme_query = self.filter_theme.get().lower().strip()

        for q in self.history:
            # Логика фильтрации
            if author_query and author_query not in q['author'].lower():
                continue
            if theme_query and theme_query not in q['theme'].lower():
                continue
            
            self.tree.insert("", "end", values=(q['text'], q['author'], q['theme']))

    def reset_filters(self):
        self.filter_author.delete(0, tk.END)
        self.filter_theme.delete(0, tk.END)
        self.update_history_table()

    # 5. Сохранение в JSON
    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_history_table()
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()




