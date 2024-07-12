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
        self.geometry("400x400")

        # 현재 날짜 가져오기
        self.now = datetime.now()
        self.year = self.now.year
        self.month = self.now.month

        # SQLite 데이터베이스 연결
        self.conn = sqlite3.connect("calendar_memo.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # 월 이름 리스트 생성
        self.months = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]

        self.month_var = tk.StringVar(value=self.months[self.month - 1])
        self.year_var = tk.StringVar(value=str(self.year))

        # 위젯 생성
        self.create_widgets()

        # 캘린더 표시
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
        self.prev_button = tk.Button(self, text="<<", command=self.prev_month)
        self.next_button = tk.Button(self, text=">>", command=self.next_month)
        self.prev_button.pack(side=tk.LEFT, padx=20)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # 콤보박스 (드롭다운 메뉴) 생성
        self.month_cb = ttk.Combobox(self, textvariable=self.month_var, values=self.months)
        self.year_cb = ttk.Combobox(self, textvariable=self.year_var, values=[str(year) for year in range(1900, 2101)])

        self.month_cb.pack(pady=5)
        self.year_cb.pack(pady=5)

        self.month_cb.bind("<<ComboboxSelected>>", self.update_calendar)
        self.year_cb.bind("<<ComboboxSelected>>", self.update_calendar)

        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(fill="both", expand=True)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.update_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.update_calendar()

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

    def update_calendar(self, event=None):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_var.set(self.months[self.month - 1])
        self.year_var.set(str(self.year))

        cal = calendar.TextCalendar(firstweekday=calendar.SUNDAY)
        month_cal = cal.monthdayscalendar(self.year, self.month)

        # 요일 헤더
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=col)

        # 날짜
        for row, week in enumerate(month_cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_frame, text=day, command=lambda day=day: self.add_memo(day))
                    btn.grid(row=row, column=col)
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
