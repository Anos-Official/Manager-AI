import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import threading
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Backend.Ai.ai import ask_ai

BUDGET_SYSTEM_PROMPT = """You are a Canadian financial advisor for Manager AI.
You help users budget their money based on Canadian cost of living.
Always use CAD, reference Canadian cities and provinces, and give realistic advice.
Be specific and practical."""

income_sources = []
expenses = []

def create(parent):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    # main scrollable area
    scroll = ctk.CTkScrollableFrame(frame, fg_color="#323339")
    scroll.pack(fill="both", expand=True, padx=10, pady=10)

    # title
    ctk.CTkLabel(scroll, text="Budget Tracker", font=font(26, bold=True)).pack(pady=(10,5))

    # ── INCOME SECTION ──
    ctk.CTkLabel(scroll, text="Income", font=font(18, bold=True)).pack(anchor="w", pady=(15,5))

    income_list_frame = ctk.CTkFrame(scroll, fg_color="#2C2D32", corner_radius=8)
    income_list_frame.pack(fill="x", pady=5)

    income_total_lbl = ctk.CTkLabel(scroll, text="Total Income: $0.00", font=font(14, bold=True))
    income_total_lbl.pack(anchor="w", pady=2)

    income_row = ctk.CTkFrame(scroll, fg_color="transparent")
    income_row.pack(fill="x", pady=5)

    income_name = ctk.CTkEntry(income_row, placeholder_text="Source (e.g. Job, Freelance)", width=250, font=font(13))
    income_name.pack(side="left", padx=5)

    income_amount = ctk.CTkEntry(income_row, placeholder_text="Amount ($)", width=150, font=font(13))
    income_amount.pack(side="left", padx=5)

    def refresh_income():
        for w in income_list_frame.winfo_children():
            w.destroy()
        total = 0
        for i, (name, amount) in enumerate(income_sources):
            row = ctk.CTkFrame(income_list_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=f"{name}: ${amount:,.2f}", font=font(13)).pack(side="left")
            ctk.CTkButton(row, text="✕", width=30, fg_color="transparent", hover_color="#ff4444",
                          font=font(13), command=lambda i=i: remove_income(i)).pack(side="right")
            total += amount
        income_total_lbl.configure(text=f"Total Income: ${total:,.2f}")
        refresh_chart()

    def remove_income(i):
        income_sources.pop(i)
        refresh_income()

    def add_income():
        name = income_name.get().strip()
        try:
            amount = float(income_amount.get().strip())
        except ValueError:
            return
        if name and amount > 0:
            income_sources.append((name, amount))
            income_name.delete(0, "end")
            income_amount.delete(0, "end")
            refresh_income()

    ctk.CTkButton(income_row, text="Add Income", command=add_income, font=font(13)).pack(side="left", padx=5)

    # ── EXPENSE SECTION ──
    ctk.CTkLabel(scroll, text="Expenses", font=font(18, bold=True)).pack(anchor="w", pady=(20,5))

    expense_list_frame = ctk.CTkFrame(scroll, fg_color="#2C2D32", corner_radius=8)
    expense_list_frame.pack(fill="x", pady=5)

    expense_total_lbl = ctk.CTkLabel(scroll, text="Total Expenses: $0.00", font=font(14, bold=True))
    expense_total_lbl.pack(anchor="w", pady=2)

    expense_row = ctk.CTkFrame(scroll, fg_color="transparent")
    expense_row.pack(fill="x", pady=5)

    expense_name = ctk.CTkEntry(expense_row, placeholder_text="Expense (e.g. Rent, Food)", width=200, font=font(13))
    expense_name.pack(side="left", padx=5)

    expense_amount = ctk.CTkEntry(expense_row, placeholder_text="Amount ($)", width=130, font=font(13))
    expense_amount.pack(side="left", padx=5)

    expense_category = ctk.CTkEntry(expense_row, placeholder_text="Category", width=130, font=font(13))
    expense_category.pack(side="left", padx=5)

    def refresh_expenses():
        for w in expense_list_frame.winfo_children():
            w.destroy()
        total_income = sum(a for _, a in income_sources)
        total = 0
        for i, (name, amount, category) in enumerate(expenses):
            pct = (amount / total_income * 100) if total_income > 0 else 0
            row = ctk.CTkFrame(expense_list_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=f"{name} ({category}): ${amount:,.2f}  ({pct:.1f}%)", font=font(13)).pack(side="left")
            ctk.CTkButton(row, text="✕", width=30, fg_color="transparent", hover_color="#ff4444",
                          font=font(13), command=lambda i=i: remove_expense(i)).pack(side="right")
            total += amount
        expense_total_lbl.configure(text=f"Total Expenses: ${total:,.2f}")
        refresh_summary(total)
        refresh_chart()

    def remove_expense(i):
        expenses.pop(i)
        refresh_expenses()

    def add_expense():
        name = expense_name.get().strip()
        category = expense_category.get().strip() or "Other"
        try:
            amount = float(expense_amount.get().strip())
        except ValueError:
            return
        if name and amount > 0:
            expenses.append((name, amount, category))
            expense_name.delete(0, "end")
            expense_amount.delete(0, "end")
            expense_category.delete(0, "end")
            refresh_expenses()

    ctk.CTkButton(expense_row, text="Add Expense", command=add_expense, font=font(13)).pack(side="left", padx=5)

    # ── AI GENERATE BUDGET ──
    ai_btn = ctk.CTkButton(scroll, text="AI Generate Budget Split", font=font(14, bold=True))
    ai_btn.pack(pady=10)

    def generate_budget():
        total_income = sum(a for _, a in income_sources)
        if total_income <= 0:
            return
        ai_btn.configure(state="disabled", text="Loading...")
        def run():
            prompt = f"""Generate a realistic monthly budget for someone in Canada with a total income of ${total_income:,.2f} CAD.
            Split it into expenses like Rent, Food, Transport, Utilities, Savings, Entertainment etc.
            For each expense give: name, recommended amount in CAD, category.
            Return ONLY a numbered list in this exact format:
            1. Rent: $1200 (Housing)
            2. Food: $400 (Food)
            Do not include any other text."""
            result = ask_ai(prompt, system_prompt=BUDGET_SYSTEM_PROMPT)
            lines = [l.strip() for l in result.split("\n") if l.strip() and ":" in l]
            for line in lines:
                try:
                    line = line.lstrip("0123456789. ")
                    parts = line.split(":")
                    name = parts[0].strip()
                    rest = parts[1].strip()
                    amount_str = rest.split("(")[0].strip().replace("$", "").replace(",", "")
                    category = rest.split("(")[1].replace(")", "").strip() if "(" in rest else "Other"
                    amount = float(amount_str)
                    expenses.append((name, amount, category))
                except Exception:
                    continue
            refresh_expenses()
            ai_btn.configure(state="normal", text="AI Generate Budget Split")
        threading.Thread(target=run).start()

    ai_btn.configure(command=generate_budget)

    # ── SUMMARY ──
    ctk.CTkLabel(scroll, text="Summary", font=font(18, bold=True)).pack(anchor="w", pady=(20,5))

    summary_lbl = ctk.CTkLabel(scroll, text="Remaining: $0.00", font=font(16, bold=True))
    summary_lbl.pack(anchor="w", pady=2)

    def refresh_summary(total_expenses):
        total_income = sum(a for _, a in income_sources)
        remaining = total_income - total_expenses
        color = "#44ff88" if remaining >= 0 else "#ff4444"
        summary_lbl.configure(text=f"Remaining: ${remaining:,.2f}", text_color=color)

    # ── PIE CHART ──
    ctk.CTkLabel(scroll, text="Budget Breakdown", font=font(18, bold=True)).pack(anchor="w", pady=(20,5))

    chart_frame = ctk.CTkFrame(scroll, fg_color="#2C2D32", corner_radius=8)
    chart_frame.pack(fill="x", pady=5)

    chart_canvas_holder = [None]

    def refresh_chart():
        if chart_canvas_holder[0]:
            chart_canvas_holder[0].get_tk_widget().destroy()
        if not expenses:
            return
        labels = [e[0] for e in expenses]
        sizes = [e[1] for e in expenses]
        fig = Figure(figsize=(5, 4), facecolor="#2C2D32")
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
               textprops={"color": "white", "fontsize": 9})
        ax.set_facecolor("#2C2D32")
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        chart_canvas_holder[0] = canvas

    # ── AI REVIEW ──
    ctk.CTkLabel(scroll, text="AI Budget Review", font=font(18, bold=True)).pack(anchor="w", pady=(20,5))

    review_box = ctk.CTkTextbox(scroll, height=200, state="disabled", font=font(13))
    review_box.pack(fill="x", pady=5)

    review_btn = ctk.CTkButton(scroll, text="Get AI Review", font=font(14, bold=True))
    review_btn.pack(pady=10)

    def get_review():
        review_btn.configure(state="disabled", text="Loading...")
        def run():
            total_income = sum(a for _, a in income_sources)
            expense_summary = "\n".join([f"{n}: ${a:,.2f} ({c})" for n, a, c in expenses])
            prompt = f"""Review this monthly budget for a Canadian resident:
            Total Income: ${total_income:,.2f} CAD
            Expenses:
            {expense_summary}
            Give specific advice on: what looks good, what should change, what's missing, how to save more."""
            result = ask_ai(prompt, system_prompt=BUDGET_SYSTEM_PROMPT)
            review_box.configure(state="normal")
            review_box.delete("1.0", "end")
            review_box.insert("end", result)
            review_box.configure(state="disabled")
            review_btn.configure(state="normal", text="Get AI Review")
        threading.Thread(target=run).start()

    review_btn.configure(command=get_review)

    # ── FOOTER NOTE ──
    ctk.CTkLabel(scroll, text="Other features are unnecessary for this version.",
                 font=font(12), text_color="#888888").pack(pady=(20,10))

    return frame