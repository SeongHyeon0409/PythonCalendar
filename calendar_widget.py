import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime


class CalendarWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calendar Widget")
        self.geometry("300x300")

        # 현재 날짜 가져오기
        self.now = datetime.now()
        self.year = self.now.year
        self.month = self.now.month

        # 콤보박스 (드롭다운 메뉴) 생성
        self.months = list(calendar.month_name)[1:]
        self.years = [str(year) for year in range(1900, 2101)]

        self.month_var = tk.StringVar(value=self.months[self.month - 1])
        self.year_var = tk.StringVar(value=str(self.year))

        self.month_cb = ttk.Combobox(self, textvariable=self.month_var, values=self.months)
        self.year_cb = ttk.Combobox(self, textvariable=self.year_var, values=self.years)

        self.month_cb.pack(pady=5)
        self.year_cb.pack(pady=5)

        self.month_cb.bind("<<ComboboxSelected>>", self.update_calendar)
        self.year_cb.bind("<<ComboboxSelected>>", self.update_calendar)

        # 캘린더 표시
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(fill="both", expand=True)

        self.update_calendar()

    def update_calendar(self, event=None):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        try:
            self.month = self.months.index(self.month_var.get()) + 1
            self.year = int(self.year_var.get())
        except ValueError:
            return

        cal = calendar.monthcalendar(self.year, self.month)

        # 요일 헤더
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days:
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=days.index(day))

        # 날짜
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    tk.Label(self.calendar_frame, text=day).grid(row=row, column=col)


if __name__ == "__main__":
    app = CalendarWidget()
    app.mainloop()
