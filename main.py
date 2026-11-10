
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# DATABASE CONNECTION
conn = sqlite3.connect("quiz_results.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    score INTEGER,
    total_questions INTEGER,
    percentage REAL,
    quiz_date TEXT
)
""")
conn.commit()

# MAIN WINDOW
root = tk.Tk()
root.title("Online Quiz Application")
root.geometry("750x550")
root.configure(bg="#D9F0FF")
root.resizable(False, False)

# QUIZ QUESTIONS
questions = [
    {
        "question": "1. Which language is used for Python programming?",
        "options": ["Python", "Java", "HTML", "CSS"],
        "answer": "Python"
    },
    {
        "question": "2. Which function displays output in Python?",
        "options": ["input()", "print()", "scan()", "show()"],
        "answer": "print()"
    },
    {
        "question": "3. Which data type stores True or False?",
        "options": ["String", "Integer", "Boolean", "Float"],
        "answer": "Boolean"
    },
    {
        "question": "4. Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "&"],
        "answer": "#"
    },
    {
        "question": "5. Which keyword defines a function?",
        "options": ["function", "define", "def", "fun"],
        "answer": "def"
    },
    {
        "question": "6. Which data structure stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary"
    },
    {
        "question": "7. Which loop is used to iterate over a sequence?",
        "options": ["for", "if", "else", "break"],
        "answer": "for"
    },
    {
        "question": "8. Which operator is used for equality comparison?",
        "options": ["=", "==", "!=", "+"],
        "answer": "=="
    },
    {
        "question": "9. Which function returns the length of a list?",
        "options": ["size()", "count()", "length()", "len()"],
        "answer": "len()"
    },
    {
        "question": "10. Which module is used for random numbers?",
        "options": ["math", "random", "time", "os"],
        "answer": "random"
    }
]

# VARIABLES
current_question = 0
score = 0
player_name = ""
selected_answer = tk.StringVar()

# HEADING
heading = tk.Label(
    root,
    text="ONLINE QUIZ APPLICATION",
    font=("Arial", 25, "bold"),
    bg="#D9F0FF",
    fg="#123B60"
)
heading.pack(pady=35)

welcome = tk.Label(
    root,
    text="Welcome! Test Your Knowledge",
    font=("Arial", 17),
    bg="#D9F0FF"
)
welcome.pack(pady=10)

name_label = tk.Label(
    root,
    text="Enter Your Name:",
    font=("Arial", 14),
    bg="#D9F0FF"
)
name_label.pack()

name_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25
)
name_entry.pack(pady=15)

# QUESTION DISPLAY
question_label = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold"),
    bg="#D9F0FF",
    wraplength=650
)

options_frame = tk.Frame(root, bg="#D9F0FF")

# START QUIZ FUNCTION
def start_quiz():
    global current_question, score, player_name

    if name_entry.get().strip() == "":
        messagebox.showwarning(
            "Warning", "Please enter your name!"
        )
        return

    player_name = name_entry.get().strip()
    current_question = 0
    score = 0

    heading.pack_forget()
    welcome.pack_forget()
    name_label.pack_forget()
    name_entry.pack_forget()
    start_button.pack_forget()

    question_label.pack(pady=30)
    options_frame.pack(pady=15)

    show_question()

# DISPLAY QUESTIONS
def show_question():
    selected_answer.set("")

    question_label.config(
        text=questions[current_question]["question"]
    )

    for widget in options_frame.winfo_children():
        widget.destroy()

    for option in questions[current_question]["options"]:
        tk.Radiobutton(
            options_frame,
            text=option,
            variable=selected_answer,
            value=option,
            font=("Arial", 14),
            bg="#D9F0FF",
            activebackground="#D9F0FF"
        ).pack(anchor="w", pady=7)

    progress_label.config(
        text=f"Question {current_question + 1} of {len(questions)}"
    )

    next_button.config(
        text="Next" if current_question < len(questions) - 1
        else "Submit Quiz"
    )
    next_button.pack(pady=20)

# NEXT QUESTION FUNCTION
def next_question():
    global current_question, score

    if selected_answer.get() == "":
        messagebox.showwarning(
            "Warning", "Please select an answer!"
        )
        return

    if selected_answer.get() == questions[current_question]["answer"]:
        score += 1

    current_question += 1

    if current_question < len(questions):
        show_question()
    else:
        show_result()

# SAVE RESULT IN DATABASE
def save_result():
    percentage = (score / len(questions)) * 100

    cursor.execute("""
        INSERT INTO results
        (student_name, score, total_questions, percentage, quiz_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        player_name,
        score,
        len(questions),
        percentage,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

# DISPLAY RESULT
def show_result():
    percentage = (score / len(questions)) * 100

    save_result()

    question_label.config(
        text=(
            "QUIZ COMPLETED!\n\n"
            f"Student Name: {player_name}\n\n"
            f"Your Score: {score}/{len(questions)}\n\n"
            f"Percentage: {percentage:.2f}%\n\n"
            "Congratulations!"
        )
    )

    options_frame.pack_forget()
    next_button.pack_forget()
    progress_label.pack_forget()

    restart_button.pack(pady=10)
    view_button.pack(pady=10)
    exit_button.pack(pady=5)

# VIEW SAVED RESULTS
def view_results():
    window = tk.Toplevel(root)
    window.title("Saved Quiz Results")
    window.geometry("750x350")
    window.configure(bg="#D9F0FF")

    tk.Label(
        window,
        text="PREVIOUS QUIZ RESULTS",
        font=("Arial", 18, "bold"),
        bg="#D9F0FF"
    ).pack(pady=15)

    columns = (
        "Name", "Score", "Total",
        "Percentage", "Date"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=130)

    table.pack(fill="both", expand=True, padx=10, pady=10)

    cursor.execute("""
        SELECT student_name, score, total_questions,
        percentage, quiz_date
        FROM results ORDER BY id DESC
    """)

    for row in cursor.fetchall():
        table.insert("", tk.END, values=row)

# RESTART QUIZ
def restart_quiz():
    global current_question, score

    current_question = 0
    score = 0

    question_label.pack_forget()
    restart_button.pack_forget()
    view_button.pack_forget()
    exit_button.pack_forget()

    progress_label.pack_forget()

    heading.pack(pady=35)
    welcome.pack(pady=10)
    name_label.pack()
    name_entry.delete(0, tk.END)
    name_entry.pack(pady=15)
    start_button.pack(pady=20)

# EXIT APPLICATION
def exit_application():
    conn.close()
    root.destroy()

# BUTTONS
start_button = tk.Button(
    root,
    text="Start Quiz",
    font=("Arial", 14, "bold"),
    bg="#2878B5",
    fg="white",
    command=start_quiz,
    width=15
)
start_button.pack(pady=20)

progress_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    bg="#D9F0FF"
)

next_button = tk.Button(
    root,
    text="Next",
    font=("Arial", 14, "bold"),
    bg="#2878B5",
    fg="white",
    command=next_question,
    width=15
)

restart_button = tk.Button(
    root,
    text="Restart Quiz",
    font=("Arial", 13, "bold"),
    bg="#2878B5",
    fg="white",
    command=restart_quiz
)

view_button = tk.Button(
    root,
    text="View Previous Results",
    font=("Arial", 13, "bold"),
    bg="#2878B5",
    fg="white",
    command=view_results
)

exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 13, "bold"),
    bg="#C0392B",
    fg="white",
    command=exit_application
)

# RUN APPLICATION
root.mainloop()
