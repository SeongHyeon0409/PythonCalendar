import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime
from tkinter import simpledialog, messagebox
import sqlite3


class CalendarWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calendar Widget")

        # 현재 날짜 가져오기
        self.now = datetime.now()
        self.year = self.now.year
        self.month = self.now.month

        # SQLite 데이터베이스 연결
        self.conn = sqlite3.connect("calendar_memo.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # 월 이름 리스트 생성
        self.months = ["1", "2", "3", "4", "5", "6",
                       "7", "8", "9", "10", "11", "12"]

        self.month_var = tk.StringVar(value=self.months[self.month - 1])
        self.year_var = tk.StringVar(value=str(self.year))

        # 위젯 생성
        self.create_widgets()

        # 캘린더 표시
        self.update_month_year_from_widgets()
        self.update_calendar()

    def create_table(self):
        # 메모 저장용 테이블 생성
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                memo TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # 이전, 다음 버튼
        self.prev_button = tk.Button(self, text="<", command=self.prev_month)
        self.next_button = tk.Button(self, text=">", command=self.next_month)
        self.prev_button.grid(row=0, column=0, padx=10, pady=10)
        self.next_button.grid(row=0, column=2, padx=10, pady=10)

        # 콤보박스 (드롭다운 메뉴) 생성
        self.month_cb = ttk.Combobox(self, textvariable=self.month_var, values=self.months, state="readonly")
        self.year_cb = ttk.Combobox(self, textvariable=self.year_var, values=[str(year) for year in range(1900, 2101)], state="readonly")
        self.month_cb.grid(row=0, column=1, padx=10, pady=10)
        self.year_cb.grid(row=1, column=1, padx=10, pady=10)

        self.month_cb.bind("<<ComboboxSelected>>", lambda event: self.on_combobox_change())
        self.year_cb.bind("<<ComboboxSelected>>", lambda event: self.on_combobox_change())

        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_combobox_change(self):
        self.update_month_year_from_widgets()
        self.update_calendar()

    def update_month_year_from_widgets(self):
        try:
            self.month = int(self.month_var.get())
            self.year = int(self.year_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid month or year")
            self.month_var.set(self.months[self.month - 1])
            self.year_var.set(str(self.year))

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_comboboxes()
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_comboboxes()
        self.update_calendar()

    def update_comboboxes(self):
        self.month_var.set(self.months[self.month - 1])
        self.year_var.set(str(self.year))

    def add_memo(self, day):
        date_key = f"{self.year}-{self.month:02d}-{day:02d}"
        current_memo = self.get_memo(date_key)
        new_memo = simpledialog.askstring("Add Memo", f"Memo for {date_key}:", initialvalue=current_memo)
        if new_memo is not None:
            self.save_memo(date_key, new_memo)
            self.update_calendar()

    def save_memo(self, date, memo):
        self.cursor.execute("REPLACE INTO memos (date, memo) VALUES (?, ?)", (date, memo))
        self.conn.commit()

    def get_memo(self, date):
        self.cursor.execute("SELECT memo FROM memos WHERE date = ?", (date,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.TextCalendar(firstweekday=calendar.SUNDAY)
        month_cal = cal.monthdayscalendar(self.year, self.month)

        # 요일 헤더
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=col, sticky="nsew")

        # 날짜
        for row, week in enumerate(month_cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_frame, text=day, command=lambda day=day: self.add_memo(day))
                    btn.grid(row=row, column=col, sticky="nsew")
                    date_key = f"{self.year}-{self.month:02d}-{day:02d}"
                    if self.get_memo(date_key):
                        btn.config(bg="lightblue")

    def on_closing(self):
        self.conn.close()
        self.destroy()


if __name__ == "__main__":
    app = CalendarWidget()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
